Brightway backwards
###################

:date: 2025-04-13-12:00
:category: brightway
:slug: brightway-from-the-bottom-up
:summary: A way-too-detailed look at how Brightway actually works

.. figure:: /images/inner-workings.jpg
    :align: center
    :alt: https://www.flickr.com/photos/el_ramon/8109601643/

In this post, we will look at Brightway backwards - from the pure math back to the data entry and storage steps. This post will be long, and go into detail on exactly how Brightway works in April 2025. There is `a companion notebook <https://github.com/cmutel/spatial-assessment-blog/blob/master/notebooks/Backwards.ipynb>`__ which has all the code used here in a single convenient place.

Building the matrices
=====================

We will assume that we are modelling a linear system, i.e. one where there are strict linear relationships between inputs and outputs, and where each production function can supply an infinite amount of its reference product. These are assumptions which don't hold in the real world, but are relatively standard in life cycle assessment.

Let's imagine a very simple system - the production of a steel bicycle. In our example system we can write two equations, one each for the production of the bicycle and the production of the steel tubes used to make the bicycle. We can write the equations however we want, but in this case we will use the convention that inputs are on the left and outputs on the right:

.. figure:: /images/lca-equations-1.png
    :align: center
    :height: 90px

CO2 is an output - it's emitted by the processes. The steel tubes come for free because we are making the example simple.

Let's see what happens if we move everything over to the right hand side:

.. figure:: /images/lca-equations-2.png
    :align: center
    :height: 60px

Here we have already discovered a very important concept - we will have positive and negative numbers in our equations, and therefore we need a **sign convention** that is applied consistently and that we can understand. Brightway uses the following sign convention:

* Products which are consumed have a negative number
* Products which are produced have a positive number
* Elementary flows are special

Traditionally elementary flows have an environmental context - something like ``emissions to air`` or ``natural resources``. The implication of this tradition is that, in some contexts (like ``natural resources``), elementary flows **being consumed are positive**, while in other contexts (like ``emissions to air``) elementary flows **being released are also positive**. This tradition is the exact opposite of how we treat products, but because it is followed by all inventory databases and impact assessment methods that I know of (characterization factors are positive, even if they are characterizing resource consumption), it is easier to follow this convention than risk introducing errors by changing numbers.

It would be nicer to have a single consistent sign convention.

Because we are modelling this as a linear system, we can put these coefficients into a matrix. Brightway also has a convention here: **processes** are columns, and **products** or **elementary flows** are rows.

.. figure:: /images/lca-equations-3.png
    :align: center
    :height: 120px

We don't have to put zeros in places where we don't have data - we will be building a `sparse matrix <https://en.wikipedia.org/wiki/Sparse_matrix>`__, where empty elements are assumed to be zero.

However, we can't use this equation to solve :math:`\textbf{A}x=f` because our matrix isn't square - it has three rows and two columns. Instead, we can split this matrix into two different matrices. Brightway calls these the technosphere and the biosphere matrices:

.. figure:: /images/lca-equations-4.png
    :align: center
    :height: 130px

If we want to do impact assessment, then we also need a characterization matrix. This matrix turns the physical elementary flows into whatever unit of damage the impact category is describing - for example, Comparative Toxic Units instead of kilograms. This characterization matrix, :math:`\textbf{C}`, has both rows and columns of elementary flows, and only has numbers on its diagonal. Each number in the characterization matrix is, like everything else, a linear coefficient.

We have a lot of the number ``1`` already - let's do characterization in grams of CO2-equivalent. Our characterization factor would therefore be 1000 gram CO2-equivalent per kg of CO2:

.. figure:: /images/lca-equations-5.png
    :align: center
    :height: 100px

Before we figure out how to build this system in Brightway, let's look at how we could solve this simple system manually. Our technosphere matrix is the :math:`\textbf{A}` in :math:`\textbf{A}x=f` - what are the other values? :math:`f` is the **demand** array, which specifies how much of each possible **product** we want, and :math:`x` is the **supply** array - the amount of each **process** needed to supply the demand, and the result of solving :math:`\textbf{A}x=f`. We don't know :math:`x` until we do some math, but we get to choose :math:`f`. Let's do a calculation for 5 bikes and nothing else. We would then have:

.. figure:: /images/lca-equations-6.png
    :align: center
    :height: 120px

What values do we need in :math:`x` to satisfy our demand? If we start with the first row, we can see that we need to scale the bike making process by 5 to get enough bike product to meet the demand. Our first value in :math:`x` is therefore 5.

We now have a problem - our demand vector doesn't ask for any steel tube production, but by scaling the bike production by 5, we now have -12.5 (note the **negative**) kilograms of steel tube, not zero kilograms. We can now scale the steel tube process up to produce enough steel tubes to **cancel out** this negative number. The scaling factor is 12.5, because each time the steel tube making process is run it produces 1 kilogram of steel tubes. We have now solved our linear system and can put in the correct values for :math:`x`:

.. figure:: /images/lca-equations-7.png
    :align: center
    :height: 100px

Humans make lots of mistakes, so let's put this data in the computer and make sure we have the right answer. We will start with a dense Numpy array first:

.. code-block:: python

    import numpy as np
    A = np.array([
        (1,    0),
        (-2.5, 1)
    ])
    f = np.array((5, 0))
    np.linalg.solve(A, f)
    >>> array([ 5. , 12.5])

The solvers we will use do something similar, but use tricks to make it possible to solve very large systems quickly.

The induced scaling of the steel-making process is also how substitution works - if we had a process which produced two products (two positive numbers), but our demand was only for one of them, then another process would have to decrease (have a negative scaling factor) to zero out the production of the second good. That's why there is **no mathematical difference between production and substitution** - we just use different labels to show the intent of the modeller.

In real practice, we will have large and pretty sparse technosphere matrices, so let's see how this would work with a Scipy sparse matrix instead of a dense Numpy array. This will require a bit more work - Brightway uses the constructor from Scipy which looks like this:

.. code-block:: python

    from scipy.sparse import csr_matrix
    csr_matrix((data, (row_ind, col_ind)), [shape=(M, N)])

Where:

* ``data`` is a 1-d Numpy array with the non-zero elements in the technosphere matrix
* ``row_ind`` is a 1-d Numpy array in the same order as `data`; `row_ind[x]` give the row index of `data[x]`.
* ``col_ind`` is a 1-d Numpy array in the same order as `data`; `col_ind[x]` give the column index of `data[x]`.
* ``(M, N)`` are the number of rows and columns in the matrix. Because we don't specify values of zero, the matrix could be larger than the rows and columns given in the preceding arrays if there are columns or rows completely filled with zeros.

The ``row_ind`` and ``col_ind`` can be confusing. They are all one-dimensional, and have the same length. The way I remember how it works is: if element ``7`` of ``data`` is ``3.141``, element ``7`` of ``row_ind`` is ``11``, and element ``7`` of ``col_ind`` is ``56``, then we know that in row ``11`` and column ``56`` of the matrix being built there will be a value of ``3.141``.

The CSR sparse matrix constructor has a very nice property - you can specify **multiple values** for the same matrix element, and these values will be added together. In the LCA context, this means we can specify that a given process produces one kilogram of product, but also loses a small amount due to spoilage, and the matrix constructor will automatically give us the correct net production amount.

.. code-block:: python

    import numpy as np
    from scipy.sparse import csr_matrix

    data = np.array([1, -0.1])
    row_ind = np.array([0, 0])
    col_ind = np.array([0, 0])
    shape = (1, 1)
    matrix = csr_matrix((data, (row_ind, col_ind)), shape=shape)
    matrix.todense()
    >>> matrix([[0.9]])

In our example, our data array would have three values - the non-zero elements of the matrix. The row and column indices should be in the same order as the data, and keep in mind that Python starts indices with zero. So our first non-zero value is ``1``, in row ``0`` (we start counting with zero) and column ``0``. The next is ``-2.5``, in row ``1`` and column ``0``. Finally, we have the data value ``1``, in row ``1`` and column ``1``:

.. code-block:: python

    import numpy as np
    from scipy.sparse import csr_matrix

    data = np.array([1, -2.5, 1])
    row_ind = np.array([0, 1, 1])
    col_ind = np.array([0, 0, 1])
    shape = (2, 2)
    matrix = csr_matrix((data, (row_ind, col_ind)), shape=shape)
    matrix.todense()
    >>> matrix([[ 1. ,  0. ],
    >>>         [-2.5,  1. ]])

The best sparse solver depends on your CPU architecture. If you don't have the best solver for your CPU, Brightway will let you know:

.. code-block:: python

    from bw2calc import spsolve
    >>> It seems like you have an ARM architecture, but haven't installed scikit-umfpack:
    >>>
    >>>     https://pypi.org/project/scikit-umfpack/
    >>>
    >>> Installing it could give you much faster calculations.
    >>>
    >>>   warnings.warn(UMFPACK_WARNING)

We can then use the solver to solve our linear problem:

.. code-block:: python

    from bw2calc import spsolve
    spsolve(matrix, b)
    >>> array([ 5. , 12.5])

Indexing in matrices
--------------------

We have cheated a bit so far - we have assumed that we know **where** the data should go in the matrix - the matrix row and column indices for each value. But this isn't really true. Our data comes from some sort of database, and that database has its **own way of constructing ids**. Many times this would start with an sequential integer id starting from one, but Brightway uses `Snowflake IDs <https://en.wikipedia.org/wiki/Snowflake_ID>`__:

.. code-block:: python

    from bw2data.snowflake_ids import snowflake_id_generator
    next(snowflake_id_generator)
    >>> 169741598115975168

Brightway uses Snowflake IDs because they can be generated client side instead of only in the database and are sortable by creation time.

Brightway assumes that database ids are positive integers, but imposes no additional restraints, and allows for 64 bit integers.

The library ``matrix_utils`` has mapping functions from database ids to matrix row and column indices.

Let's pick some arbitrary database ids for our processes and products:

* Process ``bike_making``: 555555555
* Process ``steel_tube_making``: 666666666
* Product ``bike``: 123456789
* Product ``steel_tubes``: 111111
* Elementary flow ``CO2``: 1

We can then let Brightwy do the translation to matrix indices:

.. code-block:: python

    from matrix_utils import ArrayMapper
    import numpy as np

    bike_making = 555555555
    steel_tube_making = 666666666
    bike = 123456789
    steel_tubes = 111111
    CO2 = 1

    am = ArrayMapper(array=np.array([bike_making, steel_tube_making, bike, steel_tubes, CO2]))
    am.map_array(np.array([steel_tubes, bike]))
    >>> array([1, 2])

``ArrayMapper`` works by sorting the set of unique inputs, and mapping them to a range of increasing integers from zero to the number of unique inputs. In the above example, the database id ``steel_tubes`` is 111111, which is the second value in all the values sorted from smallest to largest (one is the second value, Python starts counting from zero).

Funnily enough, the ``ArrayMapper`` class actually `builds a sparse matrix <https://github.com/brightway-lca/matrix_utils/blob/a34841f2dd1fb4839fd849eb3d6f055494741624/matrix_utils/array_mapper.py#L62>`__ when it does this mapping from database ids to matrix indices, as this was the most efficient approach we found so far which can handle very large 64 bit integers.

In theory, one could skip this mapping step, as sparse matrices can include many rows of zeros. However, not everything is sparse - both the demand and supply arrays are dense matrices, and a dense matrix of 169741598115975168 elements would take 700 million GiB of RAM.

Let's simulate a system where our data came from the database - in this case we would have the database ids, and need to translate them to the matrix indices before feeding them to the CSR matrix builder. Here's how that would look with the example ids above:

.. code-block:: python

    from matrix_utils import ArrayMapper
    from scipy.sparse import csr_matrix
    import numpy as np

    bike_making = 555_555_555
    steel_tube_making = 666_666_666
    bike = 123_456_789
    steel_tubes = 111_111
    CO2 = 1

    process_mapper = ArrayMapper(array=np.array([bike_making, steel_tube_making]))
    product_mapper = ArrayMapper(array=np.array([steel_tubes, bike]))
    biosphere_mapper = ArrayMapper(array=np.array([CO2]))

    data = np.array([1, -2.5, 1])
    row_ind = product_mapper.map_array(np.array([bike, steel_tubes, steel_tubes]))
    col_ind = process_mapper.map_array(np.array([bike_making, bike_making, steel_tube_making]))
    shape = (2, 2)
    technosphere_matrix = csr_matrix((data, (row_ind, col_ind)), shape=shape)
    technosphere_matrix.todense()

    >>> matrix([[-2.5,  1. ],
    >>>         [ 1. ,  0. ]])

Note that we use different mappers for the different dimensions (process/product/biosphere).

This result matrix is the same but different - the row order is flipped. In Brightway, the `matrix diagonal is a construct <https://chris.mutel.org/zero-digonals.html>`__ - it doesn't have the same meaning as in IO analysis. This is because our rows are **products** and our columns are **processes**, and we have no guarantee that these two lists are in the same order when sorted.

Standard LCA Matrices
---------------------

In addition to the technosphere matrix, standard matrix-based LCA includes the biosphere matrix (relates processes to their elementary flows) and the characterization matrix. These are all sparse matrices, and are constructed in the same way as the technosphere matrix.

Keep in mind the sign convention for the biosphere matrix - most value are positive, even if they are resources being consumed by a process.

.. code-block:: python

    from matrix_utils import ArrayMapper
    from scipy.sparse import csr_matrix
    import numpy as np

    bike_making = 555_555_555
    steel_tube_making = 666_666_666
    CO2 = 1

    process_mapper = ArrayMapper(array=np.array([bike_making, steel_tube_making]))
    biosphere_mapper = ArrayMapper(array=np.array([CO2]))

    data = np.array([0.1, 2])
    row_ind = biosphere_mapper.map_array(np.array([CO2, CO2]))
    col_ind = process_mapper.map_array(np.array([bike_making, steel_tube_making]))
    shape = (1, 2)
    biosphere_matrix = csr_matrix((data, (row_ind, col_ind)), shape=shape)

    data = np.array([1000])
    only_ind = biosphere_mapper.map_array(np.array([CO2]))
    shape = (1, 1)
    characterization_matrix = csr_matrix((data, (only_ind, only_ind)), shape=shape)

    biosphere_matrix.todense(), characterization_matrix.todense()
    >>> (matrix([[0.1, 2. ]]), matrix([[1000]]))

With these matrices we already have enough to do an LCA calculation. The standard formula, assuming that the characterization matrix is diagonal and only includes a single impact category, is:

.. math::
    h = CBA^{-1}f

where:

* :math:`\textbf{C}` is the characterization matrix
* :math:`\textbf{B}` is the biosphere matrix
* :math:`\textbf{A}` is the technosphere matrix
* :math:`f` is the demand array

We can manually calculate the answer before checking with the computer - for our functional unit of five bikes, we need to scale bike production five times, which means :math:`0.1 \cdot 5 = 0.5` kilograms of CO2. This also needs the production of ``12.5`` kilograms of steel tubes, each of which emits ``2`` kilograms of CO2, making :math:`12.5 \cdot 2 = 25` kilograms of CO2 in total. Adding these together and multiplying by ``1000`` gives ``25500`` grams of CO2-equivalent.

.. code-block:: python

    bike_index = product_mapper.map_array(np.array([bike]))

    f = np.zeros(2)
    f[bike_index] = 5

    characterization_matrix @ biosphere_matrix @ spsolve(technosphere_matrix, f)
    >>> array([25500.])

Note that we have to be careful here getting the product demand in the right row, given our product mapping. The mapper tells us whether bikes are in row zero or one.

Datapackages: Persisting Matrix Data
====================================

It would be nicer if we had all this data in a prepared form, so we didn't need to build the mappers, arrays, etc. every time. The Brightway library `bw_processing <https://github.com/brightway-lca/bw_processing>`__ does exactly that: it defines a standard way of storing this data so it can be easily loaded into a matrix builder and used in calculations.

These `bw_processing` datapackages are based on the `frictionless data datapackage standard <https://specs.frictionlessdata.io/data-package/>`__, which defines how to attach data resources, and how to include and serialize metadata.

Let's put the data we have into a datapackage and use it in a calculation. First, we create an in-memory datapackage. `bw_processing` uses `fsspec <https://filesystem-spec.readthedocs.io/en/latest/>`__, which allows file storage on many kinds of filesystems, but in-memory is OK for now.

Next, we need to add the data to the datapackage. Because our libraries are designed to work together, it is relatively easy. The only major difference with what we did before is that we can glue the row and column indices together in one array - they are always in the same order and only used together, and so there is no reason to keep them separate.

We do this gluing by creating a Numpy `record array <https://numpy.org/doc/stable/reference/generated/numpy.recarray.html>`__ - a special kind of array where each row is defined by a tuple of ``(label, datatype)`` pairs. In our case it looks like this:

.. code-block:: python

    import bw_processing as bwp
    bwp.INDICES_DTYPE
    >>>[('row', numpy.int64), ('col', numpy.int64)]

This data is coming from the database, and uses database ids. We wouldn't want to map it to matrix indices in any case as we don't know what other background databases will be used, which means we don't know the size of the matrices or anything else about them yet.

Datapackages can include multiple resource groups, though all datapackages produced by Brightway will only include either inventory or impact assessment data. In this example we can put everything into a single datapackage:

.. code-block:: python

    import bw_processing as bwp

    technosphere_indices = np.array([
        # row, column
        (bike, bike_making),
        (steel_tubes, bike_making),
        (steel_tubes, steel_tube_making)
    ], dtype=bwp.INDICES_DTYPE)
    technosphere_data = np.array([1, -2.5, 1])

    dp = bwp.create_datapackage()
    dp.add_persistent_vector(
        matrix="technosphere_matrix",
        indices_array=technosphere_indices,
        data_array=technosphere_data
    )

    biosphere_indices = np.array([
        (CO2, bike_making),
        (CO2, steel_tube_making),
    ], dtype=bwp.INDICES_DTYPE)
    biosphere_data = np.array([0.1, 2])
    dp.add_persistent_vector(
        matrix="biosphere_matrix",
        indices_array=biosphere_indices,
        data_array=biosphere_data
    )

    characterization_indices = np.array([
        (CO2, CO2),
    ], dtype=bwp.INDICES_DTYPE)
    characterization_data = np.array([1000.])
    dp.add_persistent_vector(
        matrix="characterization_matrix",
        indices_array=characterization_indices,
        data_array=characterization_data
    )

You can see all the available information about one of the resource groups with:

.. code-block:: python

    next(group.metadata for _, group in dp.groups.items())

There is quite a lot!

.. code-block:: python

    {'profile': 'data-package',
     'name': 'd54118b9a0c64009aefe82cf10b46771',
     'id': 'ede8cb8ccf134732af7be138c07bbced',
     'licenses': [{'name': 'ODC-PDDL-1.0',
       'path': 'http://opendatacommons.org/licenses/pddl/',
       'title': 'Open Data Commons Public Domain Dedication and License v1.0'}],
     'created': '2025-04-10T20:35:11.305245+00:00Z',
     'combinatorial': False,
     'sequential': False,
     'seed': None,
     '64_bit_indices': True,
     'sum_intra_duplicates': True,
     'sum_inter_duplicates': False,
     'matrix_serialize_format_type': 'numpy',
     'resources': [{'profile': 'data-resource',
       'format': 'npy',
       'mediatype': 'application/octet-stream',
       'name': 'd9fc130dcfc6464e929950b56a0498d1.indices',
       'matrix': 'technosphere_matrix',
       'kind': 'indices',
       'path': 'd9fc130dcfc6464e929950b56a0498d1.indices.npy',
       'group': 'd9fc130dcfc6464e929950b56a0498d1',
       'category': 'vector',
       'nrows': 3},
      {'profile': 'data-resource',
       'format': 'npy',
       'mediatype': 'application/octet-stream',
       'name': 'd9fc130dcfc6464e929950b56a0498d1.data',
       'matrix': 'technosphere_matrix',
       'kind': 'data',
       'path': 'd9fc130dcfc6464e929950b56a0498d1.data.npy',
       'group': 'd9fc130dcfc6464e929950b56a0498d1',
       'category': 'vector',
       'nrows': 3}]}

This single datapackage is all we need to do an LCA calculation:

.. code-block:: python

    import bw2calc as bc

    lca = bc.LCA(demand={bike: 5}, data_objs=[dp])
    lca.lci()
    lca.lcia()
    lca.score
    >>> 25500.0

In normal Brightway usage we wouldn't start with an in-memory datapackage, but one which has already been written to the local filesystem. Let's trace the code flow on how Brightway would do this calculation given a functional unit and an impact category from the database.

First, Brightway would `look up the datapackages it needs for the given calculation <https://github.com/brightway-lca/brightway2-data/blob/551e975d8c530419ad75581f3935c5db44a27e35/bw2data/compat.py#L69>`__. This includes looking at the dependent datapackages needed for the functional unit (e.g. if you built your foreground data on top of Exiobase, this would be two different datapackages), as well as the datapackages for the impact category. A normal Brightway calculation would have between three and ten datapackages loaded.

The `bw2calc` library will `call the matrix_utils library <https://github.com/brightway-lca/brightway2-calc/blob/a51ac18348f22ada859e72f9d6c9a8774a4c0cb3/bw2calc/lca_base.py#L37>`__ to create `MappedMatrix <https://github.com/brightway-lca/matrix_utils/blob/a34841f2dd1fb4839fd849eb3d6f055494741624/matrix_utils/mapped_matrix.py>`__ instances from the datapackages for each matrix needed for the given calculation. The ``MappedMatrix`` class creates and stores the information needed to go from database ids to matrix indices (the ``ArrayMapper`` that we saw earlier), and makes sure that these are used consistently for all datapackages and matrices - the order of processes in the technosphere and biosphere matrices must be the same.

``MappedMatrix`` also allows for some functionality we won't discuss in this post, including specifying custom indexers, RNG seeds, dynamic matrix values, combinatorial sampling, and possibility arrays. See the `bw_processing documentation <https://github.com/brightway-lca/bw_processing>`__ for details on this functionality.

We also need to `borrow the product mapper from the technosphere matrix <https://github.com/brightway-lca/brightway2-calc/blob/a51ac18348f22ada859e72f9d6c9a8774a4c0cb3/bw2calc/lca.py#L205>`__ to correctly create the demand array.

Finally, Brightway doesn't actually calculate :math:`h = CBA^{-1}f`, because this collapses the result matrix to a single score. It can be quite helpful to instead look at the characterized inventory matrix, which has rows of elementary flows and columns of processes. Therefore we use this alternative equation:

.. math::
    h = CB \cdot diag ( A^{-1}f )

This gives us a characterized inventory result matrix with rows of elementary flows and columns of processes - the same form as the life cycle inventory matrix.

.. code-block:: python

    lca.characterized_inventory.todense()
    >>> matrix([[  500., 25000.]])

With the characterized inventory matrix, we can sum and sort all the columns to find the most damaging elementary flow (in the example it's CO2, there is only one elementary flow 😊), but we can do the same to the rows to find the most damaging process:

.. code-block:: python

    process_indices_by_damage = np.argsort(
        np.abs(
            lca.characterized_inventory.sum(axis=0).data
        ).ravel()
    )[::-1]

    [lca.dicts.activity.reversed[index] for index in process_indices_by_damage]
    >>> [666666666, 555555555]

This returns the **database ids** we defined earlier. and the order is what we would expect given that we know steel tube making (666666666) emits more CO2 than bike making (555555555).

Brightway supports a variety of uncertainty, scenario, and variant analyses, but they all boil down to the same mathematical trick - we want to change one or matrices by using different versions of the **data vector**, but **leaving the indices the same**. There is a lot of flexibility on how this is implemented, depending on whether the set of possible values in known in advance or generated dynamically, and the degree of value correlation across matrices (see for example `this <https://github.com/brightway-lca/from-the-ground-up/blob/main/2%20-%20Building%20and%20using%20matrices%20in%20bw2calc.ipynb>`__ and `this <https://github.com/brightway-lca/brightway2/blob/master/notebooks/Scenario%20analysis%20with%20uncertainty.ipynb>`__).

That's basically ``bw2calc`` and its support libraries. Let's turn to how Brightway stores data in a database.

Graph Database
==============

At is core, ``bw2data`` is a wrapper around SQLite used as a graph database, plus some metadata storage in JSON files. We have two main tables, one for nodes (currently called `activitydataset <https://github.com/brightway-lca/brightway2-data/blob/551e975d8c530419ad75581f3935c5db44a27e35/bw2data/backends/schema.py#L8>`__) and the other for edges (currently called `exchangedataset <https://github.com/brightway-lca/brightway2-data/blob/551e975d8c530419ad75581f3935c5db44a27e35/bw2data/backends/schema.py#L22>`__). Nodes are products, processes (including multifunctional processes), and elementary flow objects; Edges are directed qualitative or quantitative relationships between nodes.

Brightway's data model for edges kind of looks like the following. It isn't exactly this, but you should think of it like this:

.. code-block:: python

    from dataclasses import dataclass

    @dataclass
    class Edge:
        target: int  # database id
        source: int  # database id
        data: dict

Similarly, you should think of nodes as following this simple data model:

.. code-block:: python

    from dataclasses import dataclass
    from enum import StrEnum

    @dataclass
    class Node:
        id: int
        type: StrEnum
        collection: str
        data: dict

Nodes belong to collections, which are containers to store metadata about a number of nodes associated together. For example, the `US LCA commons <https://www.lcacommons.gov/>`__ is a container for process and product nodes, and refers to the `fedelemflowlist <https://github.com/USEPA/fedelemflowlist>`__, a collection of elementary flows.

Brightway uses different kinds of collections for inventory and impact assessment data. However, they all roughly follow this simplified data model:

.. code-block:: python

    from dataclasses import dataclass
    from datetime import datetime
    from typing import Any

    @dataclass
    class Collection:
        id: Any
        modified: datetime
        data: dict

The datapackages needed for ``bw2calc`` map one-to-one with collections in ``bw2data``. In standard LCA, there are only two types: inventory database datapackages and impact category datapackages. Extensions like regionalization or the inclusion of normalization and weighting can introduce additional datapackage types.

If you haven't passed them in yourself using ``data_objs``, ``bw2calc`` will ask ``bw2data`` which datapackages are needed for a given functional unit. ``bw2data`` will in turn check the creation date for the datapackage and the ``modified`` date for the collection. If the datapackage on disk is obsolete because the collection has been modified since the datapackage was created, it will be deleted and a new datapackage will created from the current database state and written to disk. The requested datapackages (as ``bw_processing.Datapackage`` objects, which can in turn reference any ``fsspec`` file objects) are then passed back to ``bw2calc``.

Datapackage creation
--------------------

Datapackages are created **from the edge data**. Technically, we do retrieve one attribute from the node table - the location of a process - but this is only used in regionalized LCA. The code to write datapackages, in a simplified form (`here is the real code <https://github.com/brightway-lca/brightway2-data/blob/551e975d8c530419ad75581f3935c5db44a27e35/bw2data/backends/base.py#L883>`__), is the following:

.. code-block:: python

    from bw_processing import Datapackage

    def filter_func(edge, matrix, collection) -> bool:
        return (
            e.target.collection == collection and
            edge.type in edge_types_for_this_matrix(matrix)
        )

    class Collection:
        def process(self):
            dp = Datapackage(fs=self.get_collection_datapackage_for_our_filesystem())
            for matrix in self.matrix_list:
                dp.add_persistent_vector_from_iterator(
                    matrix=matrix,
                    dict_iterator=filter_func(edges, matrix, collection)
                )
            dp.finalize_serialization()

For the biosphere matrix, the edge type rules are:

* Only include edges whose ``type`` is in `biosphere_edge_types <https://github.com/brightway-lca/brightway2-data/blob/551e975d8c530419ad75581f3935c5db44a27e35/bw2data/configuration.py#L26>`__.

For the technosphere matrix, the edge type rules are:

* Include `production and substitution <https://github.com/brightway-lca/brightway2-data/blob/551e975d8c530419ad75581f3935c5db44a27e35/bw2data/configuration.py#L31>`__ edges directly
* Include `consumption <https://github.com/brightway-lca/brightway2-data/blob/551e975d8c530419ad75581f3935c5db44a27e35/bw2data/configuration.py#L27>`__ edges but multiply the amount times negative one, to get the right sign in the technosphere matrix
* For every process node which doesn't have a defined production edge, `assume that that process produces one unit of itself <https://github.com/brightway-lca/brightway2-data/blob/main/bw2data/backends/base.py#L920>`__ (i.e. it isn't a process node but instead a ``processwithreferenceproduct`` `chimaera node <https://github.com/brightway-lca/brightway2-data/blob/551e975d8c530419ad75581f3935c5db44a27e35/bw2data/configuration.py#L22>`__).

Note that this last step - the addition of implicit productions edges - will be removed at some point in the near future. "Explicit is better than implicit" say the `Zen masters <https://peps.python.org/pep-0020/>`__.

LCIA datapackages (`Method`, `Normalization`, and `Weighting`) have a different code path and organizational layout, but are close to the biosphere matrix construction.

Collection Metadata and Data Storage
------------------------------------

Brightway isn't quite as clean as the ``Collection`` model given above. Brightway is oriented around **storing data in a directory on the local filesystem**. All subdirectories will be relative to this data directory. Metadata for the following ``Collections`` are stored as JSON files in the data directory:

* Inventory data collections: Called ``databases`` in Brightway, stored in ``databases.json``.
* Impact categories: Called ``methods`` in Brightway, stored in ``methods.json``.
* Normalization factors: Called ``normalizations`` in Brightway, stored in ``normalizations.json``.
* Weighting factors: Called ``weightings`` in Brightway, stored in ``weightings.json``.

These JSON files are loaded when Brightway is imported, and saved when ``.flush()`` is called. They are therefore susceptible to race conditions if two threads are trying to save changes.

These four metadata objects live in the ``bw2data`` namespace and their implementation is given in `bw2data/meta.py <https://github.com/brightway-lca/brightway2-data/blob/main/bw2data/meta.py>`__.

In normal practice you wouldn't work directly with these metadata objects, but would instead use their respective classes:

* ``Database`` for ``databases``
* ``Method`` for ``methods``
* ``Normalization`` for normalizations
* ``Weighting`` for ``weightings``

These objects follow a pattern of use:

* ``object(<some_id>)`` to create instances of object (can be but don't have to be in registered in the metadata objects)
* ``object.register(<key>=<value>)`` to register objects in the metadata storage (and sync metadata to disk)
* ``object.metadata`` to get the metadata associated with the object instance
* ``object.write(<some_data>)`` to write the actual data
* ``for x in object`` or ``object.load()`` to load the data

The metadata JSON files are stored in the data directory.

Storing metadata in JSON files is a poor design decision, and metadata should be stored in a relational database in the near future.

Inventory data, i.e. the data written when ``Database(some_database_name).write(some_data)`` is called, is written in the SQLite inventory database. Data for all other objects are written as ``pickle`` files in the subdirectory ``intermediate``.

Storing data in pickle files is a poor design decision, and data should be stored in a relational database in the near future.

The datapackages associated with ``Database``/``Method``/etc. instances are stored as zipfiles in the ``processed`` subdirectory.

Field Labels
------------

One of the core principles around Brightway is flexibility. However, to allow us to work together effectively as a community, we recommend following the `bw_interface_schemas <https://github.com/brightway-lca/bw_interface_schemas/blob/9abd958279a6033472464caad14f69780837f05c/bw_interface_schemas/models.py>`__ for the field labels and types for collections, nodes, and edges.

SQLite Graph Database
---------------------

The inventory graph - products, processes, and elementary flows as nodes, plus directed edges between these nodes - is stored in a SQLite database called ``databases.db`` in the subdirectory ``lci``. The actual database schema is:

.. code-block:: sql

    CREATE TABLE "activitydataset" (
        "id" INTEGER NOT NULL PRIMARY KEY,
        "data" BLOB NOT NULL,
        "code" TEXT NOT NULL,
        "database" TEXT NOT NULL,
        "location" TEXT,
        "name" TEXT,
        "product" TEXT,
        "type" TEXT
    )
    CREATE TABLE "exchangedataset" (
        "id" INTEGER NOT NULL PRIMARY KEY,
        "data" BLOB NOT NULL,
        "input_code" TEXT NOT NULL,
        "input_database" TEXT NOT NULL,
        "output_code" TEXT NOT NULL,
        "output_database" TEXT NOT NULL,
        "type" TEXT NOT NULL
    )
    CREATE UNIQUE INDEX "activitydataset_key" ON "activitydataset" ("database", "code")
    CREATE INDEX "exchangedataset_input" ON "exchangedataset" ("input_database", "input_code")
    CREATE INDEX "exchangedataset_output" ON "exchangedataset" ("output_database", "output_code")

The database ids for datapackages come from the ``activitydataset.id`` column.

This is a database schema which allows for a lot of flexibility, but will probably change in the future. Note the following important considerations:

* There are no foreign keys. This means that deletes don't cascade, but also that there is no guarantee a row referenced in ``exchangedataset`` actually exists in ``activitydataset``. It would be better if the edge table followed the simpler data schema presented above and used proper foreign keys.
* We have two unique ways of identifying a node - either its ``id``, or its ``("database", "code")`` combination.
* There is duplication of data in the nodes table, as the values for database, location, name, product, and type are all also given in ``data``. These duplicating columns are only there to allow writing SQL queries against these attributes.
* The ``data`` is not stored as JSON but instead as ``BLOB`` as pickles. For security and general sanity reasons this should change in the near future.

Brightway uses the ORM library `peewee <https://docs.peewee-orm.com/en/latest/>`__. It might be simpler than more heavyweight libraries like sqlalchemy, but it is simpler than more heavyweight libraries like sqlalchemy 😉

Brightway extends on the peewee ORM classes to add additional functionality. So, for example, in the node class (called ``Activity``, but also importable as ``Node``) the peewee ORM is a `hidden attribute <https://github.com/brightway-lca/brightway2-data/blob/551e975d8c530419ad75581f3935c5db44a27e35/bw2data/backends/proxies.py#L205>`__ which is used to `set node data <https://github.com/brightway-lca/brightway2-data/blob/551e975d8c530419ad75581f3935c5db44a27e35/bw2data/backends/proxies.py#L208>`__ and `save data to SQLite <https://github.com/brightway-lca/brightway2-data/blob/551e975d8c530419ad75581f3935c5db44a27e35/bw2data/backends/proxies.py#L307>`__.

The storage of metadata in JSON files, and the lack of foreign keys, means that the node class has to do extra work when `moving nodes to another database <https://github.com/brightway-lca/brightway2-data/blob/551e975d8c530419ad75581f3935c5db44a27e35/bw2data/backends/proxies.py#L406>`__ or `changing the node code <https://github.com/brightway-lca/brightway2-data/blob/551e975d8c530419ad75581f3935c5db44a27e35/bw2data/backends/proxies.py#L364>`__.

The ``code`` field was originally used as the main unique identifier *within a database* - however, because the datapackages required integer identifiers, we had to keep a separate mapping of ``("database", "code")`` to unique integer ids. The database was already doing this with the ``id`` column, so Brightway now recommends to use the ``id`` value, and the code is only used when linking data during IO.

The node classes also include utility functions to iterate over edges which refer to the given node, like ``node.production()`` or ``node.biosphere()``.

Edge classes (``Exchange``, but also importable as ``Edge``) follow the `same pattern as nodes <https://github.com/brightway-lca/brightway2-data/blob/551e975d8c530419ad75581f3935c5db44a27e35/bw2data/backends/proxies.py#L564>`__. Because of their unique database schema, we normally get to edges by using the node utility methods.

Projects
========

Because Brightway assumes all data can be stored in a directory, we can easily get independent projects by switching the data directory. This is what a Brightway project is - a standalone directory with all the data for that project.

Brightway uses the `platformdirs <https://platformdirs.readthedocs.io/en/latest/>`__ library to find a good place to store data on your machine. You can see the root directory that all project directories are stored in with this code (it varies by operating system and username):

.. code-block:: python

    from platformdirs import PlatformDirs
    PlatformDirs("Brightway3", "pylca").user_data_dir

In this root directory, in addition to the subdirectories for each project, there will be a SQLite file called ``projects.db``. It has the following schema:

.. code-block:: sql

    CREATE TABLE "projectdataset" (
        "id" INTEGER NOT NULL PRIMARY KEY,
        "is_sourced" INTEGER NOT NULL DEFAULT 0,
        "revision" INTEGER,
        "data" BLOB NOT NULL,
        "name" TEXT NOT NULL,
        "full_hash" INTEGER NOT NULL DEFAULT 1
    )
    CREATE UNIQUE INDEX "projectdataset_name" ON "projectdataset" ("name")

You should consider all project attributes other than the name to be internal hidden variables.

Changing Projects
-----------------

To change the active project in Brightway, you can just do ``bw2data.projects.set_current(<new_project_name>)``. However, the actual process of changing the project in the backend is a `bit more complex <https://github.com/brightway-lca/brightway2-data/blob/main/bw2data/project.py#L421>`__. We need to:

* Reload all the metadata JSON files
* Open the new SQLite inventory database, and rebind the ORM table objects to these new tables
* Possibly apply updates to project data, if needed

Reloading the metadata is simple, because ``databases``/etc. are basically fancy dictionaries. We can just load the new data into their internal state by calling their ``__init__()`` method again.

To rebind ORM tables we use a `convenient function in peewee <https://github.com/brightway-lca/brightway2-data/blob/main/bw2data/sqlite.py#L26>`__. This requires us to keep a list of SQLite tables which need `dynamic configuration <https://docs.peewee-orm.com/en/latest/peewee/database.html#run-time-database-configuration>`__.

That's it! Take a breath, have a cup of tea, and smile in the summer sun 😎
