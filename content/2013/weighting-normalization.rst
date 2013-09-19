Brightway2: Including weighting and normalization
#################################################

:date: 2013-05-27 12:00
:category: brightway2
:slug: new-example-weighting-and-normalization
:summary: A new example ipython notebook shows how to include weighting and normalization in Brightway2

Weighting and normalization are two optional steps in life cycle impact assessment calculations. Until now, there has not been any support for anything other simply multiplying a life cycle inventory by a vector of characterization factors in Brightway2. This wasn't a problem, because the ecoinvent centre implementation of its provided impact assessment methods already included weighting and normalization steps where appropriate. However, we would like to be able specify, and modify, these values ourselves.

.. figure:: images/weights.jpg
    :alt: "Do you want to get heavy" by the Jon Spencer Blues Explosion is a great song
    :align: center

    Figure 1: Weighting used to be simpler. Credit: `Joe Thom <http://www.flickr.com/photos/joethorn/97788312/>`_.

A `new ipython notebook example <http://nbviewer.ipython.org/url/brightwaylca.org/examples/weighting-and-normalization.ipynb>`_ shows how easy it is to add weighting and normalization using the Brightway2 framework. These features will be added to the main source code repository soon.
