Brightway2: Improving experience on Windows
###########################################

:date: 2013-05-25 12:00
:category: brightway2
:slug: better-on-windows-upload-logs
:summary: We're trying to improve the experience on Windows, including a new feature to easily share error logs

The primary development environment for Brightway2 is Mac OS X 10.6, but it is also tested on Ubuntu 12.04 LTS on a separate machine and Windows 7 in a virtual machine. Although I have been able to install and use Brightway2 without problems on my Windows installation, others have had difficulties due to string encoding bugs and Windows behavior that wasn't handled correctly.

.. figure:: images/friendship.jpg
    :alt: Aren't all pictures on the internet supposed to include cats?
    :align: center

    Figure 1: Getting further by working together. Credit: `EJP Photo <http://www.flickr.com/photos/ejpphoto/3654080354/>`_.

New feature: log uploads
========================

A number of these bugs have been now been fixed. Changesets `5793b0a <https://bitbucket.org/cmutel/brightway2-data/commits/5793b0a146a379f9aae2d4b5f7c5a43c61d663f5>`_ and `ec29212 <https://bitbucket.org/cmutel/brightway2-ui/commits/ec2921289bf9c933283276273b6e8c773ff78045>`_ introduce the ability to upload logs to the main Brightway2 server, so that error can be centrally collected and analyzed. In addition to bugs, I also want to figure out why some things which are fast for me are slow on other machines, like working with JSON data. A number of input/output functions now have their performance logged.

If you have an error, and want me to look at it, you can now use the following code to upload your logs:

.. code-block:: bash

    bw2-controller.py upload_logs

You can also add a comment in quotations:

.. code-block:: bash

    bw2-controller.py upload_logs "I've fallen, and I can't get up"

What about privacy?
===================

Uploading logs is voluntary, and must be done manually. Nevertheless, it is natural to ask about what information is provided. The logs themselves have the following information:

* How long it took to load and process inventory databases and impact assessment methods
* Any new inventory flows that were created during inventory or impact assessment imports

In addition, the upload service collects the following information:

* Your operating system and Python version
* Your JSON library
* Your IP address

Note that **no** names, filesystem paths, or other identifying information is included. As always, Brightway2 code is open source, and the relevant functions can be found in:

* `brightway2-data <https://bitbucket.org/cmutel/brightway2-data>`_
* `brightway2-ui <https://bitbucket.org/cmutel/brightway2-ui>`_
* `brightway2-web-reports <https://bitbucket.org/cmutel/brightway2-web-reports>`_

How to upgrade
==============

You can upgrade to the latest version of all Brightway2 packages by opening a terminal window (command shell in Windows), and type the following:

.. code-block:: bash

    pip install --upgrade --no-deps brightway2 bw2calc bw2analyzer bw2ui bw2data
