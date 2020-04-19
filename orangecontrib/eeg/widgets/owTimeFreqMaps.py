import mne
import numpy
import pywt
from mne.time_frequency import tfr_morlet
import matplotlib.pyplot as plt
from Orange.widgets import gui
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Input, Output, Msg
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel, QSizePolicy, QCheckBox
from orangecontrib.eeg.utils import style


class OWTimeFreqMaps(OWWidget):
	name = "Time Frequency Maps"
	description = "Plot time-frequency maps."

	#icon = "icons/icon_owaveraging.svg"

	want_main_area = False
	resizing_enabled = True

	class Information(OWWidget.Information):
		accepted_data = Msg("Accepted data ready to plot.")

	class Error(OWWidget.Error):
		efreqs = Msg("{} is not a valid array of float, continuing with {}.")
		eba = Msg("{} is not a valid float, continuing with {}.")
		ebb = Msg("{} is not a valid float, continuing with {}.")
		enc = Msg("{} is not a valid Integer or 'scale', continuing with {}.")
		ech = Msg("{} is not a valid Integer, continuing with {}.")

	class Inputs:
		data_epoch = Input("Epoch data", mne.Epochs)
		data_evoked = Input("Evoked data", mne.Evoked)

	def __init__(self):
		super().__init__()

		self.freqs = numpy.array([1, 2, 3, 4])
		self.n_cycles = "scale"
		self.baselineA = None
		self.baselineB = None
		self.mode = "logratio"
		self.channel = 0

		self.freqs_field = style.create_field(str("1, 2, 3, 4"))
		self.n_cycles_field = style.create_field(str(self.n_cycles))
		self.baselineA_field = style.create_field(str(self.baselineA))
		self.baselineB_field = style.create_field(str(self.baselineB))
		self.mode_field = style.create_field(str(self.mode))
		self.channel_field = style.create_field(str(self.channel))

		box = gui.widgetBox(self.controlArea, "Info")
		box.setAlignment(Qt.AlignCenter)
		self.info = gui.widgetLabel(box, 'Plot TF Maps.')
		gui.separator(self.controlArea)

		self.field_layout = QGridLayout()
		gui.widgetBox(self.controlArea, margin=10, orientation=self.field_layout)

		freqs_label = QLabel("freqs ")
		freqs_label.setFont(QFont("Helvetica", pointSize=11))
		freqs_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(freqs_label)
		self.field_layout.addWidget(self.freqs_field)

		n_cycles_label = QLabel("n_cycles")
		n_cycles_label.setFont(QFont("Helvetica", pointSize=11))
		n_cycles_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(n_cycles_label)
		self.field_layout.addWidget(self.n_cycles_field)

		baselineA_label = QLabel("baseline a")
		baselineA_label.setFont(QFont("Helvetica", pointSize=11))
		baselineA_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(baselineA_label)
		self.field_layout.addWidget(self.baselineA_field)

		baselineB_label = QLabel("baseline b")
		baselineB_label.setFont(QFont("Helvetica", pointSize=11))
		baselineB_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(baselineB_label)
		self.field_layout.addWidget(self.baselineB_field)

		mode_label = QLabel("mode")
		mode_label.setFont(QFont("Helvetica", pointSize=11))
		mode_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(mode_label)
		self.field_layout.addWidget(self.mode_field)
		
		channel_label = QLabel("channel")
		channel_label.setFont(QFont("Helvetica", pointSize=11))
		channel_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(channel_label)
		self.field_layout.addWidget(self.channel_field)

		self.b1 = QCheckBox("Plot TF of channel")
		self.b1.setChecked(True)
		self.field_layout.addWidget(self.b1)
			
		self.b2 = QCheckBox("Plot topography")
		self.field_layout.addWidget(self.b2)

		layout = QHBoxLayout()
		layout.setAlignment(Qt.AlignCenter)
		gui.widgetBox(self.controlArea, orientation=layout)

		save_btn = QPushButton("Save")
		save_btn.clicked.connect(self.save_values)
		save_btn.setStyleSheet(style.btn_success)
		save_btn.setMinimumSize(QSize(90, 25))
		save_btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
		layout.addWidget(save_btn)

		self.show_plot_btn = QPushButton("Show plot")
		self.show_plot_btn.setEnabled(False)
		self.show_plot_btn.setMinimumSize(QSize(120, 25))
		self.show_plot_btn.clicked.connect(self.plotTFMaps)
		layout.addWidget(self.show_plot_btn)

	def save_values(self):
		fr = self.freqs_field.text().strip()
		nc = self.n_cycles_field.text().strip()
		ba = self.baselineA_field.text().strip()
		bb = self.baselineB_field.text().strip()
		ch = self.channel_field.text().strip()
		self.mode = self.mode_field.text().strip()

		try:
			self.freqs = numpy.array([float(n) for n in fr.split(',')])
			self.Error.efreqs.clear()
		except ValueError:
			self.Error.efreqs(fr, str(self.freqs))

		if (nc == 'scale'):
			self.n_cycles = 'scale'
		else:
			try:
				self.n_cycles = int(nc)
				self.Error.enc.clear()
			except ValueError:
				self.Error.enc(nc, str(self.n_cycles))

		try:
			self.baselineA = float(ba)
			self.Error.eba.clear()
		except ValueError:
			self.Error.eba(ba, str(self.baselineA))

		try:
			self.baselineB = float(bb)
			self.Error.ebb.clear()
		except ValueError:
			self.Error.ebb(bb, str(self.baselineB))

		try:
			self.channel = int(ch)
			self.Error.ech.clear()
		except:
			self.Error.ech(ch, str(self.channel))

	def plotTFMaps(self):
		if self.data:
			if self.n_cycles == 'scale':
				number = self.freqs / 2.
			else:
				number = self.n_cycles

			power = tfr_morlet(self.data, freqs=self.freqs, n_cycles=number, return_itc=False)

			if (self.b1.isChecked() == True):
				power.plot([self.channel], baseline=(self.baselineA, self.baselineB), mode=self.mode, title=power.ch_names[self.channel])

			if (self.b2.isChecked() == True):
				power.plot_topo(baseline=(self.baselineA, self.baselineB), mode=self.mode, title='Average power')

	@Inputs.data_epoch
	def set_input_epoch(self, epoch):
		"""Initializes and modifies the input data and then sends the data on the output."""
		self.data = epoch
		if self.data is not None:
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

if __name__ == "__main__":
	WidgetPreview(OWTimeFreqMaps).run()
