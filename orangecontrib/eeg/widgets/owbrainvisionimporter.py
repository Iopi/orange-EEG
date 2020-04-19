import mne
from Orange.widgets import gui
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Output, Msg
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QPushButton, QGridLayout, QFileDialog, QLabel, QVBoxLayout
from PyQt5.QtWidgets import QSizePolicy as Policy
from PyQt5.QtGui import QFont
from orangecontrib.eeg.utils import style


class OWBrainVisionImporter(OWWidget):
	"""Orange widget that reads EEG data from a file selected by the user through GUI."""

	name = "BrainVision Importer"
	description = "Reads BrainVision data from a selected EEG file."
	icon = "icons/icon_owbrainvisionimporter.svg"
	priority = 10

	class Warning(OWWidget.Warning):
		no_file_selected = Msg("You didn't choose any file\n")

	class Information(OWWidget.Information):
		data_loaded = Msg("Data was successfully loaded.")

	class Error(OWWidget.Error):
		e_data_read = Msg("Unable to read data from {} file.")

	class Outputs:
		data = Output("Raw data", mne.io.Raw)

	want_main_area = False
	resizing_enabled = True

	def __init__(self):
		super().__init__()
		self.file_type = "EEG header files (*.vhdr)"
		self.file_path = None
		self.already_output = False
		self.data = None
		self.kind = 'standard_1020'

		# GUI
		box = gui.widgetBox(self.controlArea, "Info")
		self.info_file = gui.widgetLabel(box, "No file has been selected yet.")
		self.kind_field = style.create_field(str(self.kind))

		field_layout = QGridLayout()
		field_layout.setAlignment(Qt.AlignCenter)
		gui.widgetBox(self.controlArea, margin=10, orientation=field_layout)

		kind_label = QLabel("The name of the montage file.")
		kind_label.setFont(QFont("Helvetica", pointSize=11))
		kind_label.setAlignment(Qt.AlignCenter)
		field_layout.addWidget(kind_label)
		field_layout.addWidget(self.kind_field)

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignCenter)
		gui.widgetBox(self.controlArea, margin=10, orientation=layout)

		file_button = QPushButton("Choose an EEG header file")
		file_button.setStyleSheet(style.btn_primary)
		file_button.clicked.connect(self.choose_file)
		file_button.setSizePolicy(Policy.Maximum, Policy.Fixed)
		file_button.setMinimumSize(QSize(160, 25))
		layout.addWidget(file_button)

		self.reset_button = QPushButton("Reset")
		self.reset_button.setStyleSheet(style.btn_success)
		self.reset_button.clicked.connect(self.reset)
		self.reset_button.setSizePolicy(Policy.Maximum, Policy.Fixed)
		self.reset_button.setMinimumSize(QSize(160, 25))
		layout.addWidget(self.reset_button)

	def reset(self):
		"""Resets the data from the start."""
		self.Warning.clear()
		self.Information.clear()
		self.Error.clear()
		self.info_file.setText("No file has been selected yet.")
		self.file_path = None
		self.data = None
		self.already_output = False
		self.Outputs.data.send(self.data)

	def commit(self):
		"""Sends the read data on the output."""
		self.Outputs.data.send(self.data)
		self.already_output = True

	def read_file(self):
		"""Reads data from the selected file."""
		if not self.already_output:
			# TODO: Verbose setting for the command line output info
			self.data = mne.io.read_raw_brainvision(self.file_path, preload=True) #, stim_channel=False
			montage = mne.channels.read_montage(self.kind_field.text())	# added montage
			self.data.set_montage(montage, set_dig=True)
			if self.data is not None:
				self.Information.data_loaded()
				self.commit()
			else:
				self.Error.e_data_read(self.get_file_name(self.file_path))

	def choose_file(self):
		"""
		Shows a file chooser dialog to the user, where he can choose the EEG header file.
		The selected file is validated and if the file is valid, calls the `read_file` method.
		"""

		self.file_path = QFileDialog.getOpenFileName(self, "Choose a EEG header file", "/", self.file_type)[0]

		if self.is_valid_file(self.file_path):
			self.Warning.clear()
			# Displaying only the selected file name, not the whole path
			file_name = self.get_file_name(self.file_path)
			self.info_file.setText("Selected file: " + file_name)
			self.read_file()

	def get_file_name(self, file_path):
		"""Returns only the file name of the specified file path."""
		return file_path[file_path.rfind('/') + 1:]

	def is_valid_file(self, file_path):
		"""
		Checks if the specified file name is valid or not.
		If the file name is an empty string raises a warning indicating that the user didn't select any file.
		If the file has a valid extension returns true, otherwise returns false.
		"""
		if file_path == "":
			self.Warning.no_file_selected()
			return False

		extension = self.file_type[self.file_type.rfind('.'):self.file_type.rfind(')')]
		if extension in file_path:
			return True

		return False


if __name__ == "__main__":
	WidgetPreview(OWBrainVisionImporter).run()
