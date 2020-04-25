import mne
import numpy
import pywt
from mne.time_frequency import csd_fourier
from Orange.widgets import gui
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Input, Output, Msg
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from orangecontrib.eeg.utils import style


class OWFilter(OWWidget):
	name = "Filter"
	description = "Filter a subset of channels."

	icon = "icons/icon_filter.svg"

	want_main_area = False
	resizing_enabled = True

	class Error(OWWidget.Error):
		num_l_freq = Msg("{} is not a valid start frequency to consider, continuing with {}.")
		num_h_freq = Msg("{} is not a valid end frequency to consider, continuing with {}.")


	class Inputs:
		data_epoch = Input("Epoch data", mne.Epochs)
		data_evoked = Input("Evoked data", mne.Evoked)
		data_raw = Input("Raw data", mne.io.Raw)

	class Outputs:
		out_data_epoch = Output("Epoch data", mne.Epochs)
		out_data_evoked = Output("Evoked data", mne.Evoked)
		out_data_raw = Output("Raw data", mne.io.Raw)

	def __init__(self):
		super().__init__()
		self.l_freq = 0.1
		self.h_freq = 12.

		self.l_freq_field = style.create_field(str(self.l_freq))
		self.h_freq_field = style.create_field(str(self.h_freq))


		box = gui.widgetBox(self.controlArea, "Info")
		box.setAlignment(Qt.AlignCenter)
		self.info = gui.widgetLabel(box, 'Fill the lower and upper pass-band edge.')
		gui.separator(self.controlArea)

		self.field_layout = QGridLayout()
		gui.widgetBox(self.controlArea, margin=10, orientation=self.field_layout)

		l_freq_label = QLabel("The lower pass-band edge.")
		l_freq_label.setFont(QFont("Helvetica", pointSize=11))
		l_freq_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(l_freq_label)
		self.field_layout.addWidget(self.l_freq_field)

		h_freq_label = QLabel("The upper pass-band edge.")
		h_freq_label.setFont(QFont("Helvetica", pointSize=11))
		h_freq_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(h_freq_label)
		self.field_layout.addWidget(self.h_freq_field)

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
		num_l_freq = self.l_freq_field.text().strip()
		if num_l_freq == 'None':
			self.l_freq = None
		else:
			try:
				self.l_freq = float(num_l_freq)
				self.Error.num_l_freq.clear()
			except ValueError:
				self.Error.num_l_freq(num_l_freq, str(self.l_freq))

		num_h_freq = self.h_freq_field.text().strip()
		if num_h_freq == 'None':
			self.h_freq = None
		else:
			try:
				self.h_freq = float(num_h_freq)
				self.Error.num_h_freq.clear()
			except ValueError:
				self.Error.num_h_freq(num_h_freq, str(self.h_freq))


	def filter(self):
		self.filter_data = self.data.filter(self.l_freq, self.h_freq)

	@Inputs.data_epoch
	def set_input_epoch(self, epoch):
		"""Initializes and modifies the input data and then sends the data on the output."""
		self.data = epoch
		if self.data is not None:
			self.data = self.data.copy()
			self.filter()
			self.commit_epoch()

	@Inputs.data_evoked
	def set_input_evoked(self, evoked):
		"""Initializes and modifies the input data and then sends the data on the output."""
		self.data = evoked
		if self.data is not None:
			self.data = self.data.copy()
			self.filter()
			self.commit_evoked()

	@Inputs.data_raw
	def set_input_raw(self, raw):
		"""Initializes and modifies the input data and then sends the data on the output."""
		self.data = raw
		if self.data is not None:
			self.data = self.data.copy()
			self.filter()
			self.commit_raw()

	def commit_epoch(self):
		"""Outputs the processed data."""
		self.Outputs.out_data_epoch.send(self.filter_data)

	def commit_evoked(self):
		"""Outputs the processed data."""
		self.Outputs.out_data_evoked.send(self.filter_data)

	def commit_raw(self):
		"""Outputs the processed data."""
		self.Outputs.out_data_raw.send(self.filter_data)

if __name__ == "__main__":
	WidgetPreview(OWFilter).run()
