.. role:: raw-html-m2r(raw)
   :format: html


Sage: a SPARQL query engine for public Linked Data providers
============================================================


.. image:: https://travis-ci.com/sage-org/sage-engine.svg?branch=master
   :target: https://travis-ci.com/sage-org/sage-engine
   :alt: Build Status

.. image:: https://badge.fury.io/py/sage-engine.svg
   :target: https://badge.fury.io/py/sage-engine
   :alt: PyPI version


Python implementation of SaGe, a stable, responsive and unrestricted SPARQL query server.

Table of contents
=================


* `Installation <#installation>`_
* `Getting started <#getting-started>`_

  * `Server configuration <#server-configuration>`_
  * `Starting the server <#starting-the-server>`_

* `SaGe Docker image <#sage-docker-image>`_
* `Documentation <#documentation>`_

Installation
============

Installation using pip (with the HDT backend)
---------------------------------------------

Installation in a `virtualenv <https://virtualenv.pypa.io/en/stable/>`_ is **strongly advised!**

Requirements:


* `pip <https://pip.pypa.io/en/stable/>`_
* **gcc/clang** with **c++11 support**
* **Python Development headers**
  ..

     You should have the ``Python.h`` header available on your system.
     For example, for Python 3.6, install the ``python3.6-dev`` package on Debian/Ubuntu systems.


The core engine of the SaGe SPARQL query server with `HDT <http://www.rdfhdt.org/>`_ as a backend can be installed as follows:

.. code-block:: bash

   pip install sage-engine[hdt]

Manual installation (with the HDT backend)
------------------------------------------

Additional requirements:


* `git <https://git-scm.com/>`_
* `npm <https://nodejs.org/en/>`_ (shipped with Node.js on most systems)

.. code-block:: bash

   git clone https://github.com/sage-org/sage-engine
   cd sage-engine/
   pip install -r requirements.txt
   pip install -e .[hdt]

Getting started
===============

Server configuration
--------------------

A Sage server is configured using a configuration file in `YAML syntax <http://yaml.org/>`_.
You will find below a minimal working example of such configuration file.
A full example is available `in the ``config_examples/`` directory <https://github.com/sage-org/sage-engine/blob/master/config_examples/example.yaml>`_

.. code-block:: yaml

   name: SaGe Test server
   maintainer: Chuck Norris
   quota: 75
   max_results: 2000
   datasets:
   -
     name: dbpedia
     description: DBPedia
     backend: hdt-file
     file: datasets/dbpedia.2016.hdt

The ``quota`` and ``max_results`` fields are used to set the maximum time quantum and the maximum number of results
allowed per request, respectively.

Each entry in the ``datasets`` field declare a RDF dataset with a name, description, backend and options specific to this backend.
Currently, **only** the ``hdt-file`` backend is supported, which allow a Sage server to load RDF datasets from `HDT files <http://www.rdfhdt.org/>`_. Sage uses `pyHDT <https://github.com/Callidon/pyHDT>`_ to load and query HDT files.

Starting the server
-------------------

The ``sage`` executable, installed alongside the Sage server, allows to easily start a Sage server from a configuration file using `Gunicorn <http://gunicorn.org/>`_\ , a Python WSGI HTTP Server.

.. code-block:: bash

   # launch Sage server with 4 workers on port 8000
   sage my_config.yaml -w 4 -p 8000

The full usage of the ``sage`` executable is detailed below:

.. code-block:: bash

   usage: sage [-h] [-p P] [-w W] [--log-level LEVEL] config

   Launch the Sage server using a configuration file

   positional arguments:
     config             Path to the configuration file

   optional arguments:
     -h, --help         show this help message and exit
     -p P, --port P     The port to bind (default: 8000)
     -w W, --workers W  The number of server workers (default: 4)
     --log-level LEVEL  The granularity of log outputs (default: info)

SaGe Docker image
=================

The Sage server is also available through a `Docker image <https://hub.docker.com/r/callidon/sage/>`_.
In order to use it, do not forget to `mount in the container <https://docs.docker.com/storage/volumes/>`_ the directory that contains you configuration file and your datasets.

.. code-block:: bash

   docker pull callidon/sage
   docker run -v path/to/config-file:/opt/data/ -p 8000:8000 callidon/sage sage /opt/data/config.yaml -w 4 -p 8000

Documentation
=============

To generate the documentation, you must install the following dependencies

.. code-block:: bash

   pip install sphinx sphinx_rtd_theme sphinxcontrib-httpdomain

Then, navigate in the ``docs`` directory and generate the documentation

.. code-block:: bash

   cd docs/
   make html
   open build/html/index.html

Copyright 2017-2019 - `GDD Team <https://sites.google.com/site/gddlina/>`_\ , `LS2N <https://www.ls2n.fr/?lang=en>`_\ , `University of Nantes <http://www.univ-nantes.fr/>`_
