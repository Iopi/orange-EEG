import mne
import numpy
import pywt
from mne.time_frequency import csd_fourier
import matplotlib.pyplot as plt
from Orange.widgets import gui
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Input, Output, Msg
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel, QSizePolicy, QCheckBox
from orangecontrib.eeg.utils import style


class OWPlotICA(OWWidget):
	name = "PlotICA"
	description = "Plot the Independent Component Analysis."

	icon = "icons/icon_plotica.svg"

	want_main_area = False
	resizing_enabled = True

	class Information(OWWidget.Information):
		accepted_data = Msg("Accepted data ready to plot.")

	class Inputs:
		data_epoch = Input("Epoch data", mne.Epochs)
		data_evoked = Input("Evoked data", mne.Evoked)
		data_raw = Input("Raw data", mne.io.Raw)
		data = Input("ICA", mne.preprocessing.ica.ICA)

	def __init__(self):
		super().__init__()

		self.data = None
		self.icaObj = None

		box = gui.widgetBox(self.controlArea, "Info")
		box.setAlignment(Qt.AlignCenter)
		self.info = gui.widgetLabel(box, 'Plot ICA.')
		gui.separator(self.controlArea)

		self.field_layout = QGridLayout()
		gui.widgetBox(self.controlArea, margin=10, orientation=self.field_layout)

		self.b1 = QCheckBox("Sources")
		self.b1.setChecked(True)
		self.field_layout.addWidget(self.b1)
			
		self.b2 = QCheckBox("Components")
		self.field_layout.addWidget(self.b2)

		layout = QHBoxLayout()
		layout.setAlignment(Qt.AlignCenter)
		gui.widgetBox(self.controlArea, orientation=layout)

		self.show_plot_btn = QPushButton("Show plot")
		self.show_plot_btn.setEnabled(False)
		self.show_plot_btn.setMinimumSize(QSize(120, 25))
		self.show_plot_btn.clicked.connect(self.plotICA)
		layout.addWidget(self.show_plot_btn)

	def plotICA(self):
		if self.data is not None and self.icaObj is not None:
			if (self.b1.isChecked() == True):
				self.icaObj.plot_sources(self.data)

			if (self.b2.isChecked() == True):
				self.icaObj.plot_components()
	
	@Inputs.data
	def set_data(self, obj):
		"""Initializes and modifies the input data."""
		self.icaObj = obj
		if self.icaObj is not None and self.data is not None:
			self.show_plot_btn.setEnabled(True)
			self.show_plot_btn.setStyleSheet(style.btn_primary)
			self.Information.accepted_data()

	@Inputs.data_epoch
	def set_input_epoch(self, epoch):
		"""Initializes and modifies the input data and then sends the data on the output."""
		self.data = epoch
		if self.icaObj is not None and self.data is not None:
			self.show_plot_btn.setEnabled(True)
			self.show_plot_btn.setStyleSheet(style.btn_primary)
			self.Information.accepted_data()

	@Inputs.data_evoked
	def set_input_evoked(self, evoked):
		"""Initializes and modifies the input data and then sends the data on the output."""
		self.data = evoked
		if self.data is not None:
			self.show_plot_btn.setEnabled(True)
			self.show_plot_btn.setStyleSheet(style.btn_primary)
			self.Information.accepted_data()

	@Inputs.data_raw
	def set_input_raw(self, raw):
		"""Initializes and modifies the input data and then sends the data on the output."""
		self.data = raw
		if self.data is not None:
			self.show_plot_btn.setEnabled(True)
			self.show_plot_btn.setStyleSheet(style.btn_primary)
			self.Information.accepted_data()

if __name__ == "__main__":
	WidgetPreview(OWPlotICA).run()
