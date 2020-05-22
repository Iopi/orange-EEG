import mne
import numpy
import pywt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from Orange.widgets import gui
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Input, Output, Msg
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from orangecontrib.eeg.utils import style


class OWSameEpochsCount(OWWidget):
	name = "Same Epochs Count"
	description = "Unifies the number of epoch events for testing classifiers."

	#icon = "icons/icon_.svg"

	want_main_area = False
	resizing_enabled = True

	class Error(OWWidget.Error):
		smaller = Msg("{} is not a valid integer value, continuing with {}.")
		larger = Msg("{} is not a valid integer value, continuing with {}.")

	class Inputs:
		data = Input("Epoch data", mne.Epochs)

	class Outputs:
		data = Output("Epoch data", mne.Epochs)

	def __init__(self):
		super().__init__()
		# global variables
		self.data = None
		self.epochs = None

		self.smaller = 2
		self.larger = 4
		self.min_field = style.create_field(str(self.smaller))
		self.max_field = style.create_field(str(self.larger))

		layout = QGridLayout()
		box = gui.widgetBox(self.controlArea, "Info", orientation=layout)
		box.setAlignment(Qt.AlignCenter)
		info = QLabel("Enter the prestimulus and poststimulus offset in seconds to extract the specific parts of the data.")
		layout.addWidget(info)

		gui.separator(self.controlArea)

		self.field_layout = QGridLayout()
		gui.widgetBox(self.controlArea, margin=10, orientation=self.field_layout)
		prestimulus_label = QLabel("Event ID with a smaller number")
		prestimulus_label.setFont(QFont("Helvetica", pointSize=11))
		prestimulus_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(prestimulus_label)
		self.field_layout.addWidget(self.min_field)

		# gui.separator(self.controlArea)

		poststimulus_label = QLabel("Event ID with a larger number")
		poststimulus_label.setFont(QFont("Helvetica", pointSize=11))
		poststimulus_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(poststimulus_label)
		self.field_layout.addWidget(self.max_field)

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
		smaller = self.min_field.text().strip()
		larger = self.max_field.text().strip()

		try:
			self.smaller = int(smaller)
			self.Error.smaller.clear()
		except ValueError:
			self.Error.smaller(smaller, str(self.smaller))

		try:
			self.larger = int(larger)
			self.Error.larger.clear()
		except ValueError:
			self.Error.larger(larger, str(self.larger))

	def go(self):
		lenTarget = len(self.data[str(self.smaller)])
		epochs1 = self.data[str(self.larger)][:lenTarget]
		epochs2 = self.data[str(self.smaller)]

		self.epochs = mne.concatenate_epochs((epochs1, epochs2))

	@Inputs.data
	def set_train_X(self, data):
		"""Initializes and modifies the input data."""
		self.data = data
		if self.data is not None:
			self.go()
			self.commit()

	def commit(self):
		"""Outputs the processed data."""
		self.Outputs.data.send(self.epochs)


if __name__ == "__main__":
	WidgetPreview(OWSameEpochsCount).run()
