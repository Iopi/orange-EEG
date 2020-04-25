Discrete wavelet tranformation
==============================

Transformation derived from wavelet transform for discrete wavelets. Computes approximation and deail coefficient.

**Inputs**

- [Epochs](https://mne.tools/0.17/generated/mne.Epochs.html)

**Outputs**

- [numpy.ndarray][1]: Approximation coefficient
- [numpy.ndarray][1]: Detail coefficient

[1]: https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html

**Use**

![](images/dwt1.png)

1. Wavelet family - wawelet to use
2. Number of degrees of transformation

Example
-------

![](images/exa9work.png)

![](images/exa9plot.png)

More information [here](https://pywavelets.readthedocs.io/en/latest/ref/dwt-discrete-wavelet-transform.html)
