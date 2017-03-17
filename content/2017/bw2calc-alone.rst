Running ``bw2calc`` as a web service
####################################

:date: 2017-03-17 7:00
:category: brightway2
:slug: bw2calc-alone
:summary: A minimal implementation of a standalone bw2calc web service

.. figure:: images/scaffold.jpg
    :alt: Creative commons, https://www.flickr.com/photos/frosch50/14352991372
    :align: center

Linking Brightway2 to a Ruby on Rails UI
========================================

Caroline Chen, a Masters student at UC Berkeley, recently asked me how to link a `Ruby on Rails <http://rubyonrails.org/>`__ user interface to Brightway. This kind of project should be easy - it was one of the design goals of the Brightway project. This idea of a number of independent modules that can work independently with each other is also my hope for the future of LCA software development, though it will take some work and commitment by the broader community to get there.

There are a number of ways to accomplish this goal using Brightway. If you are building your own user interface, you already have your own database schema. ``bw2calc`` doesn't talk directly to databases, but instead uses an `intermediate format made of Numpy arrays <https://docs.brightwaylca.org/intro.html#intermediate-and-processed-data>`__. In order to understand this post, you should also read the `processed arrays technical documentation <https://docs.brightwaylca.org/lca.html#turning-processed-data-arrays-in-matrices>`__, as I won't repeat everything here. So, the challenge is exporting the data from your database to a processed array, sending that array to a process on a server running ``bw2calc``, and receiving meaningful result data.

Sending data as a CSV file
--------------------------

I want to explain a minimal implementation here - if you were running this as a real service, you would probably change almost every technical decision. To make life easy, we can export a CSV file from the database and send that to the server - we will let the python process on the server construct the processed array. So, if we have a database schema for the edges in our supply chain graph that looks like this:

.. code-block:: sql

    CREATE TABLE "edges" (
        "id" INTEGER NOT NULL PRIMARY KEY,
        "from" FOREIGN KEY ...,
        "to" FOREIGN KEY ...,
        "type" INTEGER,
        "amount" FLOAT,
        ...
    )

Then we can export a CSV with the relevant data to construct the LCI matrices like this:

.. code-block:: bash

    sqlite3 -csv some_db.db "select from, to, type, amount from edges where ...;" > lci.csv

The only tricky thing here is that Brightway has a mapping that from edge types to integers: Edge type 0 is a production edge, 1 is a technosphere flow, and 2 is a biosphere flow, where "from" would be a foreign key to a biosphere flow and "to" would be the activity emitting/consuming that flow. Of course, you could have a schema where technosphere and biosphere edges were stored in separate tables.

You can do a similar thing for characterization factors; I assume they have a separate table. Here is some Python 3 code that simulates an export by writing very simple LCI and LCIA files.

.. code-block:: python

    import csv

    ELEC = 1
    COAL = 2
    CO2 = 3

    LCI = [
        (ELEC, ELEC, 0, 1), # Production
        (COAL, COAL, 0, 1), # Production
        (COAL, ELEC, 1, 0.1),
        (CO2,  COAL, 2, 2)
    ]
    LCIA = [(CO2, 1)]

    def export_lci():
        with open("lci.csv", "w") as f:
            writer = csv.writer(f)
            for row in LCI:
                writer.writerow(row)

        with open("lcia.csv", "w") as f:
            writer = csv.writer(f)
            for row in LCIA:
                writer.writerow(row)

Receiving the CSV file
----------------------

Next, we need to write a web server that will accept a CSV and generate the processed arrays. I have already worked with the `flask <http://flask.pocoo.org/>`__ web framework, so I will use that here. We start by defining the data types in our arrays - these are fixed by Brightway:

.. code-block:: python

    import numpy as np
    import os
    import csv

    LCI_DTYPE = [
        ('input', np.uint32),
        ('output', np.uint32),
        ('row', np.uint32),  # We don't know the row and column indices, these will
        ('col', np.uint32),  # be filled in by the matrix generator
        ('type', np.uint8),
        ('amount', np.float32),
    ]
    LCIA_DTYPE = [
        ('flow', np.uint32),
        ('geo', np.uint32),
        ('row', np.uint32),
        ('amount', np.float32),
    ]
    MAX_INT_32 = 4294967295  # Used for values that will be filled in during the LCA calculation

The translation function is relatively simple - here it is for the LCI array:

.. code-block:: python

    arr = np.array([
        (int(inp), int(outp), MAX_INT_32, MAX_INT_32, int(typ), float(amnt))
        for inp, outp, typ, amnt in csv.reader(TextIOWrapper(request.files['lci']))
    ], dtype=LCI_DTYPE)
    np.save(os.path.join(dirpath, "lci.npy"), arr, allow_pickle=False)

Things to note here:

* We are sending the CSV files as file attachments, not as form data. In this case, the LCI file was sent as the attachment named 'lci'.
* We have to wrap the file object in `TextIOWrapper <https://docs.python.org/3/library/io.html#io.TextIOWrapper>`__ to get text instead of bytes.
* We use the fill-in value ``MAX_INT_32`` for the ``row`` and ``col`` columns.
* We convert to ``float`` or ``int`` based on our data type schema.
* I saved the file to the directoy ``dirpath``, which is undefined for now - this can be e.g. a temporary directory.

Running an independent LCA
--------------------------

An independent LCA means that the ``bw2calc`` library doesn't use bw2data or other Brightway libraries. This is also relatively simple, as we already have our processed arrays somewhere on our system:

.. code-block:: python

    from bw2calc import IndepentLCAMixin, LCA as _LCA
    import os

    class LCA(IndepentLCAMixin, _LCA):
        """With this LCA class, we provide the array filepaths directly"""
        pass

    config = {
        'demand': {some_functional_unit_id: 1},
        'database_filepath': [os.path.join(dirpath, "lci.npy")],
        'method': [os.path.join(dirpath, "lcia.npy")],
    }

    lca = LCA(**config)
    lca.lci()
    lca.lcia()
    print(lca.score)

The definition of the functional unit needs to use the same identifiers as in our CSV file. So, if we were assessing the ELEC process, this would be ``{1: some_amount}``.

Defining the web API
--------------------

All that is left is defining exactly what the API calls will look like. One possibility would be to specify the functional unit in the form data. I have made a complete example of `one such web server program <https://gist.github.com/cmutel/a408e3a62f35519065cee125d7821d4d>`__, as well as `a corresponding script that calls this web server <https://gist.github.com/cmutel/35e77f3e6902e9d383ca6f24c920e177>`__. However, the API is an area where your personal preferences might be quite different than mine, so adapt as you wish.

Future development
==================

I should emphasize that this is really just a minimal server - it is missing a lot of error handling, and returns a very minimal result set. There are a number of ways that this could be improved. Here are a few ideas off the top of my head:

* Send processed arrays directly to reduce traffic over the network and processing time on the server
* Expand the result data to include contribution analysis (not hard, just sum ``characterized_inventory`` rows and columns) and even Monte Carlo (would require an expanded array data type).
* Package the server in a Docker container and scale on demand.
* Access control and/or rate-limiting.
