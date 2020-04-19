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


class OWLDA(OWWidget):
	name = "Linear Discriminant Analysis"
	description = "A classifier with a linear decision boundary."

	icon = "icons/icon_lda.svg"

	want_main_area = False
	resizing_enabled = True

	class Inputs:
		train_data_X = Input("Train data", numpy.ndarray)
		train_data_y = Input("Train indexes", numpy.ndarray)
		test_data_X = Input("Target data", numpy.ndarray)
		test_data_y = Input("Target indexes", numpy.ndarray)

	class Outputs:
		test_data_y = Output("Target indexes", numpy.ndarray)

	def __init__(self):
		super().__init__()
		# global variables
		self.X_train = None
		self.y_train = None
		self.X_test = None
		self.y_test = None

	def makeLda(self):
		"""Predicts test's labels"""
		
		self.gained_y_test = None
		if self.X_train is not None and self.y_train is not None and self.X_test is not None and self.y_test is not None:
			ldaObj = LinearDiscriminantAnalysis()
			ldaObj.fit(self.X_train, self.y_train)
			self.gained_y_test = ldaObj.predict(self.X_test)			
		
		if self.gained_y_test in not None:
			tp = 0
			tn = 0
			fp = 0
			fn = 0

			for i in range(leb(self.gained_y_test)):
				if self.y_test[i] == 1:
					if self.gained_y_test == 1:
						tp += 1
					else:
						fp += 1
				if self.y_test[i] == 2:
					if self.gained_y_test == 2:
						tn += 1
					else:
						fn += 1

			self.precision = self.count_accuracy(tp, tn, fp, fn)
			self.recall = self.count_recall(tp, tn, fp, fn)
			self.accuracy = self.count_accuracy(tp, tn, fp, fn)

	def count_accuracy(self, tp, tn, fp, fn):
		return tp / (tp + fp)

	def count_recall(self, tp, tn, fp, fn):
		return tp / (tp + fn)

	def count_accuracy(self, tp, tn, fp, fn):
		return (tp + tn) / (tp + tn + fp + fn)

	@Inputs.train_data_X
	def set_train_X(self, train_data_X):
		"""Initializes and modifies the input data."""
		self.X_train = train_data_X
		if self.X_train is not None and self.y_train is not None and self.X_test is not None and self.y_test is not None:
			self.makeLda()
			self.commit()

	@Inputs.train_data_y
	def set_train_y(self, train_data_y):
		"""Initializes and modifies the input data."""
		self.y_train = train_data_y
		if self.X_train is not None and self.y_train is not None and self.X_test is not None and self.y_test is not None:
			self.makeLda()
			self.commit()

	@Inputs.test_data_X
	def set_test_X(self, test_data_X):
		"""Initializes and modifies the input data."""
		self.X_test = test_data_X
		if self.X_train is not None and self.y_train is not None and self.X_test is not None and self.y_test is not None:
			self.makeLda()
			self.commit()

	@Inputs.train_data_y
	def set_train_y(self, test_data_y):
		"""Initializes and modifies the input data."""
		self.y_test = test_data_y
		if self.X_train is not None and self.y_train is not None and self.X_test is not None and self.y_test is not None:
			self.makeLda()
			self.commit()

	def commit(self):
		"""Outputs the processed data."""
		self.Outputs.test_data_y.send(self.y_test)


if __name__ == "__main__":
	WidgetPreview(OWLDA).run()
