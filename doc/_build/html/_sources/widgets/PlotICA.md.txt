PlotICA
=======
Plot the Independent Component Analysis.


**Inputs**
- One of [Raw](https://mne.tools/0.17/generated/mne.io.Raw.html#mne.io.Raw),
  [Epochs](https://mne.tools/0.17/generated/mne.Epochs.html) or
  [Evoked](https://mne.tools/0.17/generated/mne.Evoked.html)

and
- [ICA](https://mne.tools/0.17/generated/mne.preprocessing.ICA.html): Object of Independent Component Analysis

**Use**

![](images/icaplot1.png)

1. Sources - If this check box is checked, the Sources plot will be displayed after pressing *Show plot*.
2. Components - If this check box is checked, the Components plot will be displayed after pressing *Show plot*.
3. Show plot button - Button for showing plots.


Example
-------

![](images/exa5work.png)

![](images/exa5plot1.png)

![](images/exa5plot2.png)

More information about [plot sources](https://mne.tools/0.17/generated/mne.preprocessing.ICA.html#mne.preprocessing.ICA.plot_sources), [plot components](https://mne.tools/0.17/generated/mne.preprocessing.ICA.html#mne.preprocessing.ICA.plot_components) and [ICA](https://mne.tools/0.17/generated/mne.preprocessing.ICA.html).
Information about all process [here](https://mne.tools/stable/auto_tutorials/preprocessing/plot_40_artifact_correction_ica.html#sphx-glr-auto-tutorials-preprocessing-plot-40-artifact-correction-ica-py).

#### Related widgets

[ICA](ICA.md)