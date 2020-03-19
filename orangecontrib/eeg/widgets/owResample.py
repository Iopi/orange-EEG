import mne
import numpy
import pywt
from Orange.widgets import gui
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Input, Output, Msg
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from orangecontrib.eeg.utils import style


class OWResample(OWWidget):
	name = "Resample"
	description = "Resample data."

	#icon = "icons/icon_owaveraging.svg"

	want_main_area = False
	resizing_enabled = True

	class Error(OWWidget.Error):
		num_sfreq = Msg("{} is not a valid sample rate, continuing with {}.")

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
		self.sfreq = 200
		self.sfreq_field = style.create_field(str(self.sfreq))

		box = gui.widgetBox(self.controlArea, "Info")
		box.setAlignment(Qt.AlignCenter)
		self.info = gui.widgetLabel(box, 'Fill sample rate to use.')
		gui.separator(self.controlArea)

		self.field_layout = QGridLayout()
		gui.widgetBox(self.controlArea, margin=10, orientation=self.field_layout)

		sfreq_label = QLabel("Sample rate to use.")
		sfreq_label.setFont(QFont("Helvetica", pointSize=11))
		sfreq_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(sfreq_label)
		self.field_layout.addWidget(self.sfreq_field)

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
		num_sfreq = self.sfreq_field.text().strip()

		try:
			self.sfreq = float(num_sfreq)
			self.Error.num_sfreq.clear()
		except ValueError:
			self.Error.num_sfreq(num_sfreq, str(self.sfreq))

	def resample(self):
		self.result = self.data.resample(self.sfreq)	

	@Inputs.data_epoch
	def set_input_epoch(self, epoch):
		"""Initializes and modifies the input data and then sends the data on the output."""
		self.data = epoch
		if self.data is not None:
			self.data = self.data.copy()
			self.resample()
			self.commit_epoch()

	@Inputs.data_evoked
	def set_input_evoked(self, evoked):
		"""Initializes and modifies the input data and then sends the data on the output."""
		self.data = evoked
		if self.data is not None:
			self.data = self.data.copy()
			self.resample()
			self.commit_evoked()

	@Inputs.data_raw
	def set_input_raw(self, raw):
		"""Initializes and modifies the input data and then sends the data on the output."""
		self.data = raw
		if self.data is not None:
			self.data = self.data.copy()
			self.resample()
			self.commit_raw()

	def commit_epoch(self):
		"""Outputs the processed data."""
		self.Outputs.out_data_epoch.send(self.result)

	def commit_evoked(self):
		"""Outputs the processed data."""
		self.Outputs.out_data_evoked.send(self.result)

	def commit_raw(self):
		"""Outputs the processed data."""
		self.Outputs.out_data_raw.send(self.result)

if __name__ == "__main__":
	WidgetPreview(OWResample).run()
