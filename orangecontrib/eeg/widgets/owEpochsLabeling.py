import time

import gc
import mne
import numpy
from Orange.widgets import gui
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Input, Output, Msg
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from orangecontrib.eeg.utils import style

from orangecontrib.eeg.widgets.oweegmarker import EEGMarker


class OWEpochsLabeling(OWWidget):
	name = "Epochs Labeling"
	description = "Labels epochs' data according to its events."

	icon = "icons/icon_labeling.svg"

	want_main_area = False
	resizing_enabled = True	

	class Error(OWWidget.Error):
		eclass = Msg("{} are not a valid markers range.")
		enum = Msg("{} is not rigth number of classes. Minimum is 2 classes")

	class Inputs:
		epochs = Input("Epoch data", mne.Epochs)

	class Outputs:
		vector = Output("Epoch data", mne.Epochs)
		labels = Output("Labels", numpy.ndarray)


	def __init__(self):
		super().__init__()
		self.epochs = None
		self.default_classes = ["S 1,S 2", "S 3"]
		self.fields = [style.create_field(self.default_classes[i]) for i in range(len(self.default_classes))]
		self.selected_classes = self.default_classes

		layout = QGridLayout()
		box = gui.widgetBox(self.controlArea, "Info", orientation=layout)
		box.setAlignment(Qt.AlignCenter)
		info = QLabel("Select the markers to make labeled classes.\n")
		note = QLabel("Note: One class can have multiple markers. \nFor binary classification use two classes. \n In binary classification will be first class positive and second negative.")
		layout.addWidget(info)
		layout.addWidget(note)

		gui.separator(self.controlArea)

		self.field_layout = QGridLayout()
		gui.widgetBox(self.controlArea, margin=10, orientation=self.field_layout)
		label = QLabel("Classes: ")
		label.setFont(QFont("Helvetica", pointSize=11))
		label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(label)

		for field in self.fields:
			self.field_layout.addWidget(field)

		gui.separator(self.controlArea)

		button_layout = QHBoxLayout()
		button_layout.setAlignment(Qt.AlignCenter)
		gui.widgetBox(self.controlArea, orientation=button_layout)

		add_button = QPushButton("Add")
		add_button.setToolTip("Add a new text field")
		add_button.clicked.connect(self.add_field)
		add_button.setStyleSheet(style.btn_primary)
		add_button.setMinimumSize(QSize(90, 25))
		button_layout.addWidget(add_button)

		remove_button = QPushButton("Remove")
		remove_button.setToolTip("Remove the last text field")
		remove_button.clicked.connect(self.remove_field)
		remove_button.setStyleSheet(style.btn_warning)
		remove_button.setMinimumSize(QSize(90, 25))
		remove_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
		button_layout.addWidget(remove_button)

		layout = QHBoxLayout()
		layout.setAlignment(Qt.AlignCenter)
		gui.widgetBox(self.controlArea, orientation=layout)

		save_btn = QPushButton("Save")
		save_btn.clicked.connect(self.save_classes)
		save_btn.setStyleSheet(style.btn_success)
		save_btn.setMinimumSize(QSize(90, 25))
		save_btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
		layout.addWidget(save_btn)	

	def save_classes(self):
		clsses_list = []
		for i in range(len(self.fields)):
			unique_class = self.fields[i].text()
			if unique_class != "":
				clsses_list.append(unique_class)
		self.selected_classes = clsses_list
		print(self.selected_classes)

	def add_field(self):
		"""Adds a new text field to the field layout in the GUI. And calls the reorder_tabs function."""

		field = style.create_field()
		self.fields.append(field)
		self.field_layout.addWidget(field)
		self.reorder_tabs()

	def remove_field(self):
		"""
		Removes the last field in the field layout. Unless there is only one field.
		"""

		if len(self.fields) != 1:
			field = self.fields.pop()
			unique_class = field.text().strip()
			if unique_class in self.selected_classes:
				self.selected_classes.remove(unique_class)
			field.setParent(None)

	def reorder_tabs(self):
		"""Creates a new tab order for the text fields."""

		for i in range(1, len(self.fields)):
			field = self.fields[i - 1]
			second_field = self.fields[i]
			field.setTabOrder(field, second_field)

	def set_selected_classes(self):
		"""Adds all unique text from the text fields as a channel name to the selected channels."""

		self.selected_classes.clear()
		for field in self.fields:
			unique_class = field.text().strip()
			if unique_class is not "" and unique_class not in self.selected_classes:
				self.selected_classes.append(unique_class)

	def clear_errors(self):
		self.Error.eclass.clear()

	def get_labels(self):
		classes = []
		markers_id = []

		#self.epochs.drop_channels(("STI 014",))
		
		i = 1
		for unique_class in self.selected_classes:
			try:
				markers = unique_class.split(",")
				for m in markers:
					classes.append(m.split(" ")[1] + " " + str(i))
					markers_id.append(str(m.split(" ")[1]))
				i = i + 1
				
			except ValueError:
				self.Error.eclass(unique_class)

		if i < 3:
			self.Error.enum(i-1)
		self.epochs = self.epochs[markers_id]
		labels_of_epochs = numpy.zeros(len(self.epochs))
		for marker in classes:
			marker_id, class_id = [int(a) for a in marker.split(" ")]
			for i in range(len(self.epochs)):
				id = next(iter(self.epochs[i].event_id.values()))
				if marker_id == id:
					labels_of_epochs[i] = class_id

		self.labels = numpy.zeros(len(self.epochs) * len(self.epochs.get_data()[0]))
		for ch in range(len(self.epochs.get_data()[0])):
			for e in range(len(self.epochs)):
				self.labels[e+ch*(len(self.epochs))] = labels_of_epochs[e]

		# self.labels = None
		# self.labels = labels_of_epochs


	@Inputs.epochs
	def set_input_epochs(self, input_epochs):
		"""Initializes and modifies the input data and then sends the data on the output."""
		self.epochs = input_epochs
		if self.epochs is not None: 
			self.epochs = self.epochs.copy()
			self.get_labels()
			self.commit()

	def commit(self):
		self.Outputs.labels.send(self.labels)
		self.Outputs.vector.send(self.epochs)


if __name__ == "__main__":
	WidgetPreview(OWEpochsLabeling).run()
