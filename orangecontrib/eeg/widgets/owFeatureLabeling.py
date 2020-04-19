import time

import gc
import mne
import numpy
from Orange.widgets import gui
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Input, Output, Msg
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from orangecontrib.eeg.utils import style

from orangecontrib.eeg.widgets.oweegmarker import EEGMarker


class OWFeatureLabeling(OWWidget):
	name = "Feature Labeling"
	description = "Labels epochs' data according to its events."

	#icon = "icons/icon_epochextraction.svg"

	want_main_area = False
	resizing_enabled = True	

	class Inputs:
		markers = Input("EEG Markers", EEGMarker, multiple=True)
		epochs = Input("Epoch data", mne.Epochs)

	class Outputs:
		vector = Output("Vector", numpy.ndarray)
		labels = Output("Labels", numpy.ndarray)


	def __init__(self):
		super().__init__()
		self.markers = {}
		self.epochs = None

		box = gui.widgetBox(self.controlArea)
		box.setMinimumSize(80, 10)
		box = gui.widgetBox(self.controlArea, "Markers")
		self.marker_info = gui.widgetLabel(box, "No markers")

	def get_labels(self):
		markers_id = []
		labels_of_epochs = numpy.zeros(len(self.epochs))

		for marker in self.markers.values():
			markers_id.append(str(marker.id))

		for i in range(len(self.epochs)):
			id = next(iter(self.epochs[i].event_id.values()))
			for x in markers_id:
				if int(x) == id:
					labels_of_epochs[i] = int(x)
					break

		self.labels = numpy.zeros(len(self.epochs) * len(self.epochs.get_data()[0]))

		for ch in range(len(self.epochs.get_data()[0])):
			for e in range(len(self.epochs)):
				self.labels[e+ch*(len(self.epochs))] = labels_of_epochs[e]

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

		if self.epochs is not None:
			self.get_labels()
			self.commit()

	@Inputs.epochs
	def set_input_epochs(self, input_epochs):
		"""Initializes and modifies the input data and then sends the data on the output."""
		self.epochs = input_epochs
		if self.epochs is not None: 
			self.epochs = self.epochs.copy()
			if self.markers is not None:
				self.get_labels()
				self.commit()

	def commit(self):
		self.Outputs.labels.send(self.labels)
		self.Outputs.vector.send(self.epochs.get_data())


if __name__ == "__main__":
	WidgetPreview(OWFeatureLabeling).run()
