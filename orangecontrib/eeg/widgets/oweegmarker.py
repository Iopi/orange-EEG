from Orange.widgets import gui
from Orange.widgets.utils.signals import Output
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Msg
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QPushButton

from orangecontrib.eeg.utils import style


class EEGMarker:
	"""Class representing one marker in the EEG data."""

	def __init__(self, name, offset):
		self.name = name
		self.offset = offset
		self.id = int(self.name.split(" ")[1])

	def increment_offset(self, length):
		self.offset += length

	def decrement_offset(self, length):
		self.offset -= length

	def __repr__(self):
		return "Name: " + self.name + " Offset: " + str(self.offset)


class OWEEGMarker(OWWidget):
	"""Orange widget representing one EEG marker input."""

	name = "EEG Marker"
	description = "Orange widget representing one EEG marker."

	icon = "icons/icon_marker.svg"

	want_main_area = False
	resizing_enabled = True

	class Error(OWWidget.Error):
		invalid_input = Msg("Offset is not an integer.")

	class Outputs:
		marker = Output("EEG Marker", EEGMarker)

	def __init__(self):
		super().__init__()
		self.EEGMarker = None
		default_marker = EEGMarker("S 2", 0)

		layout = QVBoxLayout()
		gui.widgetBox(self.controlArea, orientation=layout)
		h_box = QHBoxLayout()
		gui.widgetBox(self.controlArea, orientation=h_box)
		name_label = QLabel("Name:\t")
		self.name_input = QLineEdit(default_marker.name)
		self.name_input.setStyleSheet(style.field)
		h_box.addWidget(name_label)
		h_box.addWidget(self.name_input)

		h_box = QHBoxLayout()
		gui.widgetBox(self.controlArea, orientation=h_box)
		name_label = QLabel("Offset:\t")
		self.offset_input = QLineEdit(str(default_marker.offset))
		self.offset_input.setStyleSheet(style.field)
		h_box.addWidget(name_label)
		h_box.addWidget(self.offset_input)

		h_box = QHBoxLayout()
		h_box.setAlignment(Qt.AlignRight)
		gui.widgetBox(self.controlArea, orientation=h_box)
		save_btn = QPushButton("Save")
		save_btn.setStyleSheet(style.btn_success)
		save_btn.clicked.connect(self.set_marker)
		save_btn.setMinimumSize(QSize(60, 25))
		h_box.addWidget(save_btn)

		self.set_marker()

	def set_marker(self):
		"""Initializes the EEG marker and sends it on the output."""

		name = self.name_input.text()
		try:
			offset = int(self.offset_input.text())
			self.EEGMarker = EEGMarker(name, offset)
			self.commit()
		except ValueError:
			self.Error.invalid_input()

	def commit(self):
		"""Sends the marker on the output. """

		if self.EEGMarker is not None:
			self.Outputs.marker.send(self.EEGMarker)


if __name__ == "__main__":
	WidgetPreview(OWEEGMarker).run()
