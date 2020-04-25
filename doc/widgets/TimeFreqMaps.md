Time Frequency Maps
===================
Plot time-frequency maps.


**Inputs**
- One of [Epochs](https://mne.tools/0.17/generated/mne.Epochs.html) and
  [Evoked](https://mne.tools/0.17/generated/mne.Evoked.html)

**Output**
Time-Frequency Map

**Use**

![](images/tfmap.png)

1. freq - The frequencies in Hz.
2. n_cycles - The number of cycles globally or for each frequency. If *n_cycles* is 'scale' n_cycle = freqs / 2.
3. baseline a - Start of the time interval to apply baseline correction.
4. baseline b - End of the time interval to apply baseline correction.
5. mode - Mode to perform baseline correction.
  Possibilities:
    - *mean* - subtracting the mean of baseline values

    - *ratio* - dividing by the mean of baseline values 

    - *logratio* - dividing by the mean of baseline values and taking the log 

    - *percent* - subtracting the mean of baseline values followed by dividing by the mean of baseline values

    - *zscore* - subtracting the mean of baseline values and dividing by the standard deviation of baseline values 

    - *zlogratio* - dividing by the mean of baseline values, taking the log, and dividing by the standard deviation of log baseline values

6. channel - Channel which TF should be ploted
7. Plot TF of channel - If this check box is checked, the Time-Frequency of channel will be displayed after pressing *Show plot*.
8. Plot topography - If this check box is checked, the topography will be displayed after pressing *Show plot*.
9. Save button - Saves changes
10. Show plot button - Button for showing plots.


Example
-------

![](images/exa11work.png)

![](images/exa11plot1.png)

![](images/exa11plot2.png)

Where **Figure 1** is *TF of channel* and **Figure 2** is *topography*.

More information about [plot TF of channel](https://mne.tools/0.17/generated/mne.time_frequency.AverageTFR.html#mne.time_frequency.AverageTFR.plot) and [plot topography](https://mne.tools/0.17/generated/mne.time_frequency.AverageTFR.html#mne.time_frequency.AverageTFR.plot_topo).
Information about container for Time-Frequency data [here](https://mne.tools/0.17/generated/mne.time_frequency.AverageTFR.html).

