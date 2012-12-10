Visualizing Ecoinvent 2.2
#########################

:date: 2012-11-29 12:00
:category: visualization
:slug: visualizing-ecoinvent
:summary: Visualizing the technosphere matrix of Ecoinvent using Brightway2 and Gephi

Ecoinvent 2.2 is a large and complex system (and Ecoinvent 3 will certainly be larger and more complex). The technosphere matrix of Ecoinvent has about 4000 activities, and 40000 links between those activities. The biosphere matrix has another 60000 links from activities to biosphere flows, but it is harder to visualize, so we ignore it for now.

I used `Brightway2 <http://brightwaylca.org>`_ to import Ecoinvent, and export it as a `GEXF <http://gexf.net/format/>`_ file, the file format used by `Gephi <https://gephi.org/>`_. This is pretty easy, especially if you are comfortable in Python:

.. code-block:: python

    from bw2data.io import EcospoldImporter
    from bw2data.io.export_gexf import DatabaseToGEXF
    EcospoldImporter().importer("path/to/ecoinvent/xml/files", "ecoinvent 2.2")
    DatabaseToGEXF("ecoinvent 2.2").export()

After messing around a bit in Gephi, and then manually labelling some nodes in Inkscape, the result is almost beautiful:

.. image:: images/ecoinvent-small.png

You can also download a `larger version <images/ecoinvent.png>`_, a `pdf version <images/ecoinvent.pdf>`_, or a `desktop background <images/ecoinvent-background.png>`_.