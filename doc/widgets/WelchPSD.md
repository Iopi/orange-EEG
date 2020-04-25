Welch PSD
=========
Compute the power spectral density (PSD) using Welch’s method.


**Inputs**
- [Raw](https://mne.tools/0.17/generated/mne.io.Raw.html#mne.io.Raw)
- [Epochs](https://mne.tools/0.17/generated/mne.Epochs.html)
- [Evoked](https://mne.tools/0.17/generated/mne.Evoked.html)

**Outputs**
- (psds, freqs)
    - psds - The power spectral densities. 
    - freqs - The frequencies.

**Use**

![](images/welch1.png)

1. Start frequency - Min frequency of interest
2. End frequency - Max frequency of interest
3. Start time - Min time of interest
4. End time - Max time of interest
5. Number of points to use in Welch FFT calculations

Example
-------

![](images/exa8work.png)

![](images/exa8plot.png)

More information [here](https://mne.tools/0.17/generated/mne.time_frequency.psd_welch.html).

#### Related widgets

[Plot Welsch PSD](PlotWelchPSD.md)