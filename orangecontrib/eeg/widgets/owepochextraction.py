import time

import gc
import mne
import numpy as np
from Orange.widgets import gui
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Input, Output, Msg
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from orangecontrib.eeg.utils import style
import pprint

from orangecontrib.eeg.widgets.oweegmarker import EEGMarker


class OWEpochExtraction(OWWidget):
	"""Orange widget that extracts specified epochs from an eeg data file."""

	name = "Epoch Extraction"
	description = "Extracts specified epochs from the EEG data."

	icon = "icons/icon_epochextraction.svg"

	class Error(OWWidget.Error):
		pre = Msg("{} is not a valid pre value, continuing with {}.")
		post = Msg("{} is not a valid post value, continuing with {}.")

	class Inputs:
		markers = Input("EEG Markers", EEGMarker, multiple=True)
		data = Input("Raw data", mne.io.Raw)

	class Outputs:
		data = Output("Epoch data", mne.Epochs)

	want_main_area = False

	resizing_enabled = True

	def __init__(self):
		super().__init__()
		self.tmin = -0.1
		self.tmax = 1
		self.markers = {}
		self.data = None
		self.prestimulus_field = style.create_field(str(self.tmin))
		self.poststimulus_field = style.create_field(str(self.tmax))

		layout = QGridLayout()
		box = gui.widgetBox(self.controlArea, "Info", orientation=layout)
		box.setAlignment(Qt.AlignCenter)
		info = QLabel("Enter the prestimulus and poststimulus offset in seconds to extract the specific parts of the data.")
		layout.addWidget(info)

		boxMarker = gui.widgetBox(self.controlArea, "Markers")
		self.marker_info = gui.widgetLabel(boxMarker, "No markers")

		gui.separator(self.controlArea)

		self.field_layout = QGridLayout()
		gui.widgetBox(self.controlArea, margin=10, orientation=self.field_layout)
		prestimulus_label = QLabel("PreStimulus offset: (seconds)")
		prestimulus_label.setFont(QFont("Helvetica", pointSize=11))
		prestimulus_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(prestimulus_label)
		self.field_layout.addWidget(self.prestimulus_field)

		# gui.separator(self.controlArea)

		poststimulus_label = QLabel("PostStimulus offset: (seconds)")
		poststimulus_label.setFont(QFont("Helvetica", pointSize=11))
		poststimulus_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(poststimulus_label)
		self.field_layout.addWidget(self.poststimulus_field)

		layout = QHBoxLayout()
		layout.setAlignment(Qt.AlignCenter)
		gui.widgetBox(self.controlArea, orientation=layout)

		save_btn = QPushButton("Save")
		save_btn.clicked.connect(self.save_values)
		save_btn.setStyleSheet(style.btn_success)
		save_btn.setMinimumSize(QSize(90, 25))
		save_btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
		layout.addWidget(save_btn)

		

	def save_values(self):
		pre = self.prestimulus_field.text().strip()
		post = self.poststimulus_field.text().strip()

		try:
			self.tmin = float(pre)
			self.Error.pre.clear()
		except ValueError:
			self.Error.pre(pre, str(self.tmin))

		try:
			self.tmax = float(post)
			self.Error.post.clear()
		except ValueError:
			self.Error.post(post, str(self.tmax))

	def filter_epochs(self):
		

		events = mne.find_events(self.data, shortest_event=1)
		print(events)
		print(np.shape(events))
		if len(events) > 0:
			self.dataEpoch = mne.Epochs(self.data, events=events, tmin=self.tmin, tmax=self.tmax, preload=True,
			                       verbose=False, reject_by_annotation=False)
			if (self.markers):
				markers_id = []
				for marker in self.markers.values():
					print(marker)
					markers_id.append(str(marker.id))

				self.dataEpoch = self.dataEpoch[markers_id]
			print(self.dataEpoch)

		else:
			self.dataEpoch = None
		# print(self.data.drop_log)

	@Inputs.markers
	def add_marker(self, marker, id):
		"""
		Adds a new stimuli marker from a EEGMarker widget to the dictionary of markers.
		If the edge from the marker widget is removed, the marker is deleted from the dictionary.
		"""

		# The marker edge has been removed, remove the marker from the dict
		if id in self.markers and marker is None:
			del self.markers[id]
		else:
			self.markers[id] = marker

		markers = [marker for marker in self.markers.values()]
		info_text = ""
		if not markers:
			info_text = "No markers"
		else:
			for marker in markers:
				info_text += str(marker) + "\n"

		self.marker_info.setText(info_text)

		if self.data is not None:
			self.filter_epochs()

	@Inputs.data
	def set_input_data(self, input_data):
		"""Initializes and modifies the input data and then sends the data on the output."""
		self.data = input_data
		if self.data is not None:
			self.data = self.data.copy()
			self.filter_epochs()
		self.commit()

	def commit(self):
		self.Outputs.data.send(self.dataEpoch)


if __name__ == "__main__":
	WidgetPreview(OWEpochExtraction).run()
