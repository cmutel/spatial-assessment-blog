Modular BONSAI components
#########################

:date: 2019-03-11-09:00
:category: bonsai
:slug: bonsai-components
:summary: A preliminary layout for modular BONSAI components

.. figure:: images/bonsai-components.png
    :align: center
    :width: 930px

While planning for the BONSAI hackathon, and what should come after it, I have become more confidant that we can both produce something which is a substantial advancement over the status quo, and that it can proceed piecewise, with each new component adding to the overall system. As such, I put together the following modular system components which I would prioritize for the next year of BONSAI development. Most of these components will build on other BONSAI components libraries or standards.

Data inputs
===========

**Web input helper**: Simple web app to help format input data in RDF ontology.

**Predictor**: Given an industry or product classifier, list the most important predicted inputs (based on a suite of environmental indicators) and approximate input amount ranges based on existing datasets. Can also highlight inputs which only show up in IO tables and not in process-based inventories.

**Labeller**: Guess labels from BONSAI product and industry names based on a machine learning classifier. Keeps original data, just adds new columns. Takes CSV or RDF as input. Training data will come from the descriptions and documentation of the ontologies.

**CSV RDF converter**: Converts data from labelled CSV to an RDF file following the BONSAI ontology set that can be read directly into e.g. Apache Jena

**PDF Table extractor**: BONSAI-hosted instance of `Excalibur <https://www.tryexcalibur.com/>`__.

Validation
==========

**Validator**: Validates RDF files for the BONSAI ontology set. We need a relatively strict validation, as we want to limit the types of input data available so that our algorithms can know what to expect when processing data.

**Quality assurance**: Checks reasonableness of input data, as much as possible. Mass and economic balances, uncertainty data, etc.

RDF triplestore
===============

The master database that stores data following the BONSAI ontology. Unclear at this stage if we will include much logic in the database itself; it might be easiest for the current group to extract data, process in e.g. Python, and then write the processed data back to the triplestore.

An instance of Apache `Jena <https://jena.apache.org/>`__ for BONSAI is already running at the University of Aalborg.

Standards
=========

**Execution standards**: How to package an LCI/LCIA model as an executable in a container.

**Coding standards**: Standards for LCI/LCIA models, such as testing, documentation, library templates, IO formats, and model transparency.

**Generic Model API**: Generic interface for LCI models which follow the coding standards that allows them to be hosted web services

**Pipeline**: A simple markup language (built on top of existing data pipeline tech and standards) that allows for input pre-processing using other BONSAI components, LCI model execution, system model execution, output processing, and finally creation of a BONSAI result. Eventually this will be the way that anyone can build their own BONSAI model/database/IO table.

**BONSAI-specific ontology**: Formal specifications for the new vocabulary needed to express BONSAI concepts.

**BONSAI complete ontology**: An ontology definition which includes all ontologies used to describe BONSAI data points.

System models & IO
==================

**Database reducer**: Functional-unit specific tool to simplify IO tables outputs to eliminate complexity while retaining result integrity.

**Validation dashboard**: A constantly-updated dashboard showing how the BONSAI base system models compare to independent validation metrics.

**Format converter**: Convert RDF outputs to JSON-LD, SimaPro CSV, etc.

**Base system models**: One or more consensus system models, initially built on top of `PySUT <https://github.com/stefanpauliuk/pySUT>`__, which reconcile data points, create supply and use tables, and then create input-output tables.

**BONSAI API**: BONSAI raw data, result tables, and calculations as web services.

**Log tracer**: Traces the calculation history of each result data point back to its origin.

Hackathon 2019 outputs
======================

The following are currently listed as hackathon outputs (as first versions):

* Jena database instance
* Execution standards
* Coding standards
* BONSAI-specific ontology
* BONSAI complete ontology
* Format converter
* CSV RDF converter

Limitations
===========

This is a first draft of what BONSAI could look like, and is dependent on what the community wants to build. I have developed a draft formal process for `community decision-making <https://github.com/BONSAMURAIS/enhancements/blob/master/beps/0002-bonsai-project-community-governance-structure.md>`__, and this may or may not be adopted. In any case, BONSAI is built by people volunteering their time and ideas.

Edit history
============

* 2019-03-12: Changed description of RDF database. Thanks to Matteo Lissandrini for the comment!
