Ecoinvent 3 in Brightway2
#########################

:date: 2014-06-24 00:00
:category: math
:slug: multioutput
:summary: Ecoinvent 3 is now usable in Brightway2

.. figure:: images/friendship2.jpg
    :alt: Friendship by Trina Alexander (https://www.flickr.com/photos/paperdollimages/205857798)
    :align: center

    Friends at last

Version 1.0 of `Brightway2-data <https://bitbucket.org/cmutel/brightway2-data>`_ brings support for the `ecospold 2 data format <http://www.ecoinvent.org/data-providers/how-to-submit-data/ecospold2/>`_, and hence support for the system model-allocated versions of ecoinvent 3. Ecoinvent 3 master data (unallocated datasets) are not usable by, to my knowledge, anyone other than the ecoinvent centre - see my `earlier thoughts on an open source ecoinvent 3 linker <http://chris.mutel.org/open-source-ei3.html>`_.

Ecoinvent 3 system models
=========================

Brightway2 supports all three system models - default, consequential, and cutoff. However, each system model has its own quirks.

The details of each system model are described in detail by the ecoinvent centre.

* Cutoff: This is the newest system model, released only recently, and imports without any problems or known issues.
* Consequential: This system model imports cleanly, aside from the `known issues <http://www.ecoinvent.org/database/ecoinvent-version-3/reports-of-changes/known-data-issues/>`_.
* Default: In addition to the `known issues <http://www.ecoinvent.org/database/ecoinvent-version-3/reports-of-changes/known-data-issues/>`_, the process ``market for methane, 96% by volume, from biogas, low pressure, at user`` (file ``35603b32-0774-4805-ab0f-a446bfe989b8_df713085-e762-4edb-b02f-cc2b274ffab5.spold`` does not import cleanly. This activity links to flows which are not provided by their specified activities, and this activity is not imported cleanly in SimaPro 8.02 either.

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

With the coming release of ecoinvent 3.1, I will probably create a unified biosphere database and set of LCIA methods.

Caveats
=======

* Uncertainty data is not yet imported (this is on the todo list)
* Parameters are not imported
