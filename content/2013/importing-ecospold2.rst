Importing ecospold 2 databases
##############################

:date: 2013-09-20 12:00
:category: ecospold2
:slug: importing-ecospold2
:summary: Importing ecospold 2 databases isn't that difficult, once you learn how.
:status: draft

Limitations of this post
************************

In this blog post, we don't import all of the fields in ecospold 2, but only the ones needed to make calculations and identify datasets.

Ecospold versions one and two
=============================

The ecospold 1 data format has many faults, but its conceptual model of inputs and outputs was very simple. Consider this definition of a technological input from a randomly chosen dataset in ecoinvent 2.2:

.. code-block:: xml

    <exchange number="1942"
              category="transport systems"
              subCategory="road"
              name="transport, lorry 20-28t, fleet average"
              location="CH"
              unit="tkm"
              uncertaintyType="1"
              meanValue="14"
              standardDeviation95="2.095">
        <inputGroup>5</inputGroup>
    </exchange>

Even if you aren't familiar with `XML <http://en.wikipedia.org/wiki/XML>`_, you can easily see that the input is 14 ton-kilometers of lorry transport. You can also finding this lorry process in the database through a combination of name, category & subcategory, location, and unit.

Contrast this with another definition of an input from ecoinvent 3.01 in the ecospold 2 format:

.. code-block:: xml

    <intermediateExchange id="f0fa94e1-3fe1-4d7c-bd78-5594ff72f9c7"
                          unitId="86bbe475-8a8f-44d8-914c-e398787e7121"
                          amount="0.00050696"
                          intermediateExchangeId="479ce50b-7465-4ee0-ada2-81418055c725"
                          activityLinkId="6c380b61-5f79-4cd0-9ecc-28844d9bf01e">
        <name xml:lang="en">mowing, by rotary mower</name>
        <unitName xml:lang="en">ha</unitName>
        <uncertainty>
            <lognormal meanValue="0.00050696"
                       mu="-7.59"
                       variance="0"
                       varianceWithPedigreeUncertainty="0.0086"/>
            <pedigreeMatrix reliability="2"
                            completeness="1"
                            temporalCorrelation="4"
                            geographicalCorrelation="1"
                            furtherTechnologyCorrelation="1"/>
        </uncertainty>
        <inputGroup>5</inputGroup>
    </intermediateExchange>

This is a bit harder to handle - the ecospold 2 design team (including myself) learned about `UUIDs <http://en.wikipedia.org/wiki/Universally_unique_identifier>`_, and decided to UUID all the things!

As `Brightway2 <http://brightwaylca.org>`_ has some powerful and unique computational abilities, it was used in several of the talks, and I hope that Brightway2 can help continue to advance the state of the art in uncertainty and sensitivity analysis in LCA.

.. figure:: images/ei3-attributional.png
    :alt: Visualization of ecoinvent 3 technosphere matrix, attributional version.
    :align: center

    Figure 1: Visualization of the ecoinvent 3 technosphere matrix, default allocation.

The `LCA discussion fora <http://lcaforum.ch/>`_ have a long history of contributing to research and improved practice. On September 13, 2013, the 53rd LCA discussion forum was held in Zurich. Its formal title was *Uncertainty in Life Cycle Assessment: State of the art and practical challenges*, but we can shorten that to just *Uncertainty in LCA*, and it was organized by Catherine Raptis, Stephan Pfister, and myself.

.. figure:: images/ei3-consequential.png
    :alt: Visualization of ecoinvent 3 technosphere matrix, consequential version.
    :align: center

    Figure 2: Visualization of the ecoinvent 3 technosphere matrix, consequential system model.

In contrast to most recent discussion fora, we purposefully chose fewer speakers and more time for discussion. We also included a group exercise later in the day, which is risky because most people are tired and ready to leave. However, I think that this discussion forum was actually really great, and the slower pace and increased interaction allowed for some real thought and conversation. I hope that future organizers will chose to have fewer talks.

You can find the talks online as `videos <http://www.multimedia.ethz.ch/misc/lca/2013>`_, as well as see separate uploads of the slides (soon). We will also be writing up a conference report in the near future.

