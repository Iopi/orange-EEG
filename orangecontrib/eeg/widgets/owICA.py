import mne
import numpy
import pywt
from mne.preprocessing import ICA
from Orange.widgets import gui
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Input, Output, Msg
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from orangecontrib.eeg.utils import style


class OWICA(OWWidget):
	name = "Independent Component Analysis"
	description = "M/EEG signal decomposition using Independent Component Analysis (ICA)."

	#icon = "icons/icon_owaveraging.svg"

	want_main_area = False
	resizing_enabled = True

	class Error(OWWidget.Error):
		num_n_components = Msg("{} is not a valid number of PCA components, continuing with {}.")
		num_random_state = Msg("{} is not a valid random state, continuing with {}.")
		num_max_iter = Msg("{} is not a valid maximum number of iterations, continuing with {}.")

	class Inputs:
		data_epoch = Input("Epoch data", mne.Epochs)
		data_evoked = Input("Evoked data", mne.Evoked)
		data_raw = Input("Raw data", mne.io.Raw)

	class Outputs:
		out_data = Output("ICA", mne.preprocessing.ica.ICA)

	def __init__(self):
		super().__init__()
		self.n_components = None
		self.random_state = None
		self.max_iter = 200

		self.n_components_field = style.create_field(str(self.n_components))
		self.random_state_field = style.create_field(str(self.random_state))
		self.max_iter_field = style.create_field(str(self.max_iter))

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

		random_state_label = QLabel("Random state to initialize ICA estimation for reproducible results.")
		random_state_label.setFont(QFont("Helvetica", pointSize=11))
		random_state_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(random_state_label)
		self.field_layout.addWidget(self.random_state_field)

		max_iter_label = QLabel("Maximum number of iterations during fit.")
		max_iter_label.setFont(QFont("Helvetica", pointSize=11))
		max_iter_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(max_iter_label)
		self.field_layout.addWidget(self.max_iter_field)

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
		if self.n_components is not None:
			num_n_components = self.n_components_field.text().strip()
			try:
				self.n_components = int(num_n_components)
				self.Error.num_n_components.clear()
			except:
				try:
					self.n_components = float(num_n_components)
				except ValueError:
					self.Error.num_n_components(num_n_components, str(self.n_components))
		else:
			self.n_components = None

		if self.random_state is not None:
			num_random_state = self.random_state_field.text().strip()
			try:
				self.random_state = int(num_random_state)
				self.Error.num_random_state.clear()
			except ValueError:
				self.Error.num_random_state(num_random_state, str(self.random_state))
		else:
			self.random_state = None

		num_max_iter = self.max_iter_field.text().strip()
		try:
			self.max_iter = int(num_max_iter)
			self.Error.num_max_iter.clear()
		except ValueError:
			self.Error.num_max_iter(num_max_iter, str(self.max_iter))
	
	def makeIca(self):
		if self.data is not None:
			self.icaObj = ICA(n_components=self.n_components, random_state=self.random_state, method='extended-infomax', max_iter=self.max_iter)
			self.icaObj.fit(self.data)	

	@Inputs.data_epoch
	def set_epoch(self, epoch):
		"""Initializes and modifies the input data."""
		self.data = epoch
		if self.data is not None:
			self.data = self.data.copy()
			self.makeIca()
			self.commit()
	
	@Inputs.data_raw
	def set_raw(self, raw):
		"""Initializes and modifies the input data."""
		self.data = raw
		if self.data is not None:
			self.data = self.data.copy()
			self.makeIca()
			self.commit()

	@Inputs.data_evoked
	def set_evoked(self, evoked):
		"""Initializes and modifies the input data."""
		self.data = evoked
		if self.data is not None:
			self.data = self.data.copy()
			self.makeIca()
			self.commit()

	def commit(self):
		"""Outputs the processed data."""
		self.Outputs.out_data.send(self.icaObj)


if __name__ == "__main__":
	WidgetPreview(OWICA).run()
