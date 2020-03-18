import mne
from mne.io.brainvision.brainvision import RawBrainVision as BrainVision
from Orange.widgets import gui
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Input, Msg
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QGridLayout, QPushButton

from EEGWorkflow.utils import style


class OWEEGPlot(OWWidget):
	"""Orange widget that plots epochs from an eeg data file."""

	name = "EEG Plot"
	description = "Plots the eeg data."

	icon = "icons/icon_owplot.svg"

	class Information(OWWidget.Information):
		accepted_data = Msg("Accepted data ready to plot.")

	class Warning(OWWidget.Warning):
		invalid_type = Msg("Invalid input type {}. Available types: {}.")

	class Inputs:
		raw = Input("Raw data", mne.io.Raw)
		brain_vision = Input("BrainVision data", BrainVision)
		evoked = Input("Evoked data", mne.Evoked)
		epochs = Input("Epoch data", mne.Epochs)

	want_main_area = False
	resizing_enabled = False

	def __init__(self):
		super().__init__()
		self.inputs = {"raw": None, "brain_vision": None, "evoked": None, "epochs": None}
		layout = QGridLayout()
		gui.widgetBox(self.controlArea, orientation=layout, margin=50)

		self.show_plot_btn = QPushButton("Show plot")
		self.show_plot_btn.setEnabled(False)
		self.show_plot_btn.setMinimumSize(QSize(120, 25))
		self.show_plot_btn.clicked.connect(self.plot_eeg)
		layout.addWidget(self.show_plot_btn)

	@Inputs.raw
	def input_raw(self, raw_data):
		self.inputs["raw"] = raw_data
		self.button_change()

	@Inputs.brain_vision
	def input_brain_vision(self, brain_vision_data):
		self.inputs["brain_vision"] = brain_vision_data
		self.button_change()

	@Inputs.evoked
	def input_evoked(self, evoked_data):
		self.inputs["evoked"] = evoked_data
		self.button_change()

	@Inputs.epochs
	def input_epochs(self, epoch_data):
		self.inputs["epochs"] = epoch_data
		self.button_change()

	def button_change(self):
		has_input = False
		for input_data in self.inputs.values():
			if input_data is not None:
				has_input = True
				break

		if has_input:
			self.show_plot_btn.setEnabled(True)
			self.show_plot_btn.setStyleSheet(style.btn_primary)
			self.Information.accepted_data()
		else:
			self.Information.clear()
			self.show_plot_btn.setEnabled(False)
			self.show_plot_btn.setStyleSheet(None)

	def plot_eeg(self):
		for input_data in self.inputs.values():
			if input_data is not None:
				input_data.plot()


if __name__ == "__main__":
	WidgetPreview(OWEEGPlot).run()
