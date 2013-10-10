Brightway2: Release 0.10
########################

:date: 2013-10-10 12:00
:category: brightway2
:slug: brightway2-0.10
:summary: Version 0.10 of Brightway2 brings a number of improvements and new features.

.. figure:: images/forward.jpg
    :alt: Disco dancers moving forward.
    :align: center

    Figure 1: Forward! Credit: `Barking at Strangers <http://www.flickr.com/photos/23245551@N00/3348326890/>`_.

Version 0.10 of Brightway2 was released during the `LCA XIII <http://lcacenter.org/LCAXIII.aspx>`_ conference in Orlando, Florida. This new release brings a number of small improvements and some new features. Here are the four big new features:

SimaPro import
--------------

Most versions of SimaPro can't export EcoSpold XML files, and therefore previously it wasn't possible to import projects built in SimaPro. However, even the basic versions of SimaPro can export CSV (comma-separated variable) files, and these can now be used.

The SimaPro importer can link to existing databases. For example, if you have already installed ecoinvent, you don't need to export it from SimaPro; Brightway2 will link your exported project to ecoinvent automatically. This is non-trivial as SimaPro screws up ecoinvent process names.

However, the importer has the following limits:

* Multioutput datasets are not supported.
* Uncertainty data is not imported.
* Social and economic flows are ignored.
* Linking against datasets other than ecoinvent is not tested (most are not available otherwise).
* Modifying an existing database is not supported; it can only be overwritten completely.
* SimaPro unit conversions will cause problems matching to background databases (e.g. if you specify an import in megajoules, and the ecoinvent process is defined in kWh, they won't match).

More documentation on the importer can be found in the `online docs <http://bw2data.readthedocs.org/en/latest/io.html#simapro>`_.

Data upgrading script
---------------------

Brightway2 doesn't have a database, but it does have an accepted format for storing data, and occasionally that will change. 0.10 brought two changes in the underlying format: one was new unit normalizations, needed because SimaPro changes ecoinvent units (!?), and a second was the transition to `transition to the stats_arrays <http://chris.mutel.org/stats-arrays.html>`_ library.

To make it easier than the `typical SimaPro upgrade instructions <www.pre-sustainability.com/.../SimaPro733DatabaseUpdateFrom732.pdf‎>`_, 0.10 introduces a new script, ``bw2-uptodate.py``. It is pretty easy to use:

*List any upgrades needed*

.. code-block:: bash

    bw2-updtodate.py --list

*Apply upgrades*

.. code-block:: bash

    bw2-updtodate.py

Any data that needs to be updated will be automatically backed up prior to making changes.

You only need to upgrade if you were using a version prior to 0.10.

If you have any needed updates, you will also be notified any time you use Brightway2.

Vector of parameters for Monte Carlo
------------------------------------

This might sound a bit technical or abstract, but is quite important for uncertainty and sensitivity analysis.

For each LCI database, LCIA method, normalization, and weighting, Brightway2 will store a separate file in an efficient binary format (`general docs <http://brightway2.readthedocs.org/en/latest/key-concepts.html#intermediate-and-processed-data>`_, `specific example <http://bw2data.readthedocs.org/en/latest/database.html#bw2data.Database.process>`_). These files are then used to build separate technosphere, biosphere, etc. matrices.

However, it is often more convenient to have one long list of stochastic parameters, which can be then analyzed and manipulated, for both uncertainty and sensitivity analysis. The 0.10 release introduces a class called ``ParameterVectorLCA``, which is actually `relatively simple <https://bitbucket.org/cmutel/brightway2-calc/src/08eb5438f3952ccbe275fa9d911c94216c2c210e/bw2calc/mc_vector.py?at=default>`_; it just combines all stochastic parameters into a large list, and provides convenience methods to extract these parameters back into LCA matrices.

In the future, this will make it much easier to write e.g.automatic sensitivity tools.

Weighting uncertainty
---------------------

Brightway2 has already had the ability to include stochastic LCIA characterization factors for a while; 0.10 adds stochastic weighting. `Stephan Pfister <http://www.ifu.ethz.ch/staff/stpfiste/index_EN>`_ and I are investigating the importance of weighting uncertainty using the LIME2 LCIA method.

The foundation for stochastic normalization was also introduced, but not implemented in any Monte Carlo class.

This code builds on earlier work prototyped in a separate blog post <http://chris.mutel.org/new-example-weighting-and-normalization.html>`_
