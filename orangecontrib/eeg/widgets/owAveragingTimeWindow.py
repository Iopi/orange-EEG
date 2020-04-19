import mne
import math
import numpy
from Orange.widgets import gui
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Input, Output, Msg
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from orangecontrib.eeg.utils import style

from orangecontrib.eeg.utils import style


class OWAveragingTimeWindow(OWWidget):
	"""Orange widget that computes arithmetic mean in defined time areas."""

	name = "Averaging Time Window"
	description = "Computes arithmetic mean in defined time areas."

	#icon = "icons/icon_epochextraction.svg"

	class Error(OWWidget.Error):
		etime = Msg("{} is not a valid float range. Use format e.g. '-0.1,0.5'")
		erange = Msg("{} is out of range of epochs. Range of epochs is '{},{}.'")

	class Inputs:
		data = Input("Epoch data", mne.Epochs)

	class Outputs:
		data = Output("Averaging time window data", numpy.ndarray)

	want_main_area = False

	resizing_enabled = True

	def __init__(self):
		super().__init__()
		self.default_ranges = ["-0.5,0.5", ""]
		self.fields = [style.create_field(self.default_ranges[i]) for i in range(len(self.default_ranges))]
		self.selected_ranges = self.default_ranges

		layout = QGridLayout()
		box = gui.widgetBox(self.controlArea, "Info", orientation=layout)
		box.setAlignment(Qt.AlignCenter)
		info = QLabel("Select the time ranges of time windows to make time window for each epoch and each channel.\n")
		note = QLabel("Note: empty fields will be ignored. Invalid float ranges will also be ignored.")
		layout.addWidget(info)
		layout.addWidget(note)

		gui.separator(self.controlArea)

		self.field_layout = QGridLayout()
		gui.widgetBox(self.controlArea, margin=10, orientation=self.field_layout)
		label = QLabel("Time ranges: ")
		label.setFont(QFont("Helvetica", pointSize=11))
		label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(label)

		for field in self.fields:
			self.field_layout.addWidget(field)

		gui.separator(self.controlArea)

		button_layout = QHBoxLayout()
		button_layout.setAlignment(Qt.AlignCenter)
		gui.widgetBox(self.controlArea, orientation=button_layout)

		add_button = QPushButton("Add")
		add_button.setToolTip("Add a new text field")
		add_button.clicked.connect(self.add_field)
		add_button.setStyleSheet(style.btn_primary)
		add_button.setMinimumSize(QSize(90, 25))
		button_layout.addWidget(add_button)

		remove_button = QPushButton("Remove")
		remove_button.setToolTip("Remove the last text field")
		remove_button.clicked.connect(self.remove_field)
		remove_button.setStyleSheet(style.btn_warning)
		remove_button.setMinimumSize(QSize(90, 25))
		remove_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
		button_layout.addWidget(remove_button)

		layout = QHBoxLayout()
		layout.setAlignment(Qt.AlignCenter)
		gui.widgetBox(self.controlArea, orientation=layout)

		save_btn = QPushButton("Save")
		save_btn.clicked.connect(self.save_times)
		save_btn.setStyleSheet(style.btn_success)
		save_btn.setMinimumSize(QSize(90, 25))
		save_btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
		layout.addWidget(save_btn)		

	def save_times(self):
		times = []
		for i in range(len(self.fields)):
			time_range = self.fields[i].text()
			if time_range != "":
				times.append(time_range)
		self.selected_ranges = times
		print(self.selected_ranges)

	def add_field(self):
		"""Adds a new text field to the field layout in the GUI. And calls the reorder_tabs function."""

		field = style.create_field()
		self.fields.append(field)
		self.field_layout.addWidget(field)
		self.reorder_tabs()

	def remove_field(self):
		"""
		Removes the last field in the field layout. Unless there is only one field.
		"""

		if len(self.fields) != 1:
			field = self.fields.pop()
			time_range = field.text().replace(" ", "").strip()
			if time_range in self.selected_ranges:
				self.selected_ranges.remove(time_range)
			field.setParent(None)

	def reorder_tabs(self):
		"""Creates a new tab order for the text fields."""

		for i in range(1, len(self.fields)):
			field = self.fields[i - 1]
			second_field = self.fields[i]
			field.setTabOrder(field, second_field)

	def set_selected_ranges(self):
		"""Adds all unique text from the text fields as a channel name to the selected channels."""

		self.selected_ranges.clear()
		for field in self.fields:
			time_range = field.text().replace(" ", "").strip()
			if time_range is not "" and time_range not in self.selected_ranges:
				self.selected_ranges.append(time_range)

	def clear_errors(self):
		self.Error.etime.clear()
		self.Error.erange.clear()

	def make_average(self):
		"""
		Make averageing time window from Epochs.
		"""
		
		windows = []
		
		for time_range in self.selected_ranges:
			try:
				time = [float(i) for i in time_range.split(",")]
				if len(time) != 2:
					self.Error.etime(time)
				else:
					if time[0] < self.data.tmin or time[1] > self.data.tmax:
						self.Error.erange(time_range, self.data.tmin, self.data.tmax)
					else:
						windows.append(time)
			except ValueError:
				self.Error.etime(time_range)

		print(windows)

		epochs_len = len(self.data.get_data())
		channels_len = len(self.data.get_data()[0])
		window_num = len(windows)

		self.resultArray = numpy.zeros((epochs_len, channels_len, window_num), dtype=float)

		for w in range(window_num):
			t_idx = self.data.time_as_index((windows[w][0], windows[w][1]))
			epochs_data = self.data.get_data()[:,:,t_idx[0]:t_idx[1]] 
			times_len = len(epochs_data[0][0])
			
			for e in range(epochs_len):
				for ch in range(channels_len):
					sum = 0 
					for t in range(times_len):
						sum += epochs_data[e][ch][t]

					self.resultArray[e][ch][w] = sum / times_len

	@Inputs.data
	def set_input_data(self, input_data):
		"""Initializes and modifies the input data and then sends the data on the output."""

		self.data = input_data
		if self.data is not None:
			self.data = self.data.copy()
			self.clear_errors()
			self.set_selected_ranges()
			self.make_average()
		self.commit()

	def commit(self):
		"""Sends the data on the output."""

		self.Outputs.data.send(self.resultArray)

if __name__ == "__main__":
	WidgetPreview(OWAveragingTimeWindow).run()
