Averaging Time Windows
======================
Computes arithmetic mean in defined time areas.

**Inputs**
- [Epochs](https://mne.tools/0.17/generated/mne.Epochs.html)

**Outputs**
- [numpy.ndarray](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html): Result 3D array in format [epochs, channels, ranges]

**Use**

![](images/avetw.png)

1. Time range - Time range for one time window
2. Add Button - Adds additional empty field for time range
3. Remove Button - Removes last field for time range
4. Save Button - Saves time range

Example
-------

![](images/exa12work.png)

![](images/exa12plot.png)
