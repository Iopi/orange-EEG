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
from orangecontrib.eeg.utils import style


class OWSVC(OWWidget):
	name = "Support Vector Classification"
	description = "C-Support Vector Classification."

	icon = "icons/icon_svc.svg"

	want_main_area = False
	resizing_enabled = True

	class Inputs:
		train_data_X = Input("Train data", numpy.ndarray)
		train_data_y = Input("Train indexes", numpy.ndarray)
		test_data_X = Input("Target data", numpy.ndarray)

	class Outputs:
		test_data_y = Output("Target indexes", numpy.ndarray)

	def __init__(self):
		super().__init__()
		self.X_train = None
		self.y_train = None
		self.X_test = None

	def makeSvc(self):
		if self.X_train is not None and self.y_train is not None and self.X_test is not None:
			svcObj = svm.SVC(gamma='auto')
			print(numpy.shape(self.X_train))
			print(numpy.shape(self.y_train))
			print(numpy.shape(self.X_test))
			print(self.y_train)
			svcObj.fit(self.X_train, self.y_train)

			self.y_test = svcObj.predict(self.X_test)
			print(self.y_test)
		else:
			self.y_test = None

	@Inputs.train_data_X
	def set_train_X(self, train_data_X):
		"""Initializes and modifies the input data."""
		self.X_train = train_data_X
		if self.X_train is not None and self.y_train is not None and self.X_test is not None:
			self.makeSvc()
			self.commit()

	@Inputs.train_data_y
	def set_train_y(self, train_data_y):
		"""Initializes and modifies the input data."""
		self.y_train = train_data_y
		if self.X_train is not None and self.y_train is not None and self.X_test is not None:
			self.makeSvc()
			self.commit()

	@Inputs.test_data_X
	def set_test_X(self, test_data_X):
		"""Initializes and modifies the input data."""
		self.X_test = test_data_X
		if self.X_train is not None and self.y_train is not None and self.X_test is not None:
			self.makeSvc()
			self.commit()

	def commit(self):
		"""Outputs the processed data."""
		self.Outputs.test_data_y.send(self.y_test)


if __name__ == "__main__":
	WidgetPreview(OWSVC).run()
