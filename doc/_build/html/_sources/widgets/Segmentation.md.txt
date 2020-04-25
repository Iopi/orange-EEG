Segmentation
============
Segments epochs from raw data.

**Inputs**
- [Raw](https://mne.tools/0.17/generated/mne.io.Raw.html#mne.io.Raw)

**Outputs**
- [Epochs](https://mne.tools/0.17/generated/mne.Epochs.html): Partitioned Epochs to segments

**Use**

![](images/segm.png)

1. PreStimulus offset - Start time before event. 
2. PostStimulus offset - End time after event. 
3. Segment length - length of segment

Example
-------

![](images/exa10work.png)

![](images/exa10plot.png)

More information [here](https://mne.tools/0.17/generated/mne.Epochs.html).
