New geospatial utility: ``pandarus``
####################################

:date: 2014-02-01 12:00
:category: brightway2
:slug: pandarus
:summary: A new geospatial utility for matching inventory and impact assessment spatial scales







A new way to work with and store uncertainty values
===================================================

.. figure:: images/numbers.png
    :alt: Numbers. Just some numbers. Really.
    :align: center

    Figure 1: Numbers. Credit: `eye/see <http://www.flickr.com/photos/17001563@N00/5846058698/>`_.

One of the few good ideas to come out of the original Brightway program (see `the technical motivation for Brightway2 <http://chris.mutel.org/brightway2-technical-motivation.html>`_) is the use of `parameter arrays <https://stats_arrays.readthedocs.org/en/latest/#parameter-array>`_, which store uncertain variable definitions in a NumPy array. This functionality was factored out into `bw_stats_toolkit <https://bitbucket.org/cmutel/bw-stats-toolkit>`_.

Today was the first release of `stats_arrays <https://pypi.python.org/pypi/stats_arrays/0.1alpha1>`_, which is the basically same thing, except only better. The core idea remains the same.

See `an example of the new library in action <http://nbviewer.ipython.org/url/brightwaylca.org/examples/stats-arrays-demo.ipynb>`_.

Here are the improvements:

* There is no need to transform values in the ``amount`` column when doing stochastic and non-stochastic sampling. Instead, there are separate ``amount`` and ``loc`` columns. This makes for simpler and easier to test code.
* There are now three columns for statistical parameters, allowing for more uncertainty distributions.
* Uncertainty fields now follow semi-standardized names: ``loc``, ``scale``, and ``shape``, instead of ``amount`` and ``sigma``.
* More uncertainty distributions.
* There is documentation and more complete tests.

Check out the `source code <https://bitbucket.org/cmutel/stats_arrays>`_ and `documentation <https://stats_arrays.readthedocs.org/en/latest/>`_.

Upgrading to ``stats_arrays``
=============================

Install ``stats_arrays`` using ``pip`` or another Python package manager. For most of you, this will mean:

.. code-block:: bash

    pip install stats_arrays

You will also need to upgrade ``bw2data`` and ``bw2calc``:

.. code-block:: bash

    pip install --upgrade --no-deps bw2calc bw2data

Then, run the following in a Python shell:

.. code-block:: python

    from bw2data.utils import convert_from_stats_toolkit
    convert_from_stats_toolkit()
