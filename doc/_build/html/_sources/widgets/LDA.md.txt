Linear Discriminant Analysis
============================
A classifier with a linear decision boundary.

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

**Use**

![](images/lda1.png)

1. Results - Here are displayed results: 
    - accuracy, recall and precision in binary classification
    - accuracy in multi-class classification
2. solver - Solver to use, possible values:
    - *svd*: Singular value decomposition.
    - *lsqr*: Least squares solution, can be combined with shrinkage.
    - *eigen*: Eigenvalue decomposition, can be combined with shrinkage.
3. shrinkage
    - None: no shrinkag.
    - *auto*: automatic shrinkage using the Ledoit-Wolf lemma.
    - float between 0 and 1: fixed shrinkage parameter.
    Note that shrinkage works only with *lsqr* and *eigen* solvers.


Example
-------

![](images/exa9work.png)

![](images/exa9plot.png)

More information [here](https://scikit-learn.org/stable/modules/generated/sklearn.discriminant_analysis.LinearDiscriminantAnalysis.html)

#### Related widgets

[EEG Marker](SVC.md)