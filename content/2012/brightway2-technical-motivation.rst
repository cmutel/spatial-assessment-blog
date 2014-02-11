Brightway2 - the technical motivation
#####################################

:date: 2012-12-02 12:00
:category: brightway2
:slug: brightway2-technical-motivation
:tags: notable
:summary: The technical reasons for the development of Brightway2

I spent years of my PhD working on what became Brightway version 1. In this post, I want to talk briefly about the technical reasons for starting over with Brightway2. `Brightway2 <http://brightwaylca.org>`_ is a set of packages which together act as a framework for LCA computations, visualization, and interpretation.

Brightway was a quintessential academic project, and was starting by someone (myself) with too little experience. It was a mess of spaghetti code, and grew worse with time. More problematic was that Brightway gained features through the creation of multiple branches, and the result was that there was no Brigtway, but rather a number of slightly varying codebases, all of which were Brightway.

One additional mistake was the lack of focus in Brightway. I would spend a week or two developing some of the funcationality needed for Brightway to scale to hundreds of people (e.g. `a module for storing directed acyclic graph in Postgres <https://bitbucket.org/cmutel/django-directed-acyclic-graph>`_). But most of the basic functionality was always missing, and Brightway was never really used by anyone except for myself. I didn't have the time or knowledge to build the next SimaPro by myself. The use of `Django <https://www.djangoproject.com/>`_ was part of this lack of focus. Django is great, but difficult to integrate with other Python packages (because of the settings file). The end result was that Brightway was a like many projects of passion - large, complex, impossible to comprehend or even remember the whole thing at once, and incomplete.

Brightway2 started with the realization that the good parts were getting lost in the noise and chaos of the first version, and that a new beginning was necessary to focus on the good bits. In particular, Brightway had a strong computational engine (including regionalized LCA). These strengths could be put into a simple package that would be much more relevant to contemporary problems in the LCA world.

Here are the key ideas of Brightway2:

* It is small. Brightway2 is not a complete LCA program - it is a set of tools to do advanced LCA calculation and visualization. Everything about Brightway2 should be limited, from the scope of each package to the number of lines of code. There are currently no user interface for editing or creating data - the assumption is that you have done this already, and just need to import data and make calculations. Brightway2 is also not intended for team use - it runs best by itself on your computer. Dependencies were eliminated whenever possible, to make installation (especially on Windows) easier. There is no database, just a directory with a bunch of files, making installation and backup easy as well.
* It is modular. Instead of one big gelatinous mass of a program, each set of functions is split into a package, with its own tests and documentation. These packages are not completely independent, but the most important functions and methods are written to accept generic inputs, to make it easier to understand and test. Modularity dramatically decreases the activation energy needed for someone to contribute to this open source project.
* It is agile. Because each database is just a file, it is trivial to copy a database, or email it to your friend. The data in a database is pure python, so it is possible to easily add or remove attributes, map and reduce the data, or apply whatever transformation you dream up.

The summary is that there was some good code and some good ideas for analysis and visualization which were languishing in a mess of a codebase, and a new, almost stupidly simple framework was needed to share these good bits with the LCA community. My hope is that Brightway2 can accomplish three things:

#. Be a useful tool or software library for people interested in doing advanced LCA work.
#. Act as a reference implementation of interesting LCA calculations.
#. Be a simple tool for everyday LCA practitioners who want to do some analysis not available elsewhere.
