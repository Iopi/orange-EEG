from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QLineEdit, QSizePolicy

btn_primary = "QPushButton {color: #fff; background-color: #007bff;text-align:center; vertical-align:middle; border: " \
              "1px solid black; font-size: 1rem; padding: .375 rem .75rem; border-radius: 4px;} " \
              "QPushButton:hover { background-color: #0069d9;}" \
              "QPushButton:focus {border: 1px solid #80bdff; outline:none;}" \
              "QPushButton:pressed {border: 2px solid #083f7a; outline:none;}"

btn_warning = "QPushButton {color: black; background-color: #ffc107; text-align:center; " \
              "vertical-align:middle; border: 1px solid black; font-size: 1rem; " \
              "padding: .375 rem .75rem; border-radius: 4px;}" \
              "QPushButton:hover {background-color: #e0a800;}" \
              "QPushButton:focus {border: 1px solid #b28603; outline:none;}" \
              "QPushButton:pressed {border: 2px solid #c69500; outline:none;}"

field = "QLineEdit {border: 1px solid gray; border-radius: 5px; font-size: 13px; color: black;}" \
        "QLineEdit:focus {border: 2px solid #80bdff;}"

btn_success = "QPushButton {color: #fff; background-color: #5cb85c;text-align:center; vertical-align:middle; border: " \
              "1px solid black; font-size: 1rem; padding: .375 rem .75rem; border-radius: 4px;} " \
              "QPushButton:hover { background-color: #449d44;}" \
              "QPushButton:focus {border: 1px solid #255625; outline:none;}" \
              "QPushButton:pressed {border: 2px solid #398439; outline:none;}"


def create_field(text="", width=120, height=20, style=field):
	"""Creates a new text field with the specified text and returns it."""

	f = QLineEdit(text)
	f.setStyleSheet(style)
	f.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
	f.setMaximumSize(QSize(width, height))
	return f
