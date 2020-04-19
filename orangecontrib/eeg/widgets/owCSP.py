import mne
import numpy
import pywt
from mne.decoding import CSP
from Orange.widgets import gui
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Input, Output, Msg
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from orangecontrib.eeg.utils import style

# !not working widget!
class OWCSP(OWWidget):
	name = "Common Spatial Patterns"
	description = "M/EEG signal decomposition using the Common Spatial Patterns (CSP)."

	#icon = "icons/icon_owaveraging.svg"

	want_main_area = False
	resizing_enabled = True

	class Error(OWWidget.Error):
		num_n_components = Msg("{} is not a valid number of PCA components, continuing with {}.")


	class Inputs:
		data_epoch = Input("Epoch data", mne.Epochs)

	class Outputs:
		out_data = Output("CSP", mne.decoding.csp.CSP)

	def __init__(self):
		super().__init__()
		# global variables
		self.n_components = 4
		self.n_components_field = style.create_field(str(self.n_components))

		#gui
		box = gui.widgetBox(self.controlArea, "Info")
		box.setAlignment(Qt.AlignCenter)
		self.info = gui.widgetLabel(box, 'Fill in the necessary parameters.')
		gui.separator(self.controlArea)

		self.field_layout = QGridLayout()
		gui.widgetBox(self.controlArea, margin=10, orientation=self.field_layout)

		n_components_label = QLabel("Number of PCA components.")
		n_components_label.setFont(QFont("Helvetica", pointSize=11))
		n_components_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(n_components_label)
		self.field_layout.addWidget(self.n_components_field)

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
		"""saves changed values"""

		if self.n_components is not None:
			num_n_components = self.n_components_field.text().strip()
			try:
				self.n_components = int(num_n_components)
				self.Error.num_n_components.clear()
			except ValueError:
				self.Error.num_n_components(num_n_components, str(self.n_components))
	
	def makeCsp(self):
		"""makes CSP object"""

		if self.data is not None:
			X = self.data.get_data()  # MEG signals: n_epochs, n_meg_channels, n_times
			y = self.data.events[:, 2]  # target: Audio left or right
			self.clp = CSP(n_components=self.n_components, norm_trace=False)
			self.clp.fit(X, y)

	@Inputs.data_epoch
	def set_epoch(self, epoch):
		"""Initializes and modifies the input data."""
		self.data = epoch
		if self.data is not None:
			self.data = self.data.copy()
			self.makeCsp()
			self.commit()

	def commit(self):
		"""Outputs the processed data."""
		self.Outputs.out_data.send(self.clp)


if __name__ == "__main__":
	WidgetPreview(OWCSP).run()
