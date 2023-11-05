Brightway ♥️ Dataframes
#######################

:date: 2022-08-21-12:00
:category: brightway
:slug: brightway-dataframes
:summary: Consistent support for dataframes across Brightway
:status: draft

.. figure:: /images/robot-frame.jpg
    :align: center
    :alt: Robot inside a (data?) frame

There has been ad hoc support for converting various data or calculation results in Brightway to pandas dataframes for a while, mostly contributed by `outside Brightway authors <https://2.docs.brightway.dev/credits.html?highlight=authors#authors>`__. In the latests releases of `bw2data` and `bw2calc`, we now have a consistent set of methods which handle edge cases and both main database backends. This post goes through how to use this new functionality, and helps avoid some gotchas of the current implementation. There is also a Jupyter notebook `demonstrating this functionality <https://github.com/brightway-lca/brightway2/blob/master/notebooks/to_dataframe%20demonstration.ipynb>`__.

SQLite `Database` methods
=========================

