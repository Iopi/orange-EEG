import mne
from Orange.widgets import gui
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Input, Output, Msg
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from EEGWorkflow.utils import style


class OWBaselineCorrection(OWWidget):
	"""Orange widget that applies the baseline correction on the EEG data"""

	name = "Baseline Correction"
	description = "Applies the baseline correction on the EEG data."

	icon = "icons/icon_owbaseline.svg"

	class Error(OWWidget.Error):
		start = Msg("{} is not a valid start value, continuing with {}.")
		end = Msg("{} is not a valid end value, continuing with {}.")

	class Inputs:
		data = Input("Epoch data", mne.Epochs)

	class Outputs:
		data = Output("Epoch data", mne.Epochs)

	want_main_area = False
	resizing_enabled = True

	def __init__(self):
		super().__init__()
		self.start_time = 0
		self.end_time = 1
		self.data = None
		self.baseline_start_field = style.create_field(str(self.start_time))
		self.baseline_end_field = style.create_field(str(self.end_time))

		box = gui.widgetBox(self.controlArea, "Info")
		box.setAlignment(Qt.AlignCenter)
		self.info = gui.widgetLabel(box, 'Fill start and end time.')
		gui.separator(self.controlArea)

		self.field_layout = QGridLayout()
		gui.widgetBox(self.controlArea, margin=10, orientation=self.field_layout)
		start_time_label = QLabel("Start time: (seconds)")
		start_time_label.setFont(QFont("Helvetica", pointSize=11))
		start_time_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(start_time_label)
		self.field_layout.addWidget(self.baseline_start_field)

		end_time_label = QLabel("End time: (seconds)")
		end_time_label.setFont(QFont("Helvetica", pointSize=11))
		end_time_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(end_time_label)
		self.field_layout.addWidget(self.baseline_end_field)

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
		start = self.baseline_start_field.text().strip()
		end = self.baseline_end_field.text().strip()

		try:
			self.start_time = float(start)
			self.Error.start.clear()
		except ValueError:
			self.Error.start(start, str(self.start_time))

		try:
			self.end_time = float(end)
			self.Error.end.clear()
		except ValueError:
			self.Error.end(end, str(self.end_time))

	def baseline_correction(self):
		self.data.apply_baseline(baseline=(self.start_time, self.end_time), verbose=None)

	@Inputs.data
	def set_input_data(self, input_data):
		"""Initializes and modifies the input data and then sends the data on the output."""
		self.data = input_data
		if self.data is not None:
			self.data = self.data.copy()
			self.baseline_correction()
		self.commit()

	def commit(self):
		self.Outputs.data.send(self.data)


if __name__ == "__main__":
	WidgetPreview(OWBaselineCorrection).run()
