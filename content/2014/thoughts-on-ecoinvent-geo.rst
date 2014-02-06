Some thoughts on Ecoinvent geographies
######################################

:date: 2014-02-06 12:00
:category: ecoinvent
:slug: thoughts-ecoinvent-geo
:summary: Some thoughts on geogrpahies and geographical data in Ecoinvent version 3

.. figure:: images/louisiana.png
    :alt: Spatial datasets each have their own version of the world
    :align: center

    Figure 1: The Louisiana shoreline, as given by different datasets - red is state borders from `NationalAtlas.gov <http://nationalatlas.gov/maplayers.html?openChapters=chpbound#chpbound>`_, green county borders from the same source, and black is `Natural Earth 10m cultural <http://www.naturalearthdata.com/downloads/10m-cultural-vectors/>`_.

Ecoinvent version 3 uses spatial data to define the locations of inventory datasets (see the `data quality guidelines <http://www.ecoinvent.org/fileadmin/documents/en/Data_Quality_Guidelines/01_DataQualityGuideline_v3_Final.pdf>`_, `spreadsheet of geographies <http://www.ecoinvent.org/fileadmin/documents/en/List_of_Geographies/eiv3_geographies-names_coordinates_shortcuts_20130904.xlsx>`_, `list of geographies and spatial coordinates in Ecospold2 XML <http://www.ecoinvent.org/fileadmin/documents/en/Data_Quality_Guidelines/GeographiesIncludingKml.zip>`_, and `individual geographies in KMZ format <https://dl.dropboxusercontent.com/u/1911208/geographies-kmz.zip>`_). There is also a website for `creating new geographies <http://geography.ecoinvent.org/>`_ (`source code <https://bitbucket.org/cmutel/ecospold2-geo-utils>`_).

These locations are called *geographies* because their spatial coordinates are stored as `geographic coordinates <http://workshops.boundlessgeo.com/postgis-intro/geography.html>`_, i.e. longitude and latitude, and are not projected to a plane.

However, the current implementation is a pain to deal with, both for existing users, and for editors. The ideal solution would have, at a minimum, the following qualities:

* The spatial information should produce the same calculation results on different spatial databases, including `SQL server <http://alastaira.wordpress.com/2011/04/03/sql-server-spatial-coordinate-calculation-precision/>`_, the database used by Ecoinvent.
* It should be relatively easy to everyone to see and download individual geographies, and to create new geographies and import them to the database.
* It should be easy to build the geographies in Ecoinvent using software and spatial datasets that are free and open source. This software should be well documented and tested.

In my opinion, the best way forward from what we have right now is:

* The current software at `geography.ecoinvent.org <http://geography.ecoinvent.org/>`_ should be improved to include current geographies, and to be able to automatically provide a notification to the Ecoinvent centre when a geography should be imported to the Ecoinvent database.
* A new software that will import datasets like Natural Earth, and recreate the *geographies.xml* file. This software should be as easy as possible to install and use (i.e. probably not use a spatial database). It should also round coordinates to 8 digits after the decimal point to make the math easier, reduce spurious errors, and reduce file sizes.

A more revolutionary thought is whether the current system of using spatial coordinates to define spatial relations is needed for Ecoinvent at all. The current system uses the OGC Simple Feature relation `contains <http://postgis.refractions.net/documentation/manual-1.4/ST_Contains.html>`_ to determine if an inventory dataset can be linked to another dataset, e.g. the state of Louisiana is *contained* in the USA, and therefore contributes to its market mixes. However, if you look closely at Figure 1, you can see that the borders of the state and country don't match up. What this means practically is that each state has to be manually modified to fit inside the borders of the country, and even then what is contained on one machine with one set of geospatial libraries is not contained on another machine. Moreover, there are areas in the country borders of the USA which are not contained in the state of Louisiana borders, meaning that the union of all states would not equal the country borders.

As an alternative, we could consider moving away from using the actual spatial data to define spatial relationships, and instead do this manually in a separate file. At first, this sounds a little crazy - if you know where things are, with bleeding GIS coordinates, then of course we should use this data! The answer to this objection is three-fold:

#. We only actually use the spatial data to build a tree of spatial relationships - and we know what the spatial relationships should be. Manually specifying them would only save some time and a lot of frustration.
#. The actual spatial data is also used for regionalized life cycle assessment, but for regionalized LCA there is no contains requirement, meaning we could just use the native spatial datasets like Natural Earth without modification. Using the native datasets is more flexible, as we just follow their updates, and much easier for Ecoinvent.
#. Providing a list of what region lies within what other regions is much more transparent than a > 100 megabyte file with spatial data that can't be easy loaded into e.g. Qgis or Google Earth.
