|build| |coverage| |pypi| |python| |license|

SIpy
====

SIpy is a fast, lightweight and easily extensible python package for manipulating
physical quantities.

For more detailed information read the `documentation <https://broster.gitlab.io/sipy/>`_.

Quickstart
==========
SIpy can be installed via `pipenv
<https://docs.pipenv.org/install/#installing-packages-for-your-project>`_ or
`pip <https://docs.python.org/3/installing/index.html>`_, and requires Python 3.6.0 or higher.

.. code-block:: console

    $ pipenv install sipy
    $ pip install sipy

Once SIpy is installed just import the quantities you need and you're good to go

.. code-block:: python

    >>> from sipy import miles, hour
    >>> speed_limit = 70 * miles / hour
    >>> print(speed_limit)
    3.13E+01ms^-1


Contributing
============

SIpy is developed on `GitLab
<https://gitlab.com/broster/sipy>`_. If you come across an issue,
or have a feature request please open an `issue
<https://gitlab.com/broster/sipy/issues>`_.  If you want to
contribute a fix or feature-implementation please do by proposing a `merge request
<https://gitlab.com/broster/sipy/merge_requests>`_.

Testing
~~~~~~~

SIpy uses `Pytest <https://docs.pytest.org/en/latest/>`_ for unit testing and
and `pre-commit <https://pre-commit.com/>`_ for static analysis and auto-formatting.
Code is automatically checked by Gitlab pipelines when pushed but it is
recommended that tests are also run locally.

SIpy used `Poetry <https://python-poetry.org/>`_ for managing all external dependencies.
Install `Poetry` using the instructions `here <https://python-poetry.org/docs/>`_ and then
install dependencies with

.. code-block:: console

    $ poetry install

`pre-commit` should run automatically on every commit. To enable it run

.. code-block:: console

    $ poetry run pre-commit install

The unittests can be run with:

.. code-block:: console

    $ poetry run pytest --doctest-modules tests sipy README.rst

Help
====

The SIpy `documentation <https://broster.gitlab.io/sipy/>`_
is the best place to start, after that try searching stack overflow,
if you still can't find an answer please `open an issue
<https://broster.gitlab.io/sipy/issues>`_.


.. |build| image:: https://gitlab.com/broster/sipy/badges/master/pipeline.svg
   :target: https://gitlab.com/broster/sipy/commits/master

.. |coverage| image:: https://gitlab.com/broster/sipy/badges/master/coverage.svg
   :target: https://gitlab.com/broster/sipy/commits/master

.. |pypi| image:: https://img.shields.io/pypi/v/sipy.svg
   :target: https://pypi.python.org/pypi/Hypercorn/

.. |python| image:: https://img.shields.io/pypi/pyversions/sipy.svg
   :target: https://pypi.python.org/pypi/Hypercorn/

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://gitlab.com/pgjones/hypercorn/blob/master/LICENSE
