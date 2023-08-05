.. vfi documentation master file, created by
   sphinx-quickstart on Tue Nov 19 00:45:37 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to vfi's documentation!
===============================

The vfi package implements a variant of a determnistic machine learning method
which is called classification by Voting Feature Intervals [1]_, VFI in short.
VFI is a supervised classification method that constuct intervals around
each class for each feature. Class counts are recorded for each interval on
each feature and the classification is performed using a voting scheme.

.. [1] G. Demiroz, A. Guvenir: Classification by voting feature intervals. 
        In: 9th European Conference on Machine Learning, 85-92, 1997.01.



------------------
How to use VFI
------------------

The vfi package inherits from sklearn classes, and thus drops in neatly
next to other sklearn classifiers with an identical calling API. Similarly it
supports input in a variety of formats: an array (or pandas dataframe) of
shape ``(num_samples x num_features)``.

.. code:: python

    import vfi
    from sklearn.datasets import load_iris
    
    data, target = load_iris(return_X_y=True)
    
    model = vfi.VFI()
    model.fit(data, target)


.. toctree::
    :maxdepth: 1

    installation_guide
    auto_examples/index
    api
    benchmark

