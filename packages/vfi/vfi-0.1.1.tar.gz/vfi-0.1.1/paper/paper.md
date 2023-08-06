---
title: '``vfi``: Classification by Voting Feature Intervals in Python'
tags:
 - classification
 - supervised learning
 - discretization
 - machine learning
 - data mining
authors:
 - name: Christos K. Aridas
   orcid: 0000-0002-5021-1442
   affiliation: "1, 2"
affiliations:
 - name: Computational Intelligence Laboratory, Department of Mathematics, University of Patras
   index: 1
 - name: Code4Thought P.C.
   index: 2
date: 31/12/2019
bibliography: paper.bib
---

# Summary

``vfi`` is a Python package that mainly implements a method that is called 
classficaition by Voting Feature Intervals, in short ``VFI``. ``VFI`` is a method that was 
created by @demiroz1997 in order to cope with supervised classification problems 
and it was only avaliable in the Weka platform [@hall2009]. The proposed approach similarly 
to ``Naive Bayes`` in the sense that works independently on each feature. Constucts intervals 
around each class for each feature. Class counts are recorded for each interval 
on each feature and the classification is performed using a voting scheme. The 
vfi package provides a drop-in replacement class for ``scikit-learn`` [@pedregosa2011] 
compatible estimators. The proposed implementation differs from the original 
implementation in two folds. Firstly, it gives the ability to the user to define the 
number of the bins for the discretization of each feature, as well as the 
automatic method that is proposed in the original paper. Secondly, it gives the 
ability to the user to select the strategy of the discretization process among 
``uniform``, ``quantile`` and ``kmeans`` strategies in contrast to the proposed paper where 
the strategy that is used is the ``uniform``. ``VFI`` has over 200 citations in the scientific
literature, is a surprisingly very fast algorithm and performs very well in most 
of the cases.


# References
  