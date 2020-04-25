import mne
import numpy as np
from Orange.widgets import gui
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Msg
from Orange.data import Table, Domain, Variable, ContinuousVariable
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from orangecontrib.eeg.utils import style

class OWEpochsToTable(OWWidget):
	name = "Epochs to Table"
	description = "Converts mne.Epochs data to Orange.data.Table data."

	icon = "icons/icon_epoch_to_table.svg"

	want_main_area = False
	resizing_enabled = True

	class Error(OWWidget.Error):
		num_channel = Msg("{} is not a valid channel, continuing with {}.")

	class Warning(OWWidget.Warning):
		no_epochs = Msg("No epochs with the input markers id exist in the input data.")

	class Inputs:
		data = Input("Epoch data", mne.Epochs)

	class Outputs:
		data = Output("Table data", Table)
	
	def __init__(self):
		super().__init__()
		self.channel = 0
		self.channel_field = style.create_field(str(self.channel))


		box = gui.widgetBox(self.controlArea, "Epochs -> Table")
		#box.setMinimumSize(80, 10)
		self.convert_info = gui.widgetLabel(box, "No epochs converted.")

		self.info = gui.widgetLabel(box, 'Fill channel to convert.')
		gui.separator(self.controlArea)

		self.field_layout = QGridLayout()
		gui.widgetBox(self.controlArea, margin=10, orientation=self.field_layout)

		channel_label = QLabel("Channel to convert.")
		channel_label.setFont(QFont("Helvetica", pointSize=11))
		channel_label.setAlignment(Qt.AlignCenter)
		self.field_layout.addWidget(channel_label)
		self.field_layout.addWidget(self.channel_field)

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
		num_channel = self.channel_field.text().strip()

		try:
			self.channel = int(num_channel)
			self.Error.num_channel.clear()
		except ValueError:
			self.Error.num_channel(num_channel, str(self.channel))
	
	@Inputs.data
	def set_data(self, input_data):
		"""Sets the input data."""

		self.data = input_data
		if self.data is not None:
			print(np.shape(self.data))
			array3d = self.data.get_data()
			events = self.data.events[:, 2]

			dim1 = len(array3d)
			dim3 = len(array3d[0][0])

			array2d = np.ndarray(shape=(dim3,dim1), dtype=float, order='F')

			for x in range(dim1):
				for y in range(dim3):
					array2d[y][x] = array3d[x][self.channel][y]

			eventsVariable = [""] * len(events)
			for i in range(len(events)):
				eventsVariable[i] = ContinuousVariable.make(str(events[i]))

			domain = Domain(eventsVariable)

			self.data = Table(domain, array2d)
			print(np.shape(array2d))
			self.convert_info.setText("Epochs converted")

		else:
			self.amount_of_epochs = 0
			self.convert_info.setText("No epochs converted.")
			
		self.commit()

	def commit(self):
		"""Outputs the processed data."""

		self.Outputs.data.send(self.data)


if __name__ == "__main__":
	WidgetPreview(OWEpochsToTable).run()
