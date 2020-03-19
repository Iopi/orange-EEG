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


class OWDWT(OWWidget):
	name = "Discrete wavelet tranformation"
	description = "Computes approximation and deail coefficient."

	#icon = "icons/icon_owaveraging.svg"

	want_main_area = False
	resizing_enabled = True

	class Error(OWWidget.Error):
		num_degrees = Msg("{} is not a valid degree of transformation, continuing with {}.")

	class Inputs:
		data = Input("Epoch data", mne.Epochs)

	class Outputs:
		approximation = Output("Approximation coefficient", mne.Epochs)
		detail = Output("Detail coefficient", mne.Epochs)

	def __init__(self):
		super().__init__()
		self.wave_family = 'db1'
		self.degrees = 1
		self.family_field = style.create_field(self.wave_family)
		self.degrees_field = style.create_field(str(self.degrees))

		box = gui.widgetBox(self.controlArea, "Info")
		box.setAlignment(Qt.AlignCenter)
		self.info = gui.widgetLabel(box, 'Fill wavelet family and number of degrees of transformation.')
		gui.separator(self.controlArea)

		self.field_layout = QGridLayout()
		gui.widgetBox(self.controlArea, margin=10, orientation=self.field_layout)
		
		family_label = QLabel("Wavelet family")
		family_label.setFont(QFont("Helvetica", pointSize=11))
		family_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(family_label)
		self.field_layout.addWidget(self.family_field)

		degrees_label = QLabel("Number of degrees of transformation")
		degrees_label.setFont(QFont("Helvetica", pointSize=11))
		degrees_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(degrees_label)
		self.field_layout.addWidget(self.degrees_field)

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
		num_degrees = self.degrees_field.text().strip()

		try:
			self.degrees = int(num_degrees)
			self.Error.num_degrees.clear()
		except ValueError:
			self.Error.num_degrees(num_degrees, str(self.degrees))

	def dwt(self):
		for i in range(self.degrees):
			self.data_approximation, self.data_detail = pywt.dwt(self.data, self.wave_family)
			self.data = self.data_approximation		

	@Inputs.data
	def set_input_data(self, input_data):
		"""Initializes and modifies the input data and then sends the data on the output."""
		self.data = input_data
		if self.data is not None:
			self.data = self.data.copy()
			self.dwt()
		self.commit()

	def commit(self):
		self.Outputs.approximation.send(self.data_approximation)
		self.Outputs.detail.send(self.data_detail)

if __name__ == "__main__":
	WidgetPreview(OWDWT).run()
