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


class OWStraighten(OWWidget):
	name = "Straighten"
	description = "Auxiliarycfor converting 3d array to 2d array."

	icon = "icons/icon_straighten.svg"

	want_main_area = False
	resizing_enabled = True

	class Inputs:
		data = Input("3D epoch array", numpy.ndarray)

	class Outputs:
		data = Output("2D epoch array", numpy.ndarray)

	def __init__(self):
		super().__init__()
		# global variables
		self.array2d = None
		self.array3d = None

	def straighten(self):
		"""Straighten epoch data by channels"""

		self.array2d = numpy.zeros((len(self.array3d) * len(self.array3d.get_data()[0]), len(self.array3d.get_data()[0][0])), float)

		for ch in range(len(self.array3d.get_data()[0])):
			for e in range(len(self.array3d)):
				for t in range(len(self.array3d.get_data()[0][0])):
					self.array2d[e+ch*(len(self.epochs))][t] = self.array3d[e][ch][t]

	@Inputs.data
	def set_train_X(self, data):
		"""Initializes and modifies the input data."""
		self.array3d = data
		if self.array2d is not None:
			self.straighten()
			self.commit()

	def commit(self):
		"""Outputs the processed data."""
		self.Outputs.data.send(self.array2d)


if __name__ == "__main__":
	WidgetPreview(OWStraighten).run()
