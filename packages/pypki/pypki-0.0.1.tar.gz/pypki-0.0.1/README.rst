========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/pypki/badge/?style=flat
    :target: https://readthedocs.org/projects/pypki
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/hlevering/pypki.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/hlevering/pypki

.. |requires| image:: https://requires.io/github/hlevering/pypki/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/hlevering/pypki/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/hlevering/pypki/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/hlevering/pypki

.. |version| image:: https://img.shields.io/pypi/v/pypki.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/pypki

.. |wheel| image:: https://img.shields.io/pypi/wheel/pypki.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/pypki

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pypki.svg
    :alt: Supported versions
    :target: https://pypi.org/project/pypki

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pypki.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/pypki

.. |commits-since| image:: https://img.shields.io/github/commits-since/hlevering/pypki/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/hlevering/pypki/compare/v0.0.1...master



.. end-badges

Managing PKI systems

* Free software: BSD 2-Clause License

Installation
============

::

    pip install pypki

You can also install the in-development version with::

    pip install https://github.com/hlevering/pypki/archive/master.zip


Documentation
=============


https://pypki.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
