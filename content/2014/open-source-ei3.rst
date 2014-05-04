Some ideas on an open source version of the ecoinvent software
##############################################################

:date: 2014-04-30 00:00
:category: ecoinvent
:slug: open-source-ei3
:summary: An open source version of the software needed to transform unit process master datasets to allocated, single output unit process datasets could increase confidence and transparency of ecoinvent version three.

Disclaimer
----------

I am entirely responsible for the content of this post. Neither `ETH Zürich <https://www.ethz.ch/en.html>`_ or the `ecoinvent centre <http://ecoinvent.org/>`_ have any connection to the opinions expressed herein.

Ecoinvent version 3: A difficult elevator pitch
===============================================

There are still a lot of people confused or doubtful about ecoinvent version 3. One of the big questions that people have, as seen repeatedly on the LCA mailing list, is exactly how ecoinvent 3 works. True, there is a document called the "`data quality guidelines <http://www.ecoinvent.org/fileadmin/documents/en/Data_Quality_Guidelines/01_DataQualityGuideline_v3_Final.pdf>`_", which explains the concepts behind ecoinvent 3 in some detail. But even in the "Advanced LCA" PhD seminar that I led last fall, the data quality guidelines raised as many questions as it answered, and few have the days needed to read through that document thoroughly. The large number of changes from `version two to version three <http://www.ecoinvent.org/fileadmin/documents/en/Change_Report/05_DocumentationChanges_20130904.pdf>`_, plus the fact that some LCIA results have changed a lot, leads many to doubt whether they should make the transition.

From my perspective, as someone who has played around with `LCA software <http://brightwaylca.org/>`_, the fact that the ecoinvent software is not publicly accessible is also a source of concern - especially ironic given the motto of the ecoinvent centre, to "trust in transparency." There were a lot of clarifications and modifications needed to turn the ideas of the data quality guidelines into working computer code, and these adaptations are just as important as the general data quality guidelines framework. It is my understanding that the ecoinvent centre is in the process of creating a new document that will more precisely give the rules for the application of the various system models, but this document is not yet finished.

One big step towards addressing these problems would be to have an open source version of the software that takes unit process master data sets and applies the different system models. If done properly, this software could provide a practical implementation of the abstract idea in the data quality guidelines, giving precise details on each step needed to get to the technosphere and biosphere matrices. In the rest of this post, I will give my thoughts on what such a software could look like.

Guiding principles
==================

The first guiding principle of any such software must be practicality. Even a simple piece of software is a lot of work, and ecoinvent 3 would not be a simple piece of software. Therefore, the software should have limited scope - not all of the ecoinvent software functionality is needed - and should not reinvent the wheel, but build on existing libraries as much as possible. One should start with the easiest problems, and build up a set of simplified components that can handle most unit processes. Practicality also means using a well-established, boring technology stack.

The second guiding principle should be accessibility. The inspiration behind `literate programming <http://en.wikipedia.org/wiki/Literate_programming>`_ should apply here as well - the point of such a software is not just to redo work already done, but to make the rules, algorithms, and special cases *understandable* to people from different backgrounds. The documentation for `backbone <http://backbonejs.org/docs/backbone.html>`_ is a beautiful example of annotated source code, but probably using something like `Sphinx <http://sphinx-doc.org/index.html>`_, e.g. `brightway2 documentation <http://brightway2.readthedocs.org/en/latest/>`_ is a better example, as numerous diagrams and even animations may be necessary. Development should be open, and source code should be hosted on a service like `github <https://github.com/>`_ or `bitbucket <https://bitbucket.org/>`_.

Of course, the cooperation of the ecoinvent centre would be critical for the success of any such effort. There are good arguments for having software development happen independent of ecoinvent, but probably the best approach would be to have a diverse team of people from inside and outside the ecoinvent centre.

Software components
===================

The first major component is a data converter, to convert from the ecospold 2 XML format to something more easily accessed and manipulated. XML is a great format for inventory dataset exchange, as it has schema descriptions, validation, etc. but XML is not a great format for working with data. Just google for XML and awful or horrible or terrible or sucks. Anyway, the converter would transform the necessary parts of the unit process datasets to the native data structures of whatever programming language is chosen.

The second major component, and the hardest one, is the allocator. This would take as an input an inheritance tree of unit process data sets, and resolve each into an allocated, single output unit process (A-SOUP, terminology by Gabor Doka), whose output is a product located in time and space. This can start simple - just work on economic or mass allocation, or just substitution. In theory, or in a world where no one had invented allocation at the point of substitution, this could be trivially parallelized, and so should be relatively quick. At the beginning, the software doesn't need to do everything, and difficult data sets like clinker production could just be skipped for now.

The last big component is the linker, which matches demand for products to the A-SOUPs that produce those products in the correct time and space. I think that this should be relatively easy to do. One improvement over the procedure as illustrated in the data quality guidelines could be to define all geographic relations in advance, even in something as simple as a text file, to avoid having to integrate GIS functionality into the new software (see also `Some thoughts on Ecoinvent geographies <http://chris.mutel.org/thoughts-ecoinvent-geo.html>`_).

I envision the final codebase to have more tests than actual code, and significantly more documentation than actual code.

A brighter future
=================

My best guess is that such a software would take around one year of work. The hard stuff has already been done by ifu hamburg and the ecoinvent centre. However, translating the work that has already been done into open source code will depend on a detailed specification document explaining exactly what the current software does.

If such a software were to come into existence, it could significantly help the adoption of ecoinvent version 3. It could also provide a nice foundation for future work. One of the very nice properties of the master unit process datasets is that one can develop new system models. A well-documented and well-tested open source software would allow both ecoinvent and others to develop new system models, and realize the promise of ecoinvent version 3.
