import mne
import numpy
import pywt
from mne.time_frequency import psd_welch
from Orange.widgets import gui
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Input, Output, Msg
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from orangecontrib.eeg.utils import style


class OWWelchPSD(OWWidget):
	name = "Welch PSD"
	description = "Compute the power spectral density (PSD) using Welch’s method."

	#icon = "icons/icon_owaveraging.svg"

	want_main_area = False
	resizing_enabled = True

	class Error(OWWidget.Error):
		num_fmin = Msg("{} is not a valid start frequency to consider, continuing with {}.")
		num_fmax = Msg("{} is not a valid end frequency to consider, continuing with {}.")
		num_tmin = Msg("{} is not a valid start time to consider, continuing with {}.")
		num_tmax = Msg("{} is not a valid end time to consider, continuing with {}.")
		num_n_fft = Msg("{} is not a valid number of points, continuing with {}.")

	class Inputs:
		data_epoch = Input("Epoch data", mne.Epochs)
		data_evoked = Input("Evoked data", mne.Evoked)
		data_raw = Input("Raw data", mne.io.Raw)

	class Outputs:
		out_data = Output("Tuple", tuple)

	def __init__(self):
		super().__init__()
		self.fmin = -1000
		self.fmax = 1000
		self.tmin = -1000
		self.tmax = 1000
		self.n_fft = 2500

		self.fmin_field = style.create_field(str(self.fmin))
		self.fmax_field = style.create_field(str(self.fmax))
		self.tmin_field = style.create_field(str(self.tmin))
		self.tmax_field = style.create_field(str(self.tmax))
		self.n_fft_field = style.create_field(str(self.n_fft))

		box = gui.widgetBox(self.controlArea, "Info")
		box.setAlignment(Qt.AlignCenter)
		self.info = gui.widgetLabel(box, 'Fill start and end frequency and time to consider.')
		gui.separator(self.controlArea)

		self.field_layout = QGridLayout()
		gui.widgetBox(self.controlArea, margin=10, orientation=self.field_layout)

		fmin_label = QLabel("Start frequency to consider.")
		fmin_label.setFont(QFont("Helvetica", pointSize=11))
		fmin_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(fmin_label)
		self.field_layout.addWidget(self.fmin_field)

		fmax_label = QLabel("End frequency to consider.")
		fmax_label.setFont(QFont("Helvetica", pointSize=11))
		fmax_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(fmax_label)
		self.field_layout.addWidget(self.fmax_field)

		tmin_label = QLabel("Start time to consider.")
		tmin_label.setFont(QFont("Helvetica", pointSize=11))
		tmin_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(tmin_label)
		self.field_layout.addWidget(self.tmin_field)

		tmax_label = QLabel("End time to consider.")
		tmax_label.setFont(QFont("Helvetica", pointSize=11))
		tmax_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(tmax_label)
		self.field_layout.addWidget(self.tmax_field)

		n_fft_label = QLabel("Number of points to use in Welch FFT calculations.")
		n_fft_label.setFont(QFont("Helvetica", pointSize=11))
		n_fft_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(n_fft_label)
		self.field_layout.addWidget(self.n_fft_field)

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
		num_fmin = self.fmin_field.text().strip()
		try:
			self.fmin = float(num_fmin)
			self.Error.num_fmin.clear()
		except ValueError:
			self.Error.num_fmin(num_fmin, str(self.fmin))

		num_fmax = self.fmax_field.text().strip()
		try:
			self.fmax = float(num_fmax)
			self.Error.num_fmax.clear()
		except ValueError:
			self.Error.num_fmax(num_fmax, str(self.fmin))
			
		if self.tmin is not None:
			num_tmin = self.tmin_field.text().strip()
			try:
				self.tmin = float(num_tmin)
				self.Error.num_tmin.clear()
			except ValueError:
				self.Error.num_tmin(num_tmin, str(self.tmin))
		
		if self.tmax is not None:
			num_tmax = self.tmax_field.text().strip()
			try:
				self.tmax = float(num_tmax)
				self.Error.num_tmax.clear()
			except ValueError:
				self.Error.num_tmax(num_tmax, str(self.tmax))

		num_n_fft = self.n_fft_field.text().strip()
		try:
			self.n_fft = int(num_n_fft)
			self.Error.num_n_fft.clear()
		except ValueError:
			self.Error.num_n_fft(num_n_fft, str(self.n_fft))
		

	def welch(self):
		if self.data is not None:
			psds, freqs = psd_welch(self.data, fmin=self.fmin, fmax=self.fmax, tmin=self.tmin, tmax=self.tmax, n_fft=256,
              n_overlap=0, n_per_seg=None, picks=None, proj=False, n_jobs=1,
              reject_by_annotation=True, verbose=None)

			self.welch_result = (psds, freqs)

	@Inputs.data_epoch
	def set_epoch(self, epoch):
		"""Initializes and modifies the input data."""
		self.data = epoch
		if self.data is not None:
			self.data = self.data.copy()
			self.welch()
			self.commit()

	@Inputs.data_evoked
	def set_evoked(self, evoked):
		"""Initializes and modifies the input data."""
		self.data = evoked
		if self.data is not None:
			self.data = self.data.copy()
			self.welch()
			self.commit()
	
	@Inputs.data_raw
	def set_raw(self, raw):
		"""Initializes and modifies the input data."""
		self.data = raw
		if self.data is not None:
			self.data = self.data.copy()
			self.welch()
			self.commit()

	def commit(self):
		"""Outputs the processed data."""
		self.Outputs.out_data.send(self.welch_result)


if __name__ == "__main__":
	WidgetPreview(OWWelchPSD).run()
