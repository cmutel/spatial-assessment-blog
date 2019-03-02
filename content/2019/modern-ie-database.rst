What would a modern Industrial Ecology database look like?
##########################################################

:date: 2019-02-24 23:45
:category: bonsai
:slug: modern-ie-database
:summary: What we do differently if we could start over

.. figure:: images/sunrise.jpg
    :alt: From https://www.flickr.com/photos/dennis/6411630783
    :align: center

Life cycle assessment has a number of inventory databases, both commercial and freely available. Material flow assessment doesn't really have any managed databases, though most people use STAN, which facilitates data exchange. We see a clear `community desire for open IE data <https://is4ie.org/opendata>`__, but it is hard to shake researchers, practitioners, and database developers out of their old habits. Moreover, technical debt means that it is difficult for long-established systems to change. If we could start with a blank sheet of paper, and design a database that would work for both supply chain analysis (LCA) and material flows and stocks, what principles and ideas would we emphasize? The following is my personal answer to this question.

First, we would design the database as a community resource. This means that decisions on small and large things would be discussed and voted on by the community, and clearly documented and communicated. All aspects of the database would be open, from the data processing pipeline and tools to the developers mailing list and budget. Moreover, there would not be a single database, but a variety of database flavors that fit different system modelling assumptions or research needs - however, all flavors would be derived from a common set of input data statements.

Second, the entire thing would be free and open - open source code, only open data, and open management. Openness is both a good in itself, and a necessity if our results are to be taken seriously and used to inform decisions that will affect us all. But openness also means making it easy for everyone to contribute. That means the process for entering data has to both intuitive and quick, and that people can see the results of their contributions in a reasonable timeframe.

Third, the process of gathering or improving data should be purposeful. Though we should be open to any data provided, the focus of the organization should be tailored to reducing overall uncertainty. Of course, we will need to have a status page documenting key areas of uncertainty, as well as other validation metrics that give us an indication of how much our database is simply missing.

Finally, our database should have high quality. To my mind, this means an emphasis on comprehensive documentation and quantification of uncertainty and variability, and the ability to break away from linear dynamics where necessary. Although linear systems are convenient, we should also support complex models which generate data for inventory datasets of material flows.

If one considers the amount of useful data available to industrial ecologists, much less than one tenth of that data ends up used in IE research. Another order of magnitude is lost when one considers the data published in IE studies. And at least one additional order of magnitude is lost when filtering the data which will eventually end up in a database. One could see this as a tragedy - needless and inconsistent repetition of effort, and a failure to seize chances right in front of us. But I chose to see this as an opportunity. Together, we have at least 1000 times more data than we think, and today we have both the technology and the people to turn this idea into reality.

I hope to help the `BONSAI team <https://bonsai.uno/>`__ to follow these principles during the next few years. I don't know if BONSAI will succeed in its ambitions, but I am absolutely convinced that we should try, and BONSAI, with its broad team, diverse skill set, and founding philosophy, is our best chance. Please contact me if you want to know more.
