Support Vector Classification
=============================
C-Support Vector Classification

**Inputs**
- [numpy.ndarray][1]: Training data
- [numpy.ndarray][1]: Labels of training data
- [numpy.ndarray][1]: Target data
- [numpy.ndarray][1]: Labels of target data

**Outputs**
If classification is binary:
- *float*: accuracy
- *float*: recall
- *float*: precision

If classification is multi-class:
- *float*: accuracy


[1]: https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html

![](images/svc1.png)

1. Results - Here are displayed results: 
    - accuracy, recall and precision in binary classification
    - accuracy in multi-class classification
2. Random state - The seed of the pseudo random number generator to use when shuffling the data for the dual coordinate descent.
3. Max iter - The maximum number of iterations to be run.

Example
-------

![](images/exa12work.png)

![](images/exa12plot.png)

More information [here](https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html)

#### Related widgets

[EEG Marker](LDA.md)