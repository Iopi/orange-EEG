Filter
======
Filter a subset of channels.


**Inputs**
- [Raw](https://mne.tools/0.17/generated/mne.io.Raw.html#mne.io.Raw)
- [Epochs](https://mne.tools/0.17/generated/mne.Epochs.html)
- [Evoked](https://mne.tools/0.17/generated/mne.Evoked.html)

**Outputs**
- [Raw](https://mne.tools/0.17/generated/mne.io.Raw.html#mne.io.Raw): Filtered Raw
- [Epochs](https://mne.tools/0.17/generated/mne.Epochs.html): Filtered Epochs
- [Evoked](https://mne.tools/0.17/generated/mne.Evoked.html): Filtered Evoked

**Use**

![](images/fil1.png)

1. The lower pass-band edge - Low cut-off frequency in Hz.
2. The upper pass-band edge - High cut-off frequency in Hz.


Example
-------

![](images/exa5work.png)

More information filter in Raw [here](https://mne.tools/0.17/generated/mne.io.Raw.html#mne.io.Raw.filter).
More information filter in Epochs [here](https://mne.tools/0.17/generated/mne.Epochs.html#mne.Epochs.filter).
More information filter in Evoked [here](https://mne.tools/0.17/generated/mne.Evoked.html#mne.Evoked.filter).