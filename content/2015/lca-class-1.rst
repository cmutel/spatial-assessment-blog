2015 advanced LCA seminar
#########################

:date: 2015-11-02 00:00
:category: lca-seminar
:slug: 2015-class-1
:summary: The 2015 advanced LCA seminar

Advanced LCA Seminar
====================

I teach a PhD-level seminar at `ETH Zürich <https://www.ethz.ch/en.html>`__ every fall semester. Because we focus on advanced life cycle assessment, the class is imaginatively called "Advanced LCA seminar". In 2013, we looked at ecoinvent version 3, and in particular at the `data quality guidelines <http://www.ecoinvent.org/files/dataqualityguideline_ecoinvent_3_20130506.pdf>`__. In 2014, we covered dynamic (temporal) LCA and regionalization. This year, we will look at complex and integrated assessments.

As part of my work at the `laboratory for energy systems analysis <http://www.psi.ch/lea/>`__ at the `Paul Scherrer Institute <http://www.psi.ch/>`__, we are assisting the energy transition in Switzerland by assessing current and future energy and mobility technologies. However, we recognize that individual case studies provide only limited information to decision makers, as they don't provide the full systems context. For example, an LCA of a new electricity storage technology is essentially meaningless unless it includes the increases in renewable energy that are made possible by the specific characteristics of its storage system. Similarly, we can develop detailed models of current and future transportation systems, but need an understanding of how housing patterns and the electricity grid will evolve to make a complete assessment. Thus, the 2015 course will be focused on complex and integrated systems.

The goal this year is to make a small toy model in each class session (the class meets every two weeks, for two hours), to demonstrate some aspect of how LCA can be integrated into a more complete systems analysis. The syllabus will evolve, based on how well each class works, but the topics will probably be:

#. Introduction. Installation of BW2. Initial calculations.
#. Optimization. Simple optimizer in Python.
#. Machine learning. Classification and feature selection.
#. Sensitivity. Local and global sensitivity, probably based on a simple physical model of a car.
#. Assessing large systems. Processing data from `Matsim <http://www.matsim.org/>`__.
#. Integration. `Calliope <http://www.callio.pe/>`__.
#. Economic models. IO tables (EXIOBASE). Filling in the holes from ecoinvent.

The order for classes is not finalized, and will depend on how the seminar progresses.

Online and open classes
=======================

My intention is to make all data and code used in the course open, and published online in this blog. We will use the ecoinvent database, which is a pretty big exception to the previous statement, as it is not freely available, but I don't see a way around this rather glaring contradiction for now. Unfortunately, the few free life cycle inventory databases are not good enough for what we want to do.

Each class with follow a `Jupyter notebook <https://jupyter.org/>`__. You can download the `current set of notebooks <http://brightwaylca.org/data/LCA%20seminar%202015%20notebooks.zip>`__. Note that the notebooks will require `Brightway2 <http://brightwaylca.org/>`__; please follow the `installation guide <http://brightwaylca.org/dev-docs/installation.html>`__.

Running the notebook server
---------------------------

The easiest way to open the notebooks on Windows is to drag a copy of the ``bw2-notebook.bat`` script from ``C:\bw2-python\`` to wherever you extracted the notebooks, and then to run the script. On OS X, enter the following into the Terminal:

.. code-block:: bash

    source ~/bw2-python/bin/activate bw2
    cd path/to/extracted/folders
    jupyter notebook

Class 1 - Introduction
======================

`Class 1 notebook <http://nbviewer.ipython.org/urls/bitbucket.org/cmutel/brightway2/raw/2.0/notebooks/2015%20LCA%20Seminar%20-%20Class%201%20-%20Introduction.ipynb>`__

This class will introduce LCA and Brightway2. Don't forget to set up a notebooks directory after doing the basic installation.

In this class, we will follow notebook 1, which you should download and open now (see link above). Note that we are using version 2.2 of ecoinvent because we are doing the exercise in class, and importing and calculating with 2.2 is faster than with 3.x.

Class 2 - Optimization
======================

`Class 2 notebook <http://nbviewer.ipython.org/urls/bitbucket.org/cmutel/brightway2/raw/2.0/notebooks/2015%20LCA%20Seminar%20-%20Class%202%20-%20Optimization.ipynb>`__

In this class, we construct a basic agent model of transport choices, and then do basic optimization for different criteria using `Scipy optimize <http://docs.scipy.org/doc/scipy/reference/optimize.html>`__.

Class 3 - Classification
========================

`Class 3 notebook <http://nbviewer.ipython.org/urls/bitbucket.org/cmutel/brightway2/raw/2.0/notebooks/2015%20LCA%20Seminar%20-%20Class%203%20-%20Clustering.ipynb>`__

In this class we link a physics model of motorcycle dynamics with ecoinvent, and use a few of the functions from `scikit-learn <http://scikit-learn.org/>`__ to classify the motorcycles in our database.

Class 4 - Hybrid LCA
====================

`Class 4 notebook <http://nbviewer.ipython.org/urls/bitbucket.org/cmutel/brightway2/raw/2.0/notebooks/2015%20LCA%20Seminar%20-%20Class%204%20-%20Hybrid%20LCA.ipynb>`__

In this class we will import the `EXIOBASE 2.2 <http://exiobase.eu/>`__ industry by industry IO tables, and explore what hybrid LCA is and how it works.

Class 5 - Integration with transport modelling
==============================================

Class 5 includes some data, `so is available here <http://brightwaylca.org/data/class5.zip>`__.

Class 6 - Energy system modelling
=================================

Class 6 includes even more data, `so is available here <http://brightwaylca.org/data/class6.zip>`__.

Class 7 - Sensitivity analysis
==============================

Class 7 builds on class 5, and assumes you have have the data files available. It can be `viewed or downloaded here <http://nbviewer.ipython.org/urls/bitbucket.org/cmutel/brightway2/raw/2.0/notebooks/2015%20LCA%20Seminar%20-%20Class%207%20-%20Sensitivity%20analysis.ipynb>`__
