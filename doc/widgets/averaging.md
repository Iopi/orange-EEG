Averaging
=========
Averages the epoch data based on the stimuli markers


**Inputs**

- [Epochs][1]
- EEGMarker: Markers from widget [EEGMarker](eegmarker.md)

**Outputs**

- [Evoked](https://mne.tools/0.17/generated/mne.Evoked.html): The averaged epochs.

[1]: https://mne.tools/0.17/generated/mne.Epochs.html

**Use**

![](images/ave2.png)

If there are markers on the input, their name will be shown and after the averaging process the network number of epochs averaged will be displayed.

Example
-------

![](images/exa2work.png)

![](images/exa2plot.png)

More information [here](https://mne.tools/0.17/generated/mne.Epochs.html#mne.Epochs.average).

#### Related widgets

[EEG Marker](eegmarker.md)