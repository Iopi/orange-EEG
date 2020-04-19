import mne
import math
import numpy as np
from Orange.widgets import gui
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Input, Output, Msg
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from orangecontrib.eeg.utils import style

from orangecontrib.eeg.widgets.oweegmarker import EEGMarker


class OWSegmentation(OWWidget):
	"""Orange widget that segments epochs from raw data."""

	name = "Segmentation"
	description = "Segments epochs from raw data."

	icon = "icons/icon_segmentation.svg"

	class Error(OWWidget.Error):
		pre = Msg("{} is not a valid pre value, continuing with {}.")
		post = Msg("{} is not a valid post value, continuing with {}.")
		seg = Msg("{} is not a valid Integer value, continuing with {}.")

	class Inputs:
		data = Input("Raw data", mne.io.Raw)

	class Outputs:
		data = Output("Epoch data", mne.Epochs)

	want_main_area = False

	resizing_enabled = True

	def __init__(self):
		super().__init__()
		self.tmin = -0.1
		self.tmax = 1
		self.segment_len = 1000
		self.prestimulus_field = style.create_field(str(self.tmin))
		self.poststimulus_field = style.create_field(str(self.tmax))
		self.segment_len_field = style.create_field(str(self.segment_len))

		layout = QGridLayout()
		box = gui.widgetBox(self.controlArea, "Info", orientation=layout)
		box.setAlignment(Qt.AlignCenter)
		info = QLabel("Enter the segment length to segment the specific parts of the data.")
		layout.addWidget(info)

		gui.separator(self.controlArea)

		self.field_layout = QGridLayout()
		gui.widgetBox(self.controlArea, margin=10, orientation=self.field_layout)

		prestimulus_label = QLabel("PreStimulus offset: (seconds)")
		prestimulus_label.setFont(QFont("Helvetica", pointSize=11))
		prestimulus_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(prestimulus_label)
		self.field_layout.addWidget(self.prestimulus_field)

		# gui.separator(self.controlArea)

		poststimulus_label = QLabel("PostStimulus offset: (seconds)")
		poststimulus_label.setFont(QFont("Helvetica", pointSize=11))
		poststimulus_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(poststimulus_label)
		self.field_layout.addWidget(self.poststimulus_field)

		segment_len_label = QLabel("Segment length")
		segment_len_label.setFont(QFont("Helvetica", pointSize=11))
		segment_len_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(segment_len_label)
		self.field_layout.addWidget(self.segment_len_field)

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
		segment_val = self.segment_len_field.text().strip()
		pre = self.prestimulus_field.text().strip()
		post = self.poststimulus_field.text().strip()

		try:
			self.tmin = float(pre)
			self.Error.pre.clear()
		except ValueError:
			self.Error.pre(pre, str(self.tmin))

		try:
			self.tmax = float(post)
			self.Error.post.clear()
		except ValueError:
			self.Error.post(post, str(self.tmax))

		try:
			self.segment_len = int(segment_val)
			self.Error.seg.clear()
		except ValueError:
			self.Error.seg(segment_val, str(self.segment_len))

	def segment_data(self):
		events_len = math.ceil(len(self.data)/self.segment_len)
		if events_len < len(self.data):
			events_len = events_len + 1

		events = np.zeros((events_len, 3), dtype=int)

		for i in range(events_len):
			events[i][0] = i * self.segment_len
			events[i][2] = i

		print(events)
		print(np.shape(events))
		if len(events) > 0:
			self.dataEpoch = mne.Epochs(self.data, events=events, tmin=self.tmin, tmax=self.tmax, preload=True, verbose=False, reject_by_annotation=False)
			print(self.dataEpoch)

		else:
			self.dataEpoch = None


	@Inputs.data
	def set_input_data(self, input_data):
		"""Initializes and modifies the input data and then sends the data on the output."""
		self.data = input_data
		if self.data is not None:
			self.data = self.data.copy()
			self.segment_data()
			self.commit()

	def commit(self):
		self.Outputs.data.send(self.dataEpoch)


if __name__ == "__main__":
	WidgetPreview(OWSegmentation).run()
