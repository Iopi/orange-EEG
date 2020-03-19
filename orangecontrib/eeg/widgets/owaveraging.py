import time

import mne
import numpy
from Orange.widgets import gui
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Msg

from orangecontrib.eeg.widgets.oweegmarker import EEGMarker


class OWAveraging(OWWidget):
	name = "Averaging"
	description = "Averages the epoch data based on the stimuli markers."

	icon = "icons/icon_owaveraging.svg"

	want_main_area = False
	resizing_enabled = True

	class Warning(OWWidget.Warning):
		no_epochs = Msg("No epochs with the input markers id exist in the input data.")

	class Inputs:
		markers = Input("EEG Markers", EEGMarker, multiple=True)
		data = Input("Epoch data", mne.Epochs)

	class Outputs:
		data = Output("Evoked data", mne.Evoked)

	def __init__(self):
		super().__init__()
		if __name__ == "__main__":
			from orangecontrib.eeg.widgets.owbaselinecorrection import OWBaselineCorrection
			from orangecontrib.eeg.widgets.owlsldatareceiver import OWLSLDataReceiver
			from orangecontrib.eeg.widgets.owchannelselector import OWChannelSelector
			from orangecontrib.eeg.widgets.owepochextraction import OWEpochExtraction
			# selector = OWChannelSelector()
			# selector.set_input_data(
			# 	mne.io.read_raw_brainvision("../data/LED_28_06_2012_104.vhdr", preload=True, stim_channel=True))
			lsl = OWLSLDataReceiver()
			lsl.find_stream()
			time.sleep(20)
			extractor = OWEpochExtraction()
			extractor.set_input_data(lsl.data)
			baseline = OWBaselineCorrection()
			baseline.set_input_data(extractor.data)

			self.data = baseline.data
			self.markers = {"1": EEGMarker("S 2", 0)}
			self.average()
		else:
			self.markers = {}
			self.data = None
			self.amount_of_epochs = 0

		# make it easier to close when the gui opens, even though it's empty
		box = gui.widgetBox(self.controlArea)
		box.setMinimumSize(80, 10)
		box = gui.widgetBox(self.controlArea, "Markers")
		self.marker_info = gui.widgetLabel(box, "No markers")
		gui.separator(self.controlArea)
		self.amount_info = gui.widgetLabel(box, "No epochs averaged.")

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

		if self.data is None:
			self.average()

	@Inputs.data
	def set_data(self, input_data):
		"""Sets the input data."""

		self.data = input_data
		if self.data is not None:
			self.data = self.data.copy()
			self.average()
		else:
			self.amount_of_epochs = 0
			self.amount_info.setText("No epochs averaged.")
			
		self.commit()

	def average(self):
		"""Averages the input epochs based on the input markers. Sends the averaged data on the output."""

		if self.data is not None and self.markers:
			markers = [marker for marker in self.markers.values()]
			print("*******")
			print(self.data)
			print(self.data.events)
			print("*******")
			avg = lambda x: self.average_epochs(x, markers, self.data.events)
			try:
				self.data = self.data.average(method=avg)
				if self.amount_of_epochs is 0:
					self.data = None
			except ZeroDivisionError:
				self.data = None
				self.Warning.no_epochs()

			if self.data is not None:
				self.Warning.clear()

	def average_epochs(self, epoch_data, markers, events):
		"""
		Calculates the average epoch value for each channel in the data based on the stimuli markers.
		"""
		ch_size = epoch_data.shape[1]
		data_size = epoch_data.shape[2]
		# init the list with zeros
		average_data = numpy.zeros((ch_size, data_size))

		self.amount_of_epochs = 0

		# finding all the epochs that have the same id as the input markers
		# summing the data from the found epochs
		for event_idx in range(len(events)):
			event_id = events[event_idx][2]
			for marker in markers:
				if marker.id == event_id:
					epochs = epoch_data[event_idx]

					for i in range(len(epochs)):
						for j in range(len(epochs[i])):
							average_data[i][j] += epochs[i][j]

					self.amount_of_epochs += 1

		# check if epochs were found
		if self.amount_of_epochs is not 0:
			self.amount_info.setText("Epochs averaged: " + str(self.amount_of_epochs))
			# average out the sum epoch data
			for i in range(len(average_data)):
				for j in range(len(average_data[i])):
					average_data[i][j] /= self.amount_of_epochs

		return average_data

	def commit(self):
		"""Outputs the processed data."""

		self.Outputs.data.send(self.data)


if __name__ == "__main__":
	WidgetPreview(OWAveraging).run()
