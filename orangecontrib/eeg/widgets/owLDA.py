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

	class Error(OWWidget.Error):
		esol = Msg("{} is not a valid solver value, continuing with {}.")
		eshr = Msg("{} is not a valid shrinkage value, continuing with {}.")
		eshring = Msg("{} is not a between values 0 and 1, continuing with {}.")

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

		self.solver = 'svd'
		self.shrinkage = None

		#GUI
		self.solver_field = style.create_field(str(self.solver))
		self.shrinkage_field = style.create_field(str(self.shrinkage))

		layout = QGridLayout()
		box = gui.widgetBox(self.controlArea, "Info", orientation=layout)
		box.setAlignment(Qt.AlignCenter)
		info = QLabel("Enter solver and shrinkage to classificate classes.")
		layout.addWidget(info)

		boxMarker = gui.widgetBox(self.controlArea, "Results")
		self.marker_info = gui.widgetLabel(boxMarker, "No results")

		gui.separator(self.controlArea)

		self.field_layout = QGridLayout()
		gui.widgetBox(self.controlArea, margin=10, orientation=self.field_layout)
		solver_label = QLabel("Solver")
		solver_label.setFont(QFont("Helvetica", pointSize=11))
		solver_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(solver_label)
		self.field_layout.addWidget(self.solver_field)

		# gui.separator(self.controlArea)

		shrinkage_label = QLabel("Shrinkage")
		shrinkage_label.setFont(QFont("Helvetica", pointSize=11))
		shrinkage_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(shrinkage_label)
		self.field_layout.addWidget(self.shrinkage_field)

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
		sol = self.solver_field.text().strip()
		shr = self.shrinkage_field.text().strip()


		if sol != "svd" and sol != "lsqr" and sol != "eigen":
			self.Error.esol(sol, str(self.solver))
		else:
			self.solver = sol
			self.Error.esol.clear()

		if shr == 'None':
			self.solver = None
		else:
			if shr == 'auto':
				self.solver = 'auto'
			else:
				try:
					shrink = float(shr)
					self.Error.eshr.clear()
					self.Error.eshring.clear()
				except ValueError:
					self.Error.eshr(shr, str(self.shrinkage))
				if shrink >= 0 and shrink <= 1:
					self.shrinkage = shrink
				else:
					self.Error.eshring(shrink, str(self.shrinkage))
		

	def makeLda(self):
		"""Predicts test's labels"""
		
		self.gained_y_test = None
		if self.X_train is not None and self.y_train is not None and self.X_test is not None and self.y_test is not None:
			ldaObj = LinearDiscriminantAnalysis(solver=self.solver, shrinkage=self.shrinkage)
			ldaObj.fit(self.X_train, self.y_train)
			self.gained_y_test = ldaObj.predict(self.X_test)	

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

			self.marker_info.setText("precision - " + str(self.precision) + "\nrecall - " + str(self.recall) + "\naccuracy - " + str(self.accuracy))

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

	@Inputs.test_data_y
	def set_test_y(self, test_data_y):
		"""Initializes and modifies the input data."""
		self.y_test = test_data_y
		if self.X_train is not None and self.y_train is not None and self.X_test is not None and self.y_test is not None:
			self.makeLda()
			self.commit()

	def commit(self):
		"""Outputs the processed data."""
		self.Outputs.precision.send(self.precision)
		self.Outputs.recall.send(self.recall)
		self.Outputs.accuracy.send(self.accuracy)


if __name__ == "__main__":
	WidgetPreview(OWLDA).run()
