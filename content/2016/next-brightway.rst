What's next for Brightway?
##########################

:date: 2017-01-13 01:00
:category: brightway2
:slug: next-brightway
:summary: Plans for the next iteration of the Brightway LCA software framework

Recently, someone asked me if `Postgresql <https://www.postgresql.org/>`__ could be easily used as a storage engine instead of `SQLite <https://sqlite.org/>`__ in Brightway2. "Of course," I thought, "that is the whole idea of a modular framework. I love Postgres, and the first version of Brightway used Postgres!" I was wrong, though. One of the core design principles of Brightway2 was a `loose coupling <https://en.wikipedia.org/wiki/Loose_coupling>`__ between the data management and calculation engines. But there is a problem: the current version clearly fails this test. The rest of this post will describe the current software, including (some of) its weaknesses, and what I want to do differently in the next generation.

The Status Quo
==============

Brightway2 is called Brightway **2** because it was a more-or-less complete rewrite of life cycle assessment software I wrote during my PhD at ETH Zürich. The core libraries of Brightway2 are `brightway2-data <https://bitbucket.org/cmutel/brightway2-data>`__, which manages data in several different backends; `brightway2-calc <https://bitbucket.org/cmutel/brightway2-calc>`__, which loads numerical arrays and does various matrix-based calculations; and `brightway2-io <https://bitbucket.org/cmutel/brightway2-io>`__, which imports and exports LCI and LCIA data and results.

The good
--------

The existing software has a lot of very nice aspects, and is widely used by people who want to work outside the existing restrictions of most LCA software. A lot of the good parts of Brightway2 come from building on top of awesome work by others - this is the magic of open source software - and it turned out to be an especially good choice to write scientific software in Python, as there is a lot of great stuff happening in this community. Brightway2 has great mathematical performance (Brightway2 has certainly done far more LCA calculations than all other LCA software combined), and although there isn't a great graphical interface, the command line does allow for some remarkable expressiveness. Here is a quick example that decreases the transportation requirements of every activity in ecoinvent by ten percent:

.. code-block:: python

    for activity in Database("some ecoinvent"):
        for exchange in activity.technosphere():
            if exchange.input['name'].startswith("transport,"):
                exchange['amount'] *= 0.9
                exchange.save()

Of course, in real life you would have to check to make sure that you aren't doing stupid things to special cases - and ecoinvent loves their special cases - but you get the general idea.

Brightway2 also has *projects*. Each project has its own version of its data, and each project is just a subdirectory. This means that for each project you work on, be it a client study or a paper, you can preserve your work without worrying about other projects modifying the background databases or other data. Because each project is a subdirectory, you can also store them on Dropbox or easily ship one to a Docker container.

Finally, Brightway2 and Python are flexible and have few built-in limitations. This allows you to play around, and quickly implement new ideas. For example, the code supporting the following graph creation was written in only two hours:

.. code-block:: python

    Database("ecoinvent 3.3 cutoff").graph_technosphere()

.. figure:: images/ecoinvent-33-technosphere.png
    :align: center

    Ecoinvent 3.3 cutoff technosphere matrix

The bad
-------

Brightway2 has evolved a lot since the first commit in October 2012. The way data was stored in databases changed completely, for example. Project management only came in 2015; before that, you specified a data directory in an environment variable. There is still a lot of cruft from earlier approaches in the code base, and not all functions have been updated to the latest approach. LCIA methods, for instance, are still stored in files instead of in a database.

The ugly
--------

Write locks
```````````

Because some data is stored in files as JSON or `pickles <https://docs.python.org/3/library/pickle.html>`__, Brightway2 uses a write lock to prevent two threads from overwriting each other's changes. Locks are implemented using the `fasteners <https://pypi.python.org/pypi/fasteners>`__ library. This works OK, though if something goes wrong, it can be very frustrating to fix. Proper architecture wouldn't require a write lock in the first place.

Poor differentiation between products and activities
````````````````````````````````````````````````````

This is currently possible in Brightway2 - you can create an `activity with the type 'product' <https://bitbucket.org/cmutel/brightway2-calc/src/77807d5966bf7756a8870261cd6531185e1124e5/tests/lca.py?at=default&fileviewer=file-view-default#lca.py-315>`__ - but none of the machinery is set up to handle this in an intelligent way. Your ``product`` will still be stored as an activity, as will all biosphere (elementary) flows. It is possible to set up multioutput activities by just creating two ``production`` exchanges, and they will work fine with `LCA matrix construction and calculations <https://bitbucket.org/cmutel/brightway2-calc/src/77807d5966bf7756a8870261cd6531185e1124e5/tests/lca.py?at=default&fileviewer=file-view-default#lca.py-235>`__, but most code and importers assume that an activity has a single reference product.

The ``mapping`` object
``````````````````````

Brightway2 has a global dictionary linking all activity databases and codes to a unique integer number. Each activity is identified by an integer in processed arrays, which store database and method data. These integers occupy a fixed amount of space and can be quickly manipulated by numerical routines. Here is a sample:

.. code-block:: python

    {('ecoinvent 3.2 consequential', 'b7ec253b142868afdbf7039818b41059'): 22887,
     ('ecoinvent 3.2 cutoff (ocelot)', 'c6035426edb25dff5e2cac9faa04d294'): 68215,
     ('biosphere3', 'b6349d15-124b-473b-86b5-da63e0060c1a'): 3098,
     ('ecoinvent 3.2 apos', '700099b63130bdd8a315ba3737ba7e25'): 34268,
     ...}

The codes generated by ``brightway2-io`` were a hash of different activity attributes, and therefore were consistent from machine to machine (the names of activities don't depend on the computer where you import the data), the same is not true for the integer values in ``mapping``. These integer values depend on the order of insertion on each machine and in each project. ``mapping`` was stored as a serialized dictionary in a file, and in some cases could have 100000 values or more. Because it was stored in a file, it had to be loaded completely into memory each time a project as activated. Moreover, because it was used by ``brightway2-calc``, it meant that ``brightway2-calc`` had to be able to import ``brightway2-data``, violating the separation between these two components.

``brightway2-calc`` assumes some data is available
``````````````````````````````````````````````````

Technically, it is possible to run a ``brightway2-calc`` calculation `without access to brightway2-data and some project data <https://bitbucket.org/cmutel/brightway2-calc/src/77807d5966bf7756a8870261cd6531185e1124e5/brightway2-calc/independent_lca.py?at=default&fileviewer=file-view-default>`__, but this functionality is bolted on as a late addition to the library. Most code in ``brightway2-calc`` assumes that ``brightway2-data`` is importable. The reason that this is ugly is that it binds ``brightway2-calc`` tightly to the changing code of ``brightway2-data``, and such explicit or implicit assumptions are easy roads for the introduction of bugs. Moreover, it confuses the core purpose of the two libraries - ``brightway2-calc`` shouldn't be doing data manipulation.

``projects.set_current()`` can both select and create projects
``````````````````````````````````````````````````````````````

It is a violation of the `principle of least surprise <https://en.wikipedia.org/wiki/Principle_of_least_astonishment>`__ that these two very different things can be accomplished with the same method call, especially given the method name ``set_current``.

The default backend stores some data in binary Python blobs
```````````````````````````````````````````````````````````

This choice prevents anything other than a Python process from accessing or modifying the data, including internal database indexes. Both SQLite3 and Postgres could handle this data in an intelligent way if it was stored as JSON, and programs written in other languages, such as custom user interfaces, could actually work with the data.

The next generation
===================

In my opinion, the future of software for life cycle assessment, and integrated environmental assessments in general, is a move away from monolithic software stacks, and towards a more decentralized and chaotic market place of ideas. Of course, this is not a particularly `new idea <https://chris.mutel.org/ecobalance-2016.html>`__, not even in the LCA world, and some people have put it `better than me <https://en.wikipedia.org/wiki/The_Cathedral_and_the_Bazaar>`__. Imagine you are a graphic designer who has an idea for a new class of LCA result charts, or someone who doesn't know about calculation methodologies but has a different approach to entering inventory data. It is very difficult to implement these ideas without developing a full stack of LCA software, as the current data formats are not all that compatible between software systems, and there aren't formats at all for things like the result of an LCA calculation. If we lived in a world where people couple specialize on a certain section of the LCA software chain, everyone could focus on their particular areas of expertise, and we would get data interchange for free, because it would be required for all the parts to work together robustly. The next generation of Brightway will be a step towards that world, with very loosely coupled components, well-defined APIs between components, and better formats for data interchange.

First, the big things that will change:

* The next generation of Brightway2 will be known simply as Brightway, though it will be version 3.0. If you are curious, ``brightway2`` is currently at version 2.0.2, ``brightway2-data`` is at version 2.3.2, and ``brightway2-calc`` is at version 1.5.3.
* Brightway2 projects will be easily upgraded to Brightway version 3.
* Brightway version 3 will be Python 3.5+ only.
* Brightway will switch to Github. I personally prefer Mercurial to Git, but the development experience and community on Github is too good to ignore.

Smaller changes
---------------

* Instead of ``projects.set_current()``, we will have ``projects.select()`` and ``projects.create()``.
* Instead of binary data in the default database backend, Brightway version 3 will use JSON.
* No more write locks in the default backend. All data will be stored in a SQLite database and multiple threads can read and write at the same time.

New plugin architecture & common API
------------------------------------

There will be a plugin architecture building on top of `stevedore <http://docs.openstack.org/developer/stevedore/index.html>`__, and a common API that will allow new plugins to "just work". This common API will define common entry points, and dispatch the new information. A plugin that provided search capabilities, for example, would tie into the entry points for an activity being changed, and when an activity changed, this entry point would call the function in the search library that would update the data in the search index for the altered activity. However, certain configurations of Brightway will not need or use the common API, and it will be possible to have a completely different user interface and database, and only use the functions in the calculation and analysis packages.

No more ``mapping`` in the default backend
------------------------------------------

Instead of a mapping dictionary, we can instead use the fact that our database already has integer ids for each database row in the activity table. We don't need a separate ``mapping`` object and file, and all the code this requires. Similar analysis applies to the ``geomapping`` dictionary as well, which will also be stored in a new database table for locations.

Redefining LCA object construction
----------------------------------

Currently building an LCA object requires ``brightway2-calc`` to import ``brightway2-data`` to read the ``mapping``, and to figure out the dependency graph between databases. In the new version there will be a helper function in the equivalent of ``brightway2-data`` to prepare the input arguments to any ``brightway2-calc`` calculation. The new calculation library will be truly independent of the underlying data store, and will instead just load arrays from a file or web resource, build the required matrices, and do the calculations.

Splitting the LCI processed array into technosphere and biosphere arrays
------------------------------------------------------------------------

Currently, the technosphere and biosphere exchanges in an LCI database are stored as one processed array, which has to be treated differently from all other processed arrays when building matrices. ``brightway2-calc`` neeeds to know how to split this array into two components, the technosphere and biosphere arrays, and then alter the signs on some of the values in the technosphere array based on the type of exchange. In the next generation, the data backends will instead generate two processed arrays with the correct signs, and all the special case code in ``brightway2-calc`` can be removed.

Conclusion
==========

The new generation will introduce some backwards incompatibilities, but these changes will be well documented, and only made when there was a clear case for improvement. Code from Brightway2 will be reused whenever possible.

The next generation of Brightway will be a large step on the journey towards a world of decentralized LCA applications that can interact with each other. The respective components of Brightway will truly be independent of one another, and the interfaces between Brightway libraries will be well defined for the first time. The result of these changes will be a software framework where it is much easier to build interfaces to other databases or storage concepts, and much easier to write user interfaces against a common, well-defined API.

The shift towards a more modular design with packages on Github should improve the ability of the LCA community to contribute to Brightway.
