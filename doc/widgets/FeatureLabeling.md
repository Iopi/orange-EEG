Feature Labeling
================
Labels epochs' data according to its events.

**Inputs**

- [Epochs](https://mne.tools/0.17/generated/mne.Epochs.html)
- EEGMarker: Markers from widget [EEGMarker](eegmarker.md)

**Outputs**

- [numpy.ndarray][1]: Vector of data
- [numpy.ndarray][1]: Labels of data

[1]: https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html

**Use**

![](images/feat.png)

*Markers* - If there are markers on the input, their name will be shown.

Example
-------

![](images/exa9work.png)

![](images/exa9plot.png)

#### Related widgets

[EEG Marker](eegmarker.md)