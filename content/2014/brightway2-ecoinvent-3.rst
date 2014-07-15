Ecoinvent 3 in Brightway2
#########################

:date: 2014-06-24 00:00
:category: brightway2
:slug: ecoinvent3
:summary: Ecoinvent 3 is now usable in Brightway2

.. figure:: images/friendship2.jpg
    :alt: Friendship by Trina Alexander (https://www.flickr.com/photos/paperdollimages/205857798)
    :align: center

    Friends at last

Version 1.0 of `Brightway2-data <https://bitbucket.org/cmutel/brightway2-data>`_ brings support for the `ecospold 2 data format <http://www.ecoinvent.org/data-providers/how-to-submit-data/ecospold2/>`_, and hence support for the system model-allocated versions of ecoinvent 3. Ecoinvent 3 master data (unallocated datasets) are not usable by, to my knowledge, anyone other than the ecoinvent centre - see my `earlier thoughts on an open source ecoinvent 3 linker <http://chris.mutel.org/open-source-ei3.html>`_.

Ecoinvent 3 system models
=========================

.. note:: Updated for ecoinvent 3.1

Brightway2 supports all three system models - default, consequential, and cutoff. The `known issues <http://www.ecoinvent.org/database/ecoinvent-version-3/reports-of-changes/known-data-issues/>`_ seem to all be resolved, though 3.1 introduces a few small issues itself (two steps forward, one step back, and all that). As in 3.01, the "cutoff" system imports with no linking problems; both "consequential, longterm" and "default" have a few linking problems.

Importing Ecoinvent 3
=====================

The complete database can be downloaded from the ecoinvent website, in "files" (https://ecoquery.ecoinvent.org/File/Files - must be logged in)

Extracting the ecoinvent archives should give two subfolders - master data, and the process datasets. The absolute paths to each will need to be provided. Importing works like this:

.. code-block:: python

    from bw2data.io import Ecospold2Importer
    Ecospold2Importer(
        datapath="/path/to/extracted/archive/datasets",
        metadatapath="/path/to/extracted/archive/MasterData",
        name="ecoinvent 3.01 system-model-type"
    ).importer()

Importing ecoinvent 3 will create a new biosphere database, called ``biosphere3``.

Because the import ecoinvent 3 consumes a lot of memory, you should probably reset your python process or ipython notebook after import.

Impact assessment methods
=========================

The existing LCIA method only link to the default ``biosphere`` database. New LCIA methods need to be installed to calculate LCA results using ecoinvent 3:

.. code-block:: python

    from bw2data.io import BW2Package
    from bw2data.utils import download_file
    BW2Package.import_file(download_file("lcia-ecoinvent3.bw2package"))

These new methods have the same name as the previous methods, with the addition of ``ecoinvent3`` at the end, e.g. ``('IPCC 2007', 'climate change', 'GWP 100a')`` becomes ``('IPCC 2007', 'climate change', 'GWP 100a', 'ecoinvent3')``.

I am still deciding the best way to handle the different ways of identifying biosphere flows (ecoinvent 2 versus 3), so for the time being there will be two different databases. The problem with just smashing the two databases together is that one would have the same dataset represented by two different identifiers, which could be problematic in many ways.

Caveats
=======

* Uncertainty data is not yet imported (this is on the todo list)
* Parameters are not imported
