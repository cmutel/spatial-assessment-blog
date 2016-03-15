Defining inventory models in Brightway2
#######################################

:date: 2016-03-08 00:00
:category: inventory
:slug: inventory-models
:summary: Thinking about how to define inventory models in Brightway2 leads directly to questions about the goals and struggles of Brightway2 itself.

.. figure:: images/intherain.jpg
    :alt: I give up being creative, here is a picture of one of my kids
    :align: center

    Figure 1: Cheer up, it's not that bad!

I am often asked how to build inventory models in Brightway2. This is actually a difficult question to answer, as Brightway2 doesn't have the same workflow as most other LCA software. There is no *one way* to build an inventory model. Instead, you can use a variety of data sources and programs to describe inventory models. This flexibility is very helpful when you are trying new ideas, or integrating with existing programs; however, it also makes getting started with Brightway2 more complicated. In this blog post, I will try to outline some of the ways I build and use inventory models, and hope to provide some ideas for other Brightway2 users.

Entering data
=============

The easiest way is to define inventory datasets is in Excel spreadsheets - a familiar and relatively transparent tool. One interesting aspect of the Brightway2 Excel importer is how flexible it can be - you can mark columns and even entire worksheets so that the importer will ignore them, so that you can include the calculations used to determine exchange amounts. You can also choose which fields to include when specifying activities and exchanges - you aren't locked into a certain template. See the `documentation <https://docs.brightwaylca.org/technical/bw2io.html#excel>`__ and the `example spreadsheet <https://bitbucket.org/cmutel/brightway2-io/raw/default/bw2io/data/examples/example.xlsx>`__ to learn more. Similarly, the `CSV importer <https://docs.brightwaylca.org/technical/bw2io.html#csv>`__ works with CSV files (`example CSV file <https://bitbucket.org/cmutel/brightway2-io/raw/default/bw2io/data/examples/example.csv>`__) in basically the same way and with the same flexibility. In addition to being useful by yourself, spreadsheets and CSV files are also effective means of gathering data distributed among teams or subprojects.

You can also write or generate raw text datasets, either by hand, or in a Python program or Jupyter notebook. Building datasets programmatically has several advantages - it is easy to verify correctness, generate variations in activities and exchanges, and interface with other data sources. This was the initial way that I used Brightway2, and what I used to recommend for others. The data format for datasets is very flexible, and `core fields are well-defined <https://docs.brightwaylca.org/intro.html#activity-data-format>`__, so this works for some people. However, it is certainly not the easiest and most user friendly process.

Brightway2 uses unique codes to identify activities and products. It can be tempting to enter these codes directly, but it is usually not the best way for something which will be read or understood by humans. The IO library in Brightay2 has *extensive* facilities for matching activities and exchanges by a number of different fields. These matching algorithms are the core of the IO library, because the standard data formats in LCA are pretty bad at actual data interchange, and so we have to be able to match exchanges based on name, location, unit, categories, etc. Instead of putting in a code field consisting of random string of letters and numbers, it is often better to put in the name and other uniquely identifying fields, and then apply a matching strategy when importing the data.

Of course, data can also be directly imported from standard data exchange formats. For most people, the vast majority of their data comes from imported databases like ecoinvent. Brightway2 can consume `ecospold 1 <https://docs.brightwaylca.org/intro.html#importing-from-ecospold-1>`__, `ecospold 2 <https://docs.brightwaylca.org/intro.html#importing-from-ecospold-2>`__, and `SimaPro CSV <https://docs.brightwaylca.org/intro.html#importing-from-simapro>`__, but extracting and processing information from other formats is often relatively simple. For example, Brightway2 can process the raw numeric input files from `EXIOBASE <http://www.exiobase.eu/>`__ and `EORA <http://worldmrio.com/>`__, as well as the export format for `CMLCA <http://www.cmlca.eu/>`__.

To build something simple, you will in the future be able to use the `activity browser <https://bitbucket.org/cmutel/activity-browser/>`__. The activity browser was started as an independent project by `Bernhard Steubing <http://www.cml.leiden.edu/organisation/staff/steubing.html>`__ to implement his idea of `meta-processes <http://link.springer.com/article/10.1007/s11367-015-1015-3>`__. The activity browsewr is a graphical interface has some nice and new ideas for easily defining activities, and for adding inputs and outputs. Unfortunately, it also has `several bugs <https://bitbucket.org/cmutel/activity-browser/issues?status=new&status=open>`__, and is not yet recommended for general use.

Finally, Brightway2 is even flexible enough to allow you to store data that has nothing to do with LCA. For example, I have stored data about the technical characteristics of motorcycles, and the flight paths of airplanes, as generic `DataStore <https://docs.brightwaylca.org/intro.html#database-is-a-subclass-of-datastore>`__ objects. Similarly, because you can include new fields in inventory datasets, it is often useful to include fields which can be used to process the data to create variants of the original inventories.

Processing data
===============

For conventional LCAs, defining a few activities and linking to a background database would be the end of the inventory work. When we find ourselves with the possibility of doing more, however, we often come up with new ideas to manipulate and interpret the data that we already have. One of the core motivations behind Brightway2, therefore, was to allow us to manipulate our existing data with simple Python scripts. These manipulations almost always include performing many LCA calculations, e.g. for analyzing different production scenarios, or conducting sensitivity or uncertainty analysis. Brightway2 is quite fast, but part of that speed requires choosing the best way to do calculations. I am writing a new section on speed in the manual; for now, see a `previous blog post on speed tips for Brightway2 <https://chris.mutel.org/fast-dont-lie.html>`__.

There are at least five main ways of manipulating existing data, including inventory databases.

Changing the functional unit
----------------------------

On the simplest level, we can change the functional unit provided to LCA calculations to vary the amount of different inputs, or even to change amounts deeper in the supply chain. The easiest way to do this is to use a ``calculation setup`` - a named set of functional units and LCIA methods. For more details, see the `notebook on calculation setups <http://nbviewer.jupyter.org/urls/bitbucket.org/cmutel/brightway2/raw/default/notebooks/Using%20calculation%20setups.ipynb>`__. Here is an example:

.. code-block:: python

    from brightway2 import *
    import numpy as np

    projects.current = "BW2 introduction"

    db = Database('forwast')
    new_bricks, old_bricks = db.search('brick* dk')

    selected_methods = [
        ('IPCC 2013', 'GWP', '100 years'),
        ('ReCiPe Endpoint (I,A)', 'resources', 'total'),
        ('ReCiPe Endpoint (I,A)', 'human health', 'total'),
        ('ReCiPe Endpoint (I,A)', 'ecosystem quality', 'total'),
    ]

    def bricks_needed(amount):
        """Return tuple of (mass new bricks, mass old brick recycling) needed."""
        return {new_bricks: amount, old_bricks: 2 * (1 - amount)}

    calculation_setups['bricks'] = {
        'inv': [bricks_needed(x) for x in np.linspace(0, 1, 5)],
        'ia': selected_methods
    }

    MultiLCA("bricks").results

With the output:

.. code-block:: python

    array([[-0.60672053, -0.02735928, -0.01922127, -0.01120497],
           [-0.37435046, -0.01687011, -0.01185949, -0.00691316],
           [-0.1419804 , -0.00638094, -0.00449771, -0.00262136],
           [ 0.09038967,  0.00410823,  0.00286408,  0.00167044],
           [ 0.32275974,  0.0145974 ,  0.01022586,  0.00596224]])

Of course, you could also do the same with loops and a normal ``LCA`` calculation.

Manipulation using external data sources
----------------------------------------

Similar to manipulating the functional unit, you can use external data sources to change or create variations of your inventory datasets. For example, you could use historical price data to create multiple versions of your economically allocated inventories, change default transport distances based on online routing software, or use a background database of electricity generation over time to create a copy of your inventories which represent past time periods.

Interfacing with other programs
-------------------------------

Python is a nice language for data manipulation and analysis, but sometimes you need to interface with other programs. Exchanging data back and forth can sometimes be a pain, but Python and the Python community have good facilities, libraries, and documentation for importing and exporting many different data formats, or even calling programs like `R <http://rpy2.bitbucket.org/>`__ or `Julia <http://blog.leahhanson.us/post/julia/julia-calling-python.html>`__ directly.

Manipulation using Python functions or programs
-----------------------------------------------

One common example is scenarios - a set of assumptions about current or future parameters. For example, the following code increases the energy efficiency of every electricity input in a background database:

.. code-block:: python

    from brightway2 import *
    db = Database("some database").copy("change all the things!")  # Don't wreck our original data
    for act in db:
        if act['unit'] == 'kilowatt hour':
            continue  # Don't change market or transmission activities
        for exc in act.technosphere():
            if exc.input['unit'] == 'kilowatt hour':
                exc['amount'] *= 0.9
                exc.save()

Now, in real life we should check to make sure our exclusion criteria really excludes all the processes which transmist but don't consumer electricity, and we would also need to re-scale our uncertainty distribution, but you get the general idea. When we express our scenarios in code, we can evaluate many different systems. It is also easy to do this for many scenarios, or many different combinations of parameter values, because it is automated.

Directly writing matrix data
----------------------------

In advanced use, you may wish to skip the creation of inventory datasets with their associated metadata, and write the numeric values for creating matrices directly. The `numeric parameter array format is well documented <https://docs.brightwaylca.org/lca.html#turning-processed-data-arrays-in-matrices>`__. This can be especially useful when you want to create *many* (i.e. hundreds or more) variants of you base inventory datasets, but don't want to bother writing and then deleting new ``Databases`` hundreds of times.

Doing LCA calculations
======================

Most of the time the end product of your data processing will be inventory datasets that can be used directly by the normal ``LCA`` class. However, you can also use other solvers in Brightway2, such as the `least squares LCA <https://docs.brightwaylca.org/technical/bw2calc.html#bw2calc.least_squares.LeastSquaresLCA>`__ for overdetermined product systems, or `supply chain graph traversal <https://docs.brightwaylca.org/lca.html#graph-traversal>`__. You can also subclass the ``LCA`` object to add new matrices or calculation pathways, like in Brightway2-regional (`docs <https://brightway2-regional.readthedocs.org/lca.html>`__) (`example code <https://bitbucket.org/cmutel/brightway2-regional/src/default/bw2regional/lca/base_class.py>`__).
