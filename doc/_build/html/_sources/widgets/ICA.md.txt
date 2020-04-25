Independent Component Analysis
==============================
M/EEG signal decomposition using Independent Component Analysis (ICA).
ICA is sensitive to low-frequency drifts and therefore requires the data to be high-pass filtered prior to fitting. Typically, a cutoff frequency of 1 Hz is recommended.


**Inputs**
- [Raw](https://mne.tools/0.17/generated/mne.io.Raw.html#mne.io.Raw)
- [Epochs](https://mne.tools/0.17/generated/mne.Epochs.html)
- [Evoked](https://mne.tools/0.17/generated/mne.Evoked.html)

**Outputs**
- [ICA](https://mne.tools/0.17/generated/mne.preprocessing.ICA.html): Object of Independent Component Analysis

**Use**

![](images/ica1.png)

1. Number of components - Number of principal components that are passed to the ICA algorithm during fitting.
2. Random state - Random state to initialize ICA estimation for representativ results.
3. Maximum number of iterations - Maximum number of iterations during fit.


Example
-------

![](images/exa5work.png)

![](images/exa5plot1.png)

![](images/exa5plot2.png)

More information [here](https://mne.tools/0.17/generated/mne.preprocessing.ICA.html)
and [here](https://mne.tools/stable/auto_tutorials/preprocessing/plot_40_artifact_correction_ica.html#sphx-glr-auto-tutorials-preprocessing-plot-40-artifact-correction-ica-py).

#### Related widgets

[Plot ICA](PlotICA.md)