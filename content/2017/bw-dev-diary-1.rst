Brightway development diary #1
##############################

:date: 2017-02-14 23:00
:category: brightway2
:slug: brightway-dev-diary-1
:summary: Some random thoughts as I work on the next version of Brightway

.. figure:: images/azores-landscape.jpg
    :align: center

Uniquely identifying intermediate flows
=======================================

As part of the redesign of Brightway, I have been defining database schemas on a finer level than I have previously. When I first started working on Brightway, I saw a detailed database schema as an artificial restriction on the freedom of people to define their own activity datasets, and to use whatever fields were appropriate for their use cases. Experience has shown me that most people appreciate some structure - they want to focus on their specific problems, not build an entire LCA system from the ground up. I still plan to have a more "free form" back end at some point, but the focus now is on something with a little more structure than the current default ``bw2data`` backend.

As part of the clean separation of activities and flows, I have found myself forced to break out of the mental mode of ecoinvent (and probably most other databases), in which each activity has a single "reference product" - instead, Brightway should support each activity having zero, one, or many products. This separation has introduced some new problems, and the one I am currently struggling with is how to uniquely identify these intermediate flows (they are products to some activities, but are inputs to others.) Their names aren't unique - for example, "steel" can be produced in many places. Although this feature isn't widely used yet, we also need to recognize that inventory databases can differentiate activities by temporal range, such as separate datasets steel production in China from 1990 to 2000, and from 2000 to 2010.

So far, then, in order to uniquely identify an intermediate flow our table needs to have a name, a unit, (maybe) a location, (maybe) a temporal range, and, at least in the case of biosphere flows, a list of categories. We probably also want a label for the collection that the flow belongs to, such as "ecoinvent" or "Joe's midterm project." However, I don't know if these fields are either necessary *or* sufficient to uniquely identify these intermediate flows - this is somehow too specific, and in some cases probably not specific enough. so far I don't have any uniqueness constraints in the database schema either. My preliminary conclusion is that, at least most of the time, we search for and identify a flow by its producing activity. In this case, the user interface needs to make searching such relations easy.

Making user interfaces harder
=============================

Brightway2 had two levels of abstraction above the database - one level provided by the `Peewee ORM <http://docs.peewee-orm.com/en/latest/>`__, and another in Brightway2 itself. You can see some of this indirection in the ``bw2data`` definition of `Activity <https://bitbucket.org/cmutel/brightway2-data/src/aa5e4a8377aef097be0e694ead2a149ec04dec84/bw2data/backends/peewee/proxies.py?at=default&fileviewer=file-view-default#proxies.py-100>`__. In the default backend for Brightway TNG (or whatever the next version is being called by the corporate types down at headquarters) there is only one level - the Peewee documents themselves. This means that you will need to learn some new syntax to do some basic things - here are some examples from recent test writing:

* ``Database("foo").random()`` becomes ``Collection.get(Collection.name == "foo").activities.get()`` or ``Activity.get(Activity.collection == Collection.get(Collection.name == "foo"))``.
* ``for x in Database("foo")`` becomes ``for x in Collection.get(Collection.name == "foo").activities``. But note that you can also do ``for x in Collection.get(Collection.name == "foo").flows``.

However, it is not all bad. By working directly with Peewee queries, and by moving everything into the database, we can now use the power of SQL to make some nice queries. We also get to do data manipulation in the database instead of loading data into Python first. By reducing the amount of code, we sidestep many bugs. Finally, we get consistency - the interface for everything in the SQLite database is the same.
