import mne
import numpy
import pywt
from sklearn import svm
from Orange.widgets import gui
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Input, Output, Msg
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from EEGWorkflow.utils import style


class OWSVC(OWWidget):
	name = "Support Vector Classification"
	description = "Set of supervised learning methods used for classification, regression and outliers detection."

	#icon = "icons/icon_owaveraging.svg"

	want_main_area = False
	resizing_enabled = True

	class Inputs:
		data_epoch = Input("Epoch data", mne.Epochs)

	class Outputs:
		out_data = Output("SVC", svm.classes.SVC)

	def __init__(self):
		super().__init__()

	def makeSvc(self):
		if self.data is not None:
			X = self.data.get_data()  # MEG signals: n_epochs, n_meg_channels, n_times
			y = self.data.events[:, 2]  # target: Audio left or right

			self.clp = svm.SVC(gamma='scale')
			self.clp.fit(X[:,0,:], y)


	@Inputs.data_epoch
	def set_epoch(self, epoch):
		"""Initializes and modifies the input data."""
		self.data = epoch
		if self.data is not None:
			self.data = self.data.copy()
			self.makeSvc()
			self.commit()

	def commit(self):
		"""Outputs the processed data."""
		self.Outputs.out_data.send(self.clp)


if __name__ == "__main__":
	WidgetPreview(OWSVC).run()
