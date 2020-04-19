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
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from orangecontrib.eeg.utils import style


class OWPlotWelchPSD(OWWidget):
	name = "Plot Welch PSD"
	description = "Plot the power spectral density across channels."

	icon = "icons/icon_plot_psd.svg"

	want_main_area = False
	resizing_enabled = True

	class Information(OWWidget.Information):
		accepted_data = Msg("Accepted data ready to plot.")

	class Inputs:
		data = Input("Tuple", tuple)

	def __init__(self):
		super().__init__()

		box = gui.widgetBox(self.controlArea, "Info")
		box.setAlignment(Qt.AlignCenter)
		self.info = gui.widgetLabel(box, 'Plot PSD Welch.')
		gui.separator(self.controlArea)

		self.field_layout = QGridLayout()
		gui.widgetBox(self.controlArea, margin=10, orientation=self.field_layout)

		layout = QHBoxLayout()
		layout.setAlignment(Qt.AlignCenter)
		gui.widgetBox(self.controlArea, orientation=layout)

		self.show_plot_btn = QPushButton("Show plot")
		self.show_plot_btn.setEnabled(False)
		self.show_plot_btn.setMinimumSize(QSize(120, 25))
		self.show_plot_btn.clicked.connect(self.plotPSD)
		layout.addWidget(self.show_plot_btn)
	
	def plotPSD(self):
		if self.data is not None:
			print(numpy.shape(self.data[1]))
			print(numpy.shape(self.data[0]))
			print(numpy.shape(self.data[0][0,:]))
			plt.plot(self.data[1], self.data[0][0,:])
			plt.show()
	
	@Inputs.data
	def set_data(self, input_data):
		"""Initializes and modifies the input data."""
		self.data = input_data
		if self.data is not None:
			self.show_plot_btn.setEnabled(True)
			self.show_plot_btn.setStyleSheet(style.btn_primary)
			self.Information.accepted_data()

if __name__ == "__main__":
	WidgetPreview(OWPlotWelchPSD).run()
