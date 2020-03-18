import mne
import copy
from Orange.widgets import gui
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Input, Output
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy

from EEGWorkflow.utils import style


class OWChannelSelector(OWWidget):
	"""
	Orange widget that selects certain channels, specified by the user through GUI, from the EEG data, that this widget
	receives as an input.
	"""

	name = "Channel Selector"
	description = "Removes all channels that are not selected from the data."

	icon = "icons/icon_owchannelselector.svg"

	class Inputs:
		data = Input("Raw data", mne.io.Raw)

	class Outputs:
		data = Output("Raw data", mne.io.Raw)

	want_main_area = False

	resizing_enabled = True

	def __init__(self):
		super().__init__()

		# Default settings for the widget
		self.default_channels = ["Pz", ""]
		self.fields = [style.create_field(self.default_channels[i]) for i in range(len(self.default_channels))]
		self.selected_channels = self.default_channels

		if __name__ == "__main__":
			data = mne.io.read_raw_brainvision("../data/LED_28_06_2012_104.vhdr", preload=True, stim_channel=True)
			self.set_input_data(data)
		else:
			self.data = None

		layout = QGridLayout()
		box = gui.widgetBox(self.controlArea, "Info", orientation=layout)
		box.setAlignment(Qt.AlignCenter)
		info = QLabel("Select the channels to keep in the data flow by typing out their names.\n"
		              "Channels are selected when data is input into this node.\n")
		note = QLabel("Note: empty fields will be ignored. Invalid channel names will also be ignored.")
		layout.addWidget(info)
		layout.addWidget(note)

		gui.separator(self.controlArea)

		self.field_layout = QGridLayout()
		gui.widgetBox(self.controlArea, margin=10, orientation=self.field_layout)
		label = QLabel("Channel names: ")
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
		save_btn.clicked.connect(self.save_names)
		save_btn.setStyleSheet(style.btn_success)
		save_btn.setMinimumSize(QSize(90, 25))
		save_btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
		layout.addWidget(save_btn)

	def save_names(self):
		ch_names = []
		for i in range(len(self.fields)):
			ch_name = self.fields[i].text()
			if ch_name != "":
				ch_names.append(ch_name)
		self.selected_channels = ch_names
		print(self.selected_channels)

	@Inputs.data
	def set_input_data(self, input_data):
		"""Initializes and modifies the input data and then sends the data on the output."""

		self.data = input_data
		if self.data is not None:
			self.data = self.data.copy()
			self.set_selected_channels()
			self.do_selection()
		self.commit()

	def do_selection(self):
		"""
		Modifies the data by dropping all of the channels that are not in the selected channels.
		Selected channels are specified by the user through GUI.
		"""

		# All of the channels that are not in the selected channels
		channels_to_remove = []
		for ch in self.data.ch_names:
			if ch not in self.selected_channels:
				if ch != "STI 014":
					channels_to_remove.append(ch)
		self.data = self.data.drop_channels(channels_to_remove)

	def commit(self):
		"""Sends the data on the output."""

		self.Outputs.data.send(self.data)

	def add_field(self):
		"""Adds a new text field to the field layout in the GUI. And calls the reorder_tabs function."""

		field = style.create_field()
		self.fields.append(field)
		self.field_layout.addWidget(field)
		self.reorder_tabs()

	def remove_field(self):
		"""
		Removes the last field in the field layout. Unless there is only one field.
		If the field text was a channel name stored in the selected channels list, removes that name from the list.
		"""

		if len(self.fields) != 1:
			field = self.fields.pop()
			channel = field.text().strip()
			if channel in self.selected_channels:
				self.selected_channels.remove(channel)
			field.setParent(None)

	def set_selected_channels(self):
		"""Adds all unique text from the text fields as a channel name to the selected channels."""

		self.selected_channels.clear()
		for field in self.fields:
			channel = field.text().strip()
			if channel is not "" and channel not in self.selected_channels:
				self.selected_channels.append(channel)

	def reorder_tabs(self):
		"""Creates a new tab order for the text fields."""

		for i in range(1, len(self.fields)):
			field = self.fields[i - 1]
			second_field = self.fields[i]
			field.setTabOrder(field, second_field)


if __name__ == "__main__":
	WidgetPreview(OWChannelSelector).run()
