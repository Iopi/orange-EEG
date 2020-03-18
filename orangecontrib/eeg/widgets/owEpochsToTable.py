import mne
import numpy as np
from Orange.widgets import gui
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Msg
from Orange.data import Table, Domain, Variable, ContinuousVariable

class OWEpochsToTable(OWWidget):
	name = "Epochs to Table"
	description = "Converts mne.Epochs data to Orange.data.Table data."

	#icon = "icons/icon_owaveraging.svg"

	want_main_area = False
	resizing_enabled = True

	class Warning(OWWidget.Warning):
		no_epochs = Msg("No epochs with the input markers id exist in the input data.")

	class Inputs:
		data = Input("Epoch data", mne.Epochs)

	class Outputs:
		data = Output("Table data", Table)
	
	def __init__(self):
		super().__init__()
		box = gui.widgetBox(self.controlArea, "Epochs -> Table")
		box.setMinimumSize(80, 10)
		self.convert_info = gui.widgetLabel(box, "No epochs converted.")
	
	@Inputs.data
	def set_data(self, input_data):
		"""Sets the input data."""

		self.data = input_data
		if self.data is not None:
			array3d = self.data.get_data()
			events = self.data.events[:, 2]

			dim1 = len(array3d)
			dim3 = len(array3d[0][0])

			array2d = np.ndarray(shape=(dim3,dim1), dtype=float, order='F')

			for x in range(dim1):
				for y in range(dim3):
					array2d[y][x] = array3d[x][0][y]

			eventsVariable = [""] * len(events)
			for i in range(len(events)):
				eventsVariable[i] = ContinuousVariable.make(str(events[i]))

			domain = Domain(eventsVariable)

			self.data = Table(domain, array2d)
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
