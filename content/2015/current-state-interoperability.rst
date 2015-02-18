Why we can't we all just get along?
###################################

:date: 2015-02-18 00:00
:category: data
:slug: lca-data-exchange
:summary: Reflections on the current state of LCA data interoperability

Ecospold is the data format for life cycle inventory and impact assessment data developed for the `Ecoinvent database <http://ecoinvent.org/>`_. It is an `XML <http://en.wikipedia.org/wiki/XML>`_ data format, with all the good and bad things that entails. Like many things in Ecoinvent, it was a good attempt at the time it was designed, but the numerous attempts to create a new data format show that it has not been a great format for data sharing. In this post, I want to explain the frustration of trying to work with Ecospold.

.. note:: Ecospold version 2 is a completely different subject

Misspellings
Misplaced commas and spaces
Inputs refer to processes that don't exist
Inconsistent namespacing (ESU XML files)


.. warning:: The 2011.10.25 version of the US LCI database has a file called *EcospoldXML_2011.10.25.zpp*. You need to change the file extension to **.zip**; this file will then extract as a normal *zip* file.
