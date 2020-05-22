import mne
import numpy
import pywt
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
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

	class Error(OWWidget.Error):
		eran = Msg("{} is not a valid random_state value (int or None), continuing with {}.")
		emax = Msg("{} is not a valid max_iter value(int), continuing with {}.")

	class Inputs:
		train_data_X = Input("Train data", numpy.ndarray)
		train_data_y = Input("Train indexes", numpy.ndarray)
		test_data_X = Input("Target data", numpy.ndarray)
		test_data_y = Input("Target indexes", numpy.ndarray)

	class Outputs:
		precision = Output("Precision", float)
		recall = Output("Recall", float)
		accuracy = Output("Accuracy", float)
		
	def __init__(self):
		super().__init__()
		# global variables
		self.X_train = None
		self.y_train = None
		self.X_test = None
		self.y_test = None

		self.precision = None
		self.recall = None
		self.accuracy = None

		self.random_state = None
		self.max_iter = 1000

		#GUI
		self.random_state_field = style.create_field(str(self.random_state))
		self.max_iter_field = style.create_field(str(self.max_iter))

		layout = QGridLayout()
		box = gui.widgetBox(self.controlArea, "Info", orientation=layout)
		box.setAlignment(Qt.AlignCenter)
		info = QLabel("Enter random state and maximum iteration to classificate classes.")
		layout.addWidget(info)

		boxMarker = gui.widgetBox(self.controlArea, "Results")
		self.marker_info = gui.widgetLabel(boxMarker, "No results")

		gui.separator(self.controlArea)

		self.field_layout = QGridLayout()
		gui.widgetBox(self.controlArea, margin=10, orientation=self.field_layout)
		random_state_label = QLabel("random state")
		random_state_label.setFont(QFont("Helvetica", pointSize=11))
		random_state_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(random_state_label)
		self.field_layout.addWidget(self.random_state_field)

		# gui.separator(self.controlArea)

		max_iter_label = QLabel("max iter")
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
		ran = self.random_state_field.text().strip()
		maxi = self.max_iter_field.text().strip()

		if ran == 'None':
			self.random_state = None
		else:
			try:
				self.random_state = int(ran)
				self.Error.eran.clear()
			except ValueError:
				self.Error.eran(ran, str(self.random_state))

		try:
			self.max_iter = int(maxi)
			self.Error.emax.clear()
		except ValueError:
			self.Error.emax(maxi, str(self.max_iter))
		

	def makeSvm(self):
		"""Predicts test's labels"""
		
		self.gained_y_test = None
		if self.X_train is not None and self.y_train is not None and self.X_test is not None and self.y_test is not None:
			svcObj = svm.LinearSVC(random_state=self.random_state, tol=1e-5, max_iter=self.max_iter)
			svcObj.fit(self.X_train, self.y_train)
			self.gained_y_test = svcObj.predict(self.X_test)

		if len(numpy.unique(self.y_test)) == 2:
			self.binary_classification()

		else:
			self.multi_class_classification()

	def multi_class_classification(self):
		"""Multi class classification for three or more classes """
		hit = 0
		miss = 0

		for i in range(len(self.gained_y_test)):
			if self.gained_y_test[i] == self.y_test[i]:
				hit += 1
			else:
				miss += 1

		self.accuracy = hit / (hit + miss)	

		self.marker_info.setText("accuracy - " + str(self.accuracy))	

	def binary_classification(self):
		"""Binary classification for two classes """
		
		if self.gained_y_test is not None:
			tp = 0 # true positive
			tn = 0 # true negative
			fp = 0 # false positive
			fn = 0 # false negative

			for i in range(len(self.gained_y_test)):
				if self.y_test[i] == 1:
					if self.gained_y_test[i] == 1:
						tp += 1
					else:
						fn += 1
				else:
					if self.y_test[i] == 2:
						if self.gained_y_test[i] == 2:
							tn += 1
						else:
							fp += 1

			self.precision = self.count_precision(tp, tn, fp, fn)
			self.recall = self.count_recall(tp, tn, fp, fn)
			self.accuracy = self.count_accuracy(tp, tn, fp, fn)

			self.marker_info.setText("precision - " + str(self.precision) + "\nrecall - " + 
			str(self.recall) + "\naccuracy - " + str(self.accuracy) + "\ntrue positive - " + str(tp) + 
			"\ntrue negative - " + str(tn) + "\nfalse positive - " + str(fp) + "\nfalse negative - " + str(fn))


	def count_precision(self, tp, tn, fp, fn):
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
			self.makeSvm()
			self.commit()

	@Inputs.train_data_y
	def set_train_y(self, train_data_y):
		"""Initializes and modifies the input data."""
		self.y_train = train_data_y
		if self.X_train is not None and self.y_train is not None and self.X_test is not None and self.y_test is not None:
			self.makeSvm()
			self.commit()

	@Inputs.test_data_X
	def set_test_X(self, test_data_X):
		"""Initializes and modifies the input data."""
		self.X_test = test_data_X
		if self.X_train is not None and self.y_train is not None and self.X_test is not None and self.y_test is not None:
			self.makeSvm()
			self.commit()

	@Inputs.test_data_y
	def set_test_y(self, test_data_y):
		"""Initializes and modifies the input data."""
		self.y_test = test_data_y
		if self.X_train is not None and self.y_train is not None and self.X_test is not None and self.y_test is not None:
			self.makeSvm()
			self.commit()

	def commit(self):
		"""Outputs the processed data."""
		self.Outputs.precision.send(self.precision)
		self.Outputs.recall.send(self.recall)
		self.Outputs.accuracy.send(self.accuracy)

if __name__ == "__main__":
	WidgetPreview(OWSVC).run()
