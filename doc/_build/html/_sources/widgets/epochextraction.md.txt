Epoch Extraction
================
Extracts specified epochs from the EEG data.

**Inputs**
- EEGMarker: Markers from widget [EEGMarker](eegmarker.md)
- [Raw](https://mne.tools/0.17/generated/mne.io.Raw.html#mne.io.Raw)

**Outputs**
- [Epochs](https://mne.tools/0.17/generated/mne.Epochs.html): Extracted Epochs

**Use**

![](images/etra.png)
1. *Markers* - If markers are added, extracted Epochs will be only Epochs with event-ID of added markers-ID.

2. PreStimulus offset - Start time before event. 
3. PostStimulus offset - End time after event. 

Example
-------

![](images/exa1work.png)

![](images/exa1plot.png)

More information [here](https://mne.tools/0.17/generated/mne.Epochs.html).

#### Related widgets

[EEG Marker](eegmarker.md)