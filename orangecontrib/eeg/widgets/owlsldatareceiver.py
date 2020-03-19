import threading

import mne
from Orange.widgets import gui
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Output, Msg
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QPushButton, QGridLayout, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QSizePolicy as Policy
from mne.io import RawArray
from pylsl import StreamInlet
from pylsl import resolve_byprop

from orangecontrib.eeg.utils import style


class OWLSLDataReceiver(OWWidget):
	name = "LSL Data Receiver"
	description = "Receives EEG LSL data"
	icon = "icons/icon_datareceiver.svg"
	priority = 10

	class Information(OWWidget.Information):
		streams_found = Msg("Streams were found, collecting data.")
		data_loaded = Msg("Data was successfully loaded.")
		stopped_collecting = Msg("No longer collecting data.")

	class Error(OWWidget.Error):
		no_markers = Msg("Unable to find markers stream with these settings.")
		no_data = Msg("Unable to find data stream with these settings.")
		no_streams = Msg("Unable to find either of the streams with these settings.")

	class Warning(OWWidget.Warning):
		not_valid_timeout = Msg("{} is not a valid timeout value, continuing with {}.")

	class Outputs:
		data = Output("Raw data", mne.io.Raw)

	want_main_area = False
	resizing_enabled = True

	def __init__(self):
		super().__init__()
		self.data = None
		self.data_inlet = None
		self.marker_inlet = None
		self.data_pointer = -1
		self.events = []
		self.running = True
		self.ch_names = None
		self.ch_types = None
		self.has_stim = False
		self.timeout = 2
		self.main_thread = threading.current_thread()

		self.data_stream_property = "type"
		self.data_stream_value = "EEG"
		self.markers_stream_property = "type"
		self.markers_stream_value = "Markers"

		elements_width = 135

		# GUI
		layout = QGridLayout()
		box = gui.widgetBox(self.controlArea, "Info", orientation=layout)
		box.setAlignment(Qt.AlignCenter)
		self.info_data_stream = QLabel("Data stream: no stream yet.")
		self.info_markers_stream = QLabel("Markers stream: no stream yet.")
		layout.addWidget(self.info_data_stream)
		layout.addWidget(self.info_markers_stream)

		stream_box = QVBoxLayout()
		box = gui.widgetBox(self.controlArea, "Streams settings", orientation=stream_box)
		box.setAlignment(Qt.AlignCenter)

		data_stream_box = QHBoxLayout()

		data_label_box = QVBoxLayout()
		data_field_box = QVBoxLayout()

		data_stream_property_label = QLabel("Data stream property: ")
		data_stream_property_label.setToolTip(
			"The StreamInfo property that should have a specific value (e.g., 'name', 'type', 'source_id' 'desc/manufaturer'.")
		data_label_box.addWidget(data_stream_property_label)
		self.data_stream_property_field = style.create_field(self.data_stream_property, width=elements_width)
		data_field_box.addWidget(self.data_stream_property_field)

		data_stream_value_label = QLabel("Data stream property value: ")
		data_stream_value_label.setToolTip(
			"The string value that the property should have (e.g., 'EEG' as the type property).")
		data_label_box.addWidget(data_stream_value_label)
		self.data_stream_value_field = style.create_field(self.data_stream_value, width=elements_width)
		data_field_box.addWidget(self.data_stream_value_field)

		data_stream_box.addLayout(data_label_box)
		data_stream_box.addLayout(data_field_box)

		markers_stream_box = QHBoxLayout()

		markers_label_box = QVBoxLayout()
		markers_field_box = QVBoxLayout()

		markers_stream_property_label = QLabel("Markers stream property: ")
		markers_stream_property_label.setToolTip(
			"The StreamInfo property that should have a specific value (e.g., 'name', 'type', 'source_id' 'desc/manufaturer'.")
		markers_label_box.addWidget(markers_stream_property_label)
		self.markers_stream_property_field = style.create_field(self.markers_stream_property, width=elements_width)
		markers_field_box.addWidget(self.markers_stream_property_field)

		markers_stream_value_label = QLabel("Markers stream property value: ")
		markers_stream_value_label.setToolTip(
			"The string value that the property should have (e.g., 'Markers' as the type property).")
		markers_label_box.addWidget(markers_stream_value_label)
		self.markers_stream_value_field = style.create_field(self.markers_stream_value, width=elements_width)
		markers_field_box.addWidget(self.markers_stream_value_field)

		markers_stream_box.addLayout(markers_label_box)
		markers_stream_box.addLayout(markers_field_box)

		stream_box.setSpacing(10)
		stream_box.addLayout(data_stream_box)
		stream_box.addLayout(markers_stream_box)

		btn_box = QVBoxLayout()

		timeout_box = QHBoxLayout()
		timeout_label = QLabel("Timeout: ")
		timeout_label.setToolTip("How long to look for the streams in seconds.")
		timeout_box.addWidget(timeout_label)
		btn_box.addLayout(timeout_box)

		self.timeout_field = style.create_field(str(self.timeout), width=elements_width)
		timeout_box.addWidget(self.timeout_field)

		btn_box.setAlignment(Qt.AlignCenter)
		save_settings_btn = QPushButton("Save stream settings")
		save_settings_btn.setStyleSheet(style.btn_success)
		save_settings_btn.clicked.connect(self.save_stream_settings)
		save_settings_btn.setSizePolicy(Policy.Maximum, Policy.Fixed)
		save_settings_btn.setMinimumSize(QSize(elements_width, 25))
		btn_box.addWidget(save_settings_btn)
		stream_box.addLayout(btn_box)

		layout = QGridLayout()
		gui.widgetBox(self.controlArea, orientation=layout)

		self.find_stream_btn = QPushButton("Find streams")
		self.find_stream_btn.setStyleSheet(style.btn_primary)
		self.find_stream_btn.clicked.connect(self.find_stream)
		self.find_stream_btn.setSizePolicy(Policy.Maximum, Policy.Fixed)
		self.find_stream_btn.setMinimumSize(QSize(elements_width, 25))
		layout.addWidget(self.find_stream_btn)

		output = QPushButton("Send data")
		output.setToolTip("Sends the accumulated data from the streams on the output.")
		output.setStyleSheet(style.btn_primary)
		output.clicked.connect(self.commit)
		output.setSizePolicy(Policy.Maximum, Policy.Fixed)
		output.setMinimumSize(QSize(elements_width, 25))
		layout.addWidget(output)

		self.stop_collecting_btn = QPushButton("Stop")
		self.stop_collecting_btn.setStyleSheet(style.btn_warning)
		self.stop_collecting_btn.clicked.connect(self.stop_collecting)
		self.stop_collecting_btn.setSizePolicy(Policy.Maximum, Policy.Fixed)
		self.stop_collecting_btn.setMinimumSize(QSize(elements_width, 25))
		layout.addWidget(self.stop_collecting_btn)

		self.setMinimumSize(self.layout().sizeHint())

	def onDeleteWidget(self):
		super().onDeleteWidget()
		self.running = False

	def save_stream_settings(self):
		self.data_stream_property = self.data_stream_property_field.text()
		self.data_stream_value = self.data_stream_value_field.text()

		self.markers_stream_property = self.markers_stream_property_field.text()
		self.markers_stream_value = self.markers_stream_value_field.text()

		try:
			self.timeout = int(self.timeout_field.text())
			self.Warning.clear()
		except ValueError:
			self.Warning.not_valid_timeout(self.timeout_field.text(), str(self.timeout))

	def find_stream(self):
		"""Tries to find the data and markers stream, when the streams are found starts collecting the data."""

		if self.data_inlet is None:
			data_streams = resolve_byprop(self.data_stream_property, self.data_stream_value, 1, self.timeout)
			markers_streams = resolve_byprop(self.markers_stream_property, self.markers_stream_value, 1, self.timeout)

			if data_streams and markers_streams:
				self.Error.clear()
				self.Information.clear()
				self.data_inlet = StreamInlet(data_streams[0])
				self.info_data_stream.setText("Data stream: data stream found.")
				self.marker_inlet = StreamInlet(markers_streams[0])
				self.info_markers_stream.setText("Markers stream: markers stream found.")
				self.Information.streams_found()

				thread = threading.Thread(target=self.first_sample_data)
				thread.start()
				self.find_stream_btn.setEnabled(False)
				self.find_stream_btn.setStyleSheet(None)
			else:
				self.Error.clear()
				if data_streams:
					self.Error.no_markers()
				elif markers_streams:
					self.Error.no_data()
				else:
					self.Error.no_streams()

	def create_raw_array(self):
		"""Creates a new RawArray from the data collected by the LSL data stream, if no data was found returns None."""

		sample, timestamp = self.data_inlet.pull_sample()

		if sample is None or len(sample) is 0:
			return None

		if self.ch_names is None:
			# Get the channel info from the data_inlet
			ch_names = []
			ch_types = []
			try:
				ch = self.data_inlet.info().desc().child("channels").child("channel")
				for k in range(self.data_inlet.info().channel_count()):
					ch_names.append(ch.child_value("label"))
					ch_types.append(str(ch.child_value('type')).lower())
					ch = ch.next_sibling()
			except (OSError, UnicodeDecodeError):
				return None

			if len(ch_names) != len(sample) or len(ch_types) != len(sample):
				return None

			for i in range(len(ch_types)):
				if ch_types[i] == "stim":
					self.has_stim = True

			if not self.has_stim:
				ch_names.append("STI 014")
				ch_types.append("stim")

			self.ch_names = ch_names
			self.ch_types = ch_types

		if not self.has_stim:
			sample.append(0)

		info = mne.create_info(self.ch_names, self.data_inlet.info().nominal_srate(), ch_types=self.ch_types)

		# Create an array from the data of the channels
		data = []
		for i in range(len(sample)):
			row = [sample[i]]
			data.append(row)
		self.data_pointer += 1

		return RawArray(data, info, verbose=False)

	def first_sample_data(self):
		"""Collects the first data sample setting the main data instance."""

		while self.data is None:
			self.data = self.create_raw_array()
		self.data = self.data.load_data()
		self.sample()

	def sample(self):
		"""Collects data from the LSL data stream until the user clicks on the Stop button or when the main
		application is closed."""

		while self.running:
			# End sampling when the app closes
			if not self.main_thread.is_alive():
				break

			next_raw = self.create_raw_array()
			if next_raw is not None:
				#strings, timestamp = self.marker_inlet.pull_chunk()
				strings, timestamp = self.marker_inlet.pull_sample()

				self.data.append(next_raw, preload=True)
				events = []

				if len(strings) != 0:

					event_ids = []
					for i in range(len(strings)):
						string = strings[i]#[0]
						event_id = int([s for s in string.split(" ") if s != ""][1])
						event_ids.append(event_id)

					for i in range(len(strings)):
						row = [self.data_pointer, 0, event_ids[i]]
						events.append(row)

				# If any events were received add them to the data
				if events:
					for i in range(len(events)):
						self.events.append(events[i])

					self.data.add_events(self.events, replace=True)

				self.data.load_data()

	def stop_collecting(self):
		"""Sets the self.running attribute to false, stopping the collecting thread."""

		self.Information.clear()
		self.running = False
		self.Information.stopped_collecting()

	def commit(self):
		"""Sends the read data on the output."""

		if self.data is not None:
			self.Outputs.data.send(self.data.copy())


if __name__ == "__main__":
	WidgetPreview(OWLSLDataReceiver).run()
