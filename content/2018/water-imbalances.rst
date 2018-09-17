Water imbalances, or the need for consistency in environmental flows
####################################################################

:date: 2018-09-13 22:00
:category: brightway
:slug: water-imbalances
:summary: How Brightway2 got water flows in ecoinvent 3 very, very wrong

.. figure:: images/stones.jpg
    :alt: https://www.flickr.com/photos/132479508@N02/31542770066/
    :align: center

Matrix-based life cycle assessment
==================================

The basic equation for site-generic matrix-based life cycle assessment is:

.. math::
    h = CB \cdot diag ( A^{-1}f )

**C** is the characterization matrix, which translates amount of environmental flows (also called elementary flows or biosphere flows, e.g. :math:`CO_{2}`) into midpoint or endpoint units of damage. These numbers are generally positive, e.g. a certain number of years of life lost; a negative value here would represent a net reduction in environmental or other damage.

**B** is the biosphere matrix, which gives environmental flows per activity. These values are also generally positive, e.g. X kilograms of :math:`CO_{2}` per Y units of some industrial activity.

Somewhat surprisingly, activities themselves don't really have a unit. Instead, each activity is scaled to produce a certain number of products, and it is the products that have units, like one kilogram of steel or one piece of candy. Activities can produce one or more products, but some activities, like certain waste treatment activities, produce no useful products.

**A** is the technosphere matrix, our model of the industrial world. It has columns of activities and rows of products. Negative numbers represent the net consumption of products, while positive numbers are net production. **A** can have ones down the diagonal, but doesn't have to; a more fundamental rule is just to remember that negative is consumption and positive is production. As long as **A** isn't singular, you can use it for any arbitrary demand.

*f* is the demand vector, and is given in products. Positive numbers represent demand for a product, and negative numbers are an excess product that should be substituted or avoided in the industrial economy.

The problem
===========

The ecoinvent center provides implementations of many different LCIA methods, and the characterization factors are almost always positive. For example, in the 3.5 implementation there are 850 separate impact categories, and 220.699 individual characterization factors, of which only 1.535 are negative. You can see some exploratory data analysis in `this notebook <https://nbviewer.jupyter.org/urls/bitbucket.org/cmutel/spatial-assessment-blog/raw/d4039248d27997d4d828772d1b1d77659d29c00e/notebooks/Exploring%20negative%20CFs%20in%20the%20ecoinvent%203.5%20LCIA%20implementation.ipynb>`__. Similarly, the biosphere matrix in ecoinvent 3.5 cutoff has 370.448 non-zero values, of which 1.115 are negative. The problem is the inconsistency in how the consumption of natural resources and the release of emissions are handled. In contrast with how values in **A** are signed, both the consumption of natural resources and the release of emissions in **B** have positive numbers. Normally, this isn't a problem, as the characterizaton factors in **C** have the correct sign to translate both of these effects (the consumption of natural resources, which is generally bad, and the release of pollution, which is also generally bad) into impacts correctly.

This breaks down in the case of water balances. Here is a screenshot from an inventory for electricity production from run-of-river hydropower:

.. figure:: images/water-imbalance.png
    :alt: Water in, water out
    :align: center

Brightway treats both the consumption of water as a natural resource and the release of water as positive numbers; so, both would get characterized as environmental damage if they both have a postive characterization factor. We would instead want there to be no net consumption of water by this activity. Earlier versions of `bw2_aware <https://github.com/cmutel/bw2_aware>`__ and `bw2_lcimpact <https://github.com/cmutel/bw2-lcimpact>`__ got this wrong - they had positive CFs for water releases, resulting in double counting. I think that the current ecoinvent LCIA implementation also gets it wrong, as it doesn't characterize water releases at all. In this case, water-neutral activities would have a large impact, as withdraw was characterized but release was ignored.

The solution I first came up with was to adjust the biosphere exchanges, to make "emission to water" actually be negative. This would be consistent with a positive characterization factor. Of course, we couldn't do this to all emissions - most emissions are of pollutants, which cause damage, and as such need positive numbers. Instead, to fix this we would need to special case emissions of water *to water*, and flip the sign of these emissions to be negative. This wouldn't result in a net zero number in the **B** matrix - these are two different flows, and therefore are listed in different rows - but the same CF would be applied to both numbers, resulting in no net impact.

However, the good folks at GreenDelta came up with a much better idea that I saw at the `discussion forum on regionalization <http://www.lcaforum.ch/Forum/tabid/57/Default.aspx>`__. You know what is *meant* by releases of water to "water", so you can just give these flows a negative characterization factor. This allows us not to change the ecoinvent database, though updates did have to be made to `bw2_aware <https://github.com/cmutel/bw2_aware/commit/d753f2af2708c4c97d8e9345c965966502245971>`__ and `bw2_lcimpact <https://github.com/cmutel/bw2-lcimpact/commit/5af0e29440146faa2c60a8366c691d333af7d015>`__.

I am currently investigating if the same problem would show up for other flows, such as carbon (which is also balanced in ecoinvent 3, though this comes with its own set of challenges due to how we assess biogenic carbon) and land use.

The long-term solution
======================

It would be easy to avoid these problems in a systematic way by consistently treating flows in **B** the same way we treat flows in **A**: consumption is given a negative value, production is given a positive value. This would require some changes in our characterization factors - their signs would also have to be adjusted. As in many things in life, however, a small investment by a few people would benefit the entire community for a very long time.

Changes
=======

This post was updated on September 17. I switched from making changes in ecoinvent to making changes in the LCIA method, and added a notebook and discussion of how water is handled in the ecoinvent LCIA implementation. As always, you can see all changes to this blog at its `source repo <https://bitbucket.org/cmutel/spatial-assessment-blog>`__.
