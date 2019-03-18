The allure of simple system models
##################################

:date: 2019-03-17-22:00
:category: bonsai
:slug: bonsai-system-models
:summary: Simple is better than complex. Complex is better than complicated

.. figure:: images/zen-rocks.jpg
    :align: center
    :alt: From https://www.flickr.com/photos/campra/20416181068

A system model (also called a construct in IO) is a set of rules, assumptions, and the accompanying computer code that turn individual data points into a complete and consistent database. Some of the most important parts of system models are handling activities which produce multiple products, linking product suppliers and consumers in time and space, and reconciling conflicting data points. Each of these functions could be controversial, as in many cases practitioners must make choices without being able to test their scientific validity. A system model is a compromise between our dreams and what is currently possible. Sometimes we dream too big, and end up with things like the waste treatment merger (don't ask). Though I doubt the BONSAI consensus system models will ever be "done", here is a brief discussion of how we will start building them.

Multioutput activities
----------------------

Many things in life produce more than one useful output - combined heat and power plants are a classic example, but even something as simple as consuming a bottled drink produces the service of the drink, and an empty bottle that can be recycled into other products. When we build a model that allows us to consume just heat or just power (or just Rivella), we have to do something about the other products which are produced. This is one of those problems that most people can intuitive grasp, and immediately come up with what they think is the one obvious answer. Unfortunately, everyone has a different answer.

At the beginning, we will not attempt to reinvent the wheel. Economists have been applying system models for decades, and we can apply these models directly. We even already have `Python code <https://github.com/stefanpauliuk/pySUT>`__, though I think this will have to be adapted for the size of the BONSAI matrices. If you are interested in the details of these models, I heartily recommend the `work of Guillaume Majeau-Bettez <https://scholar.google.com/citations?hl=en&user=iFAcI2wAAAAJ&view_op=list_works&sortby=pubdate>`__.

Linking in time and space
-------------------------

Each data point in BONSAI will give a description of an input or an output from an activity, and it will be up to the system model to link these inputs and outputs together. Though most LCA databases make datasets specify these links ahead of time, the current version of ecoinvent follows a similar strategy of linking via system modelling software. I have been part of the `ocelot <https://github.com/OcelotProject/Ocelot>`__ project, which is an ongoing effort to encode these system models in open source software. This is really hard, for a variety of reason, but a major one is how when complex rules are combined together, they create code and results that are difficult to work with or reason about. The details aren't worth going into, but my key lessons for a BONSAI model would be:

* No adoption of ideas which have not been tested and implemented at a large scale!
* Map-reduce works well. Iterators work well. Log everything.
* `Simple is better than complex. Complex is better than complicated <https://www.python.org/dev/peps/pep-0020/>`__.
* No dynamic "Rest-of-World" locations - everything should be located definitively in space.
* Use the idea of "market" activites sparingly or not at all. The small benefits they bring come with significant complexity, meaning bugs and unexpected behaviour.

Linking in time is currently the domain of dynamic LCA. There are a lot of value choices here as well, both in accepting or rejecting the current state of the world, but also in generational equity (just as environmental justice is an important topic for research in regionalized LCA) and in the temporal allocation of infrastructure burdens. We can also add data and concepts from industrial ecology on material stocks and fleet modelling. At first, though, we will be happy to link the different years present in EXIOBASE.

Reconciling conflicting data
----------------------------

This is the area that I am personally the most excited about, as this is where I think we can really add something new. Our basic approach will be to `maximize information entropy <https://www.tandfonline.com/doi/abs/10.1080/09535314.2016.1271774?casa_token=8VHhgSCxAYIAAAAA:e5Dk2fOYWhHZnAotyHD9Nr3FPXTttoLq9mr17nGzV1UHBqbDSnFIA_DcAG_C9FpA8mzHoG61Mg6i>`__. While this theory is well known, and has been applied to IO models, it begs the question - how does one get probability distributions for data without characterized uncertainty, how does one handle data points (or distrobutions) which only partially overlap, and what preparation steps are needed for input datasets (such as material, energetic, or economic balances)? As usual, the devil is in the details. We also have the option of explicitly including outside data sources, either as validation of calculated totals, or to help us adapt existing data to new contexts. This overall component will be difficult, and will probably be done in cooperation with other researchers rather than strictly as a BONSAI initiative.
