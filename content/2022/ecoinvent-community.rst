A few ideas on how to make ecoinvent work better
################################################

:date: 2022-06-15-22:00
:category: ecoinvent
:status: draft
:slug: a-better-ecoinvent-community
:summary: Ecoinvent is the best option for a world where LCA provides high quality decision support. Let's help it get there.

.. figure:: /images/barn.jpg
    :align: center
    :alt: From https://www.flickr.com/photos/grongar/4966015822/

The ecoinvent center plays a dual role as a both a private firm and a community resource. Legally, the ecoinvent centre is a non-profit association (*Verein* in German), though membership in this association is not open. In most respects, the centre acts as a private firm, with (`as of May 1 2022 <https://ecoinvent.org/welcome-nic/>`__) a CEO, an employee base, and a range of contracts for data licensing and development. But the roots of ecoinvent lie in five research institutes in Switzerland deciding to work together to produce a single, consistent database, and making that data usable and useful for the broader community. Though it may not be obvious to many, the staff at the ecoinvent centre are very active in a range community-oriented activities, from international working groups to projects building up capacity in lesser developed countries, a lot of which is done pro bono.

The ecoinvent centre also relies on the community for its resources. Most directly, of course, are licensing revenues, but also data provision. Some data is provided for free, and some data is paid for by ecoinvent. But there are few, if any, datasets added to ecoinvent in the last ten years which were developed by its staff alone. In many cases, even when data gathering is compensated, the payments do not cover the actual costs involved.

Over time, as the database has grown in size and complexity, the license fees for ecoinvent have gone up. The ecoinvent centre itself has also grown, from around two people 15 years ago to more than 20 people today. The ecoinvent staff do a lot, but to outside eyes it isn't clear why there are so many people, and what they all do. Therefore, my first suggestion for the new management is:

1. The ecoinvent centre depends on the goodwill of the broader community. While they do a good job being active on social media, they could do more to advertise all the `constructive work <https://ecoinvent.org/activities/>`__ they do behind the scenes.

In researching this post, I have seen more and more material from ecoinvent in the direction suggested above, and I am not sure what more they actually could do. But I talk to enough people to know that this communication could be improved (somehow).

Speaking of user engagement, the `ecoinvent forum <https://forum.ecoinvent.org/forum/forum-for-ecoinvent-version-3.html>`__ is, shall we say, `resting <https://www.youtube.com/watch?v=vZw35VUBdzo>`__. While there may have been good reasons for this decision, it leaves the `LCA discussion list <https://support.simapro.com/articles/Article/LCA-Discussion-List>`__ as the unofficial place to get ecoinvent questions answered in public. The LCA discussion list has a lot of benefits, but does not always lead to productive conversations.

2. Ecoinvent should establish a forum using `discourse <https://www.discourse.org/>`__. It's free and open source, and easy to set up.

That was pretty vanilla, let's make it a bit spicier. The ecoinvent centre is an association, and the highest decision-making body in an association is the general assembly of the members. In order to avoid "incorrect" decisions, the five founding institutes decided to limit membership in ecoinvent. But this structure feels a bit weird - an association devoted ultimately to the goodwill of the community, and with a mutual interdependence with the community, but where the community has no formal role in or window into decision making. Therefore:

3. The ecoinvent user community should have an ombudsman.

And:

4. Minutes of the ecoinvent expert working groups, and other non-sensitive meetings should be made public.

Decisions by ecoinvent staff on specific datasets, and on broader system modelling aspects, have a huge impact on users of the ecoinvent database. It would be nice for researchers, and reassuring for the broader community, to have these decisions explained in a formal way. For example, the Brightway community has a `proposal template <https://github.com/brightway-lca/enhancement-proposals/blob/main/proposals/0001-bep-template.md>`__ for any change which adds a substantial new feature or makes a breaking change. The Brightway template (based on the `Python template <https://peps.python.org/pep-0012/>`__), includes alternatives to the option selected, reasons for rejecting the alternatives, and a testing strategy for ensuring that the chosen solution will work as expected. One could even have a comment period for broader public input if you want to really embrace community engagement. Such a decision-making template would help ecoinvent communicate the details of changes which affect everyone. A recent example of such a change is the addition of a new system model, `EN15804 <https://eplca.jrc.ec.europa.eu/LCDN/EN15804.xhtml>`__ - I am quite confidant that the implementation of this model involved some subjective decisions which would be of extreme interest to people like myself, but are (AFAICT) currently locked in proprietary computer code.

5. Adopt, strictly use, and subsequently disseminate a template for systematically important decision making.

People make mistakes. This is normal and expected. Mistakes give us the opportunity to learn, and to improve processes to avoid similar mistakes in the future. One of the value propositions of the ecoinvent database is the rigorous system of quality control before data enters the database, but despite these checks, there have been some mistakes in recent releases. For example, the LCIA implementation in the 3.8 release used the elementary flow names from 3.7. A bigger issue was the global production volume of electric arc furnace low-alloyed steel in 3.7, which was much too high, leading to the global mix of low-alloyed steel being 76% from electric arc furnaces (with *much* lower impacts than primary steel); this number was fixed in 3.8 to the correct value of 26%.

Here are the relevant datasets if you are curious:

    - `3.7.1 market for steel, low-alloyed <https://v371.ecoquery.ecoinvent.org/Details/UPR/0b720099-0af4-49a6-8608-9686dccac357/290c1f85-4cc4-4fa1-b0c8-2cb7f4276dce>`__

    - `3.7.1 steel production, electric, low-alloyed <https://v371.ecoquery.ecoinvent.org/Details/UPR/fe0414ff-f3cd-4e94-8a10-e12c1a616920/8b738ea0-f89e-4627-8679-433616064e82>`__

    - `3.7.1 steel production, converter, low-alloyed <https://v371.ecoquery.ecoinvent.org/Details/UPR/b06c4e66-fdcb-4017-bf57-5b412b215e17/8b738ea0-f89e-4627-8679-433616064e82>`__

    - `3.8 market for steel, low-alloyed <https://v38.ecoquery.ecoinvent.org/Details/UPR/a27d8ca4-2de1-47d7-850c-9a93e3ad6506/290c1f85-4cc4-4fa1-b0c8-2cb7f4276dce>`__

    - `3.8 steel production, electric, low-alloyed <https://v38.ecoquery.ecoinvent.org/Details/UPR/27ee6a9c-2439-44c8-9d1a-9e921b21f776/8b738ea0-f89e-4627-8679-433616064e82>`__

    - `3.8 steel production, converter, low-alloyed <https://v38.ecoquery.ecoinvent.org/Details/UPR/7a3148a5-f1f0-4ad4-9ec1-240166dcb7cc/8b738ea0-f89e-4627-8679-433616064e82>`__

In technology companies, it is `common <https://www.atlassian.com/incident-management/handbook/postmortems>`__ `practice <https://blog.cloudflare.com/tag/postmortem/>`__ to do a `blog <https://medium.com/asos-techblog/playing-the-blame-less-game-3708f8195344>`__ `post <https://cloud.google.com/blog/products/gcp/fearless-shared-postmortems-cre-life-lessons>`__ after a major incident explaining what caused the problem, and more importantly how this class of problems will be avoided in the future. The point is not to lay blame but to find constructive solutions - one must plan for humans to be, well, human.

6. There should be a standard procedure when errors are discovered, including a public acknowledgement, and a postmortem investigation focused on how such errors can be prevented in the future.

Finally, some data in ecoinvent is public, either because it was `funded by agencies who wanted open data <https://ecoinvent.org/activities/sri-project/>`__, or because individual data sets were paid for in order to make them open. But it is very difficult to find such open data. I don't know of a definitive list of open datasets, and the SRI data page has a `broken license agreement link <https://ecoinvent.org/files/ecoinvent_association_-_sri_open_data_license_agreement_-_20190927_web.pdf>`__ and separate registration system which seems broken for now. Instead of being reluctant about this open data, ecoinvent could embrace it, and in particular make sure that such open data was `FAIR <https://en.wikipedia.org/wiki/FAIR_data>`__.

7. All open data from ecoinvent should be showcased and follow FAIR principles.

*Note: This post was based off a presentation given in 2021 at an LCA discussion forum. All opinions are my own.*
