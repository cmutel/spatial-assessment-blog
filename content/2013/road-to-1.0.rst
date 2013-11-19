The road to 1.0
###############

:date: 2013-10-15 12:00
:category: brightway2
:slug: road-to-10
:summary: There is a clear path to version 1.0 of Brightway2.

.. figure:: images/rolling-road.jpg
    :alt: Rolling road.
    :align: center

    Figure 1: Rolling Road. Credit: `Michael Krigsman <http://www.flickr.com/photos/42246573@N00/2852232536/>`_.

`Brightway2 <brightwaylca.org>`_ has made enormous progress since the first commit on November 20, 2012. The current version is 0.10, and includes the foundation for work far into the future. There are a few big things and a number of small things that need to get finished before version 1.0 can be released, however.

Brightway2 uses `semantic versioning <http://semver.org/>`_, so reaching 1.0 is a big deal. To be more specific:

    Version 1.0.0 defines the public API. The way in which the version number is incremented after this release is dependent on this public API and how it changes.

This means that it is difficult to make substantial changes, as software building on top of Brighway2 will expect certain interfaces and patterns.

Major features
--------------

Database and method explorer
============================

Status: **finished!**

There is now the following:

* `Activity browser CLI application <https://www.youtube.com/watch?v=Dw3s5K8OsM0>`_.
* Clickable activyt and method webpages with `new datatable implementation <https://bitbucket.org/cmutel/brightway2-ui/issue/2/new-data-table>`_ based on `backgrid <http://backgridjs.com/>`_.
* Raw activity and method JSON data display built on a `very cool json editor <http://www.jsoneditoronline.org/>`_.

Reworked treemap
================

Status: **Almost finished**. Just need to make hover elements outside the box, to eliminate flicker.

The current treemap is a decent start of an idea, but as a released graphic it sucks. It can be interactive, hierarchical, and (thanks to the idea of `Pascal Lesage <http://www.polymtl.ca/recherche/rc/en/professeurs/details.php?NoProf=551>`_), include biosphere flows and their associated uncertainties.

See progress at `online example 1 <http://tributary.io/inlet/4951698>`_ and `online example 2 <http://tributary.io/inlet/6960672>`_. There is also an `associated bug report <https://bitbucket.org/cmutel/brightway2-ui/issue/3/massively-improve-treemap>`_.

Graph traversal improvements
============================

Status: **Good progress**. Commit `d52549 <https://bitbucket.org/cmutel/brightway2-analyzer/commits/d52549f2f75dffc4e8d84f9e92612241654b7beb>`_ added all the basic machinery needed, including lots of tests!

The graph traversal class has undergone some serious work, both in additional tests and documentation, and in organization. However, final touches are needed for simplification and graph unrolling functions.

Graph traversal is useful, among other things, for better treemaps and `supply chain circles <http://tributary.io/inlet/4567531>`_.

Minor features
--------------

* Set all preferences in the web UI
* All documentation should be checked to make sure they are current
* More notebook examples
* New homepage with emphasis on framework aspects

Dreaming of 2.0
===============

Getting to 1.0 means the start of planning for 2.0. Here are the major features I am currently thinking of for 2.0.

* Compatibility with Python 3. Python 3 is `already at 3.4 <http://www.python.org/download/releases/3.4.0/>`_, and all major Brightway2 dependencies are Python 3 compatible.
* Pluggable data backend. Using a simple database, like `SQLite 3 <http://www.sqlite.org/>`_ or `CodernityDB <http://labs.codernity.com/codernitydb/index.html>`_ would make random access into inventory databases, and especially big databases like ecoinvent 3, much faster.
* Addition modules, most notably sensitivity analysis and regionalization.
