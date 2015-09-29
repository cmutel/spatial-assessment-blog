LCA seminar - Introduction and class 1
######################################

:date: 2015-09-22 00:00
:category: lca-seminar
:slug: 2015-class-1
:summary: Introduction to the advanced LCA seminar class

Advanced LCA Seminar
====================

I teach a PhD-level seminar at `ETH Zürich <https://www.ethz.ch/en.html>`__ every fall semester. Because we focus on advanced life cycle assessment, the class is imaginatively called "Advanced LCA seminar". In 2013, we looked at ecoinvent version 3, and in particular at the `data quality guidelines <http://www.ecoinvent.org/files/dataqualityguideline_ecoinvent_3_20130506.pdf>`__. In 2014, we covered dynamic (temporal) LCA and regionalization. This year, we will look at complex and integrated assessments.

As part of my work at the `laboratory for energy systems analysis <http://www.psi.ch/lea/>`__ at the `Paul Scherrer Institute <http://www.psi.ch/>`__, we are assisting the energy transition in Switzerland by assessing current and future energy and mobility technologies. However, we recognize that individual case studies provide only limited information to decision makers, as they don't provide the full systems context. For example, an LCA of a new electricity storage technology is essentially meaningless unless it includes the increases in renewable energy that are made possible by the specific characteristics of its storage system. Similarly, we can develop detailed models of current and future transportation systems, but need an understanding of how housing patterns and the electricity grid will evolve to make a complete assessment. Thus, the 2015 course will be focused on complex and integrated systems.

The goal this year is to make a small toy model in each class session (the class meets every two weeks, for two hours), to demonstrate some aspect of how LCA can be integrated into a more complete systems analysis. The syllabus will evolve, based on how well each class works, but the topics will probably be:

#. Introduction. Installation of BW2. Initial calculations.
#. Optimization. Simple optimizer in Python.
#. Sensitivity. Local and global sensitivity, probably based on a simple physical model of a car.
#. Machine learning. Classification and feature selection.
#. Assessing large systems. Processing data from `Matsim <http://www.matsim.org/>`__.
#. Integration. Field trip to P2G. `Calliope <http://www.callio.pe/>`__.
#. Economic models. IO tables (EXIOBASE). Filling in the holes from ecoinvent.

The order for classes 4-7 is not finalized, and will depend on how classes 1-3 go.

Online and open classes
=======================

My intention is to make all data and code used in the course open, and published online in this blog. We will use the ecoinvent database, which is a pretty big exception to the previous statement, as it is not freely available, but I don't see a way around this rather glaring contradiction for now. Unfortunately, the few free life cycle inventory databases are not good enough for what we want to do.

Class 1
=======

This class will introduce LCA, and we will follow the `installation guide <http://brightwaylca.org/dev-docs/installation.html>`__ for Brightway2. Don't forget to set up a notebooks directory after doing the basic installation.

In this class, we will follow `notebook 1 - introduction <http://nbviewer.ipython.org/urls/bitbucket.org/cmutel/brightway2/raw/2.0/notebooks/2015%20LCA%20Seminar%20-%20Class%201%20-%20Introduction.ipynb>`__, which you should download and open now. Note that we are using version 2.2 of ecoinvent because we are doing the exercise in class, and importing and calculating with 2.2 is faster.
