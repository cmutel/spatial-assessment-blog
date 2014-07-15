Multioutput processes in LCA
############################

:date: 2014-06-19 00:00
:category: math
:slug: multioutput
:summary: Multioutput processes can be used in LCA in limited circumstances.
:status: draft

.. figure:: images/cactus.jpg
    :alt: Cactus photo by Oliver Pacas (http://www.splashbase.co/sources/166)
    :align: center

    A prickly subject in LCA

Technosphere matrix with processes and products
===============================================

Before reading this post, please make sure you have read `What happens with a non-unitary production amount in LCA? <http://chris.mutel.org/non-unitary.html>`_. You should already know that in the technosphere matrix, columns are processes (activities), and rows are products. The demand array (functional unit) is expressed in units of products, and the supply array is in processes:

.. figure:: images/mo-system1.png
    :align: center

The problem with multiple outputs
=================================

There isn't a problem, per se, with processes that produce multiple outputs. The difficulty that we in the LCA community have comes from the way we impose our model, with its rules and assumptions, on the real world. We want to classify and split the world into a series of technological processes, each with a set of distinct inputs and outputs, and then be able to solve our mathematical model with an arbitrary demand. The disconnect between discrete models and semi-continuous conditions in the real world is a classic theme in model building, and is also a challenge in designing LCIA models.

The basic problem is that we have some processes, such as a combined heat and power (CHP) plant, that by their very nature produce multiple outputs, but our model allows us to specify a demand vector which includes only one output (say electricity) while requiring zero units of the other output (heat) to be produced. This is impossible, both in a real and mathematical sense.

The math of multiple outputs
----------------------------

In this system, the amount the CHP plant is run is the variable we are trying to solve for. If we demand electricity but not heat, then we have two equations with one variable:

.. math::
    \begin{array}{ccc}
    electricity \cdot CHP & = & 1 \\
    heat \cdot CHP & = & 0 \\
    \end{array}

In this example, the split between heat and electricity doesn't matter, so let's set them both to one:

.. math::
    \begin{array}{ccc}
    1 \cdot CHP & = & 1 \\
    1 \cdot CHP & = & 0 \\
    \end{array}

We could also write this in matrix form (matrices are basically just shorthand for systems of linear equations):

.. math::
    \left[ \begin{array}{c}
     1 \\
     1 \\
    \end{array} \right] CHP = \left[ \begin{array}{c}
      1 \\
      0 \\
    \end{array} \right]

Obviously, the variable *CHP* can't be both zero and one, and so this system has no solution. In fact, any system such as this one where are more equations than variables is called `overdetermined <https://en.wikipedia.org/wiki/Overdetermined_system>`_ (see also Wikipedia `system of linear equations <https://en.wikipedia.org/wiki/System_of_linear_equations>`_). Overdetermined systems can have specific solutions, depending on the demand vector; approximate solutions can also be found, e.g. `Marvuglia et al 2010 <http://link.springer.com/article/10.1007/s11367-010-0214-1>`_.

So, we can think of multioutput processes in different ways, depending on our background. Mathematically, multioutput processes cause an overdetermined technosphere matrix which has no solution. Physically, multioutput processes create a product which we specified in the demand array as having no net production. From another point of view, multioutput processes expose a disconnect between our model assumptions and the real world.

Solutions to multiple outputs
=============================

Allocation
----------

Allocation means splitting multioutput processes into single output unit processes (aka SOUPs) using physical, economic, or other criteria. Allocation has been and is the subject of much debate in the LCA literature, but isn't discussed further here.

Include all outputs in demand
-----------------------------

The easiest solution is to hit yourself on the head, and say that of course you simply can't get electricity without electricity from a CHP plant, or leather without beef, or kids without having your laptop peed on somehow (at least in my experience). Instead, you include all the products in the correct respective quantities in the demand vector itself, i.e. for example system:

.. math::
    \begin{array}{ccc}
    1 \cdot CHP & = & 1 \\
    1 \cdot CHP & = & 1 \\
    \end{array}

.. math::
    CHP = 1

Mathematically, this approach makes a matrix which does not have full rank (i.e. not all rows are linearly independent - the first row is a copy of the second row), and as such the system is longer overdetermined. There is actually only one equation and one variable.

Including all outputs is certainly the most representative of the real world, but is difficult to do when the multioutput processes are in the background, or when there are many multioutput processes. You have to get the stoichiometry of the demand array correct to get a solution, but if your multioutput process is a few levels deep in your supply chain, you would need to calculate how much of that process is needed, and then adjust your demand array for the necessary additional products.

Note that altering the demand vector does not require substitution, a subject which is discussed in the next section.

Substitution
------------

If we really want to insist that we have one unit of electricity and none of heat, then we can solve our system by getting zero net heat production. The first way to achieve this is substitution - we cancel out heat production by inducing a *negative* supply of another process that produces heat. In our example, the CHP heat could substitute for heat from natural gas combustion, which we can write as:

.. math::
    \begin{array}{ccccc}
    electricity \cdot CHP & + & 0 \cdot gas & = & 1 \\
    heat \cdot CHP & + & heat \cdot gas & = & 0 \\
    \end{array}

With the following solution:

.. math::
    \begin{array}{ccc}
    CHP & = & 1 \\
    gas & = & -1 \\
    \end{array}

We have solved our problem with the overdetermined system by adding another variable, so we have two equations and two variables. Our technosphere matrix is now square and of full rank. This is quite a flexible approach - the substituted process could also by multioutput, and have its other output substituted by a third process!

There are a few things to bear in mind about substitution. First, the substituted process must *produce* the substituted product, i.e. it is a positive number in the technosphere matrix, not an input (which would be negative). If the product is an input, then this is waste treatment, not substitution, and is covered in the next section.

Second, substitution is not defined as part of the original dataset, but rather, substitution happens automatically as long as both processes produce precisely the same product (same row in the technosphere matrix). It can be difficult to determine what is substituted, and by which processes, by looking at raw process datasets.

Third, there can only be one substituting process. If there were two, then we wouldn't know the correct balance between the two substituting processes. In our example, if there was also an old-fired boiler producing heat, then there isn't precisely one solution for the supply vector - instead, there are now an infinite number of solutions!

.. math::
    \begin{array}{ccccccc}
    electricity \cdot CHP & + & 0 \cdot gas & + & 0 \cdot oil & = & 1 \\
    heat \cdot CHP & + & heat \cdot gas & + & heat \cdot oil & = & 0 \\
    \end{array}

Now :math:`gas = -0.5` and :math:`oil = -0.5` is a solution, but so is :math:`gas = -1` and :math:`oil = 0`. This is called an `underdetermined system <http://en.wikipedia.org/wiki/Underdetermined_system>`_, because we have more variables than equations. Underdetermined systems are good for optimization, but not great for LCA, as we need a single supply array to calculate the life cycle inventory.

Waste treatment
---------------

It is important to distinguish between outputs which . This distinction is not universal - what is a waste to one person is a resource to another. Ecoinvent version 3 makes the claim that there are no wastes in their system, just materials which require treatment before they can be used by other processes.

Multioutput processes in Brightway2
===================================

The `Brightway2 LCA framework <http://brightwaylca.org/>`_ allows for multioutput processes without allocation. Substitution and waste treatment are supported by default. System expansion is supported by the ``LeastSquaresLCA`` class (``bw2calc.least_squares.LeastSquaresLCA``), which can also give approximate answers in cases where none of the solution approaches have been used.
