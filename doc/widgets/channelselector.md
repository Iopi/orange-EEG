Channel Selector
================
Selects certain channels, specified by the user through GUI, from the EEG data, that this widget receives as an input.


**Inputs**
- [Raw](https://mne.tools/0.17/generated/mne.io.Raw.html#mne.io.Raw)

**Outputs**
- [Raw](https://mne.tools/0.17/generated/mne.io.Raw.html#mne.io.Raw): Raw with selected channels

**Use**

![](images/sele1.png)

1. Channel names - Channel names you want to select
2. Add Button - Adds additional empty field for channel
3. Remove Button - Removes last field for channel
4. Save Button - Saves selected channels

Example
-------

![](images/exa1work.png)

![](images/exa1plot.png)


More information [here](https://mne.tools/0.17/generated/mne.io.Raw.html#mne.io.Raw.drop_channels)