LSL Data Receiver
=================
Receives EEG LSL data.


**Inputs**
- Online data streams
- Online markers stream

**Outputs**
- [Raw](https://mne.tools/0.17/generated/mne.io.Raw.html#mne.io.Raw)

**Use**

![](images/lsl1.png)

1. Streams settings - settings for data and markers 
2. Timeout - Optionally a timeout of the operation, in seconds. If the timeout expires, less than the desired number of streams (possibly none) will be returned. (default FOREVER)
3. Save stream settings button - saves the *Streams settings* changes
4. Find streams button - Starts with findings streams with data and markers
5. Send data button - Sends found data to workflow (as output Raw)
6. Stop button - Stop data finding

Example
-------

![](images/exa6work.png)