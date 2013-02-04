New feature: Brightway2 test coverage
#####################################

:date: 2013-01-28 12:00
:category: brightway2
:slug: test-coverage
:summary: There is now an online report of Brightway2 package test coverage.

What is test coverage?
======================

Although Brightway2 doesn't follow a strict `test-driven development <http://en.wikipedia.org/wiki/Test-driven_development>`_ philosophy, tests are an important part of making an application that works on multiple operating systems and produces correct results. Brightway2 uses `nose <https://github.com/nose-devs/nose>`_, a library for discovering and running tests, and `coverage <http://pypi.python.org/pypi/coverage>`_, which shows how well tests provide `code coverage <http://en.wikipedia.org/wiki/Code_coverage>`_.

Brightway2 test coverage now online
===================================

You can see for yourself how well the current test suite covers the Brightway2 code base at http://coverage.brightwaylca.org. Bear in mind that coverage doesn't guarantee that the code is correct, or devoid of bugs, or that a lack of test coverage means that the code is problematic. For example, `Brightway2-calc <https://bitbucket.org/cmutel/brightway2-calc>`_ has poor test coverage, but the core calculation code was ported from the original Brightway code base and has been tested and used for years.