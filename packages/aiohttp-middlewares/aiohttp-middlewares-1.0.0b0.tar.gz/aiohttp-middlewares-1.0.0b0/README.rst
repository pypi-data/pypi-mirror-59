===================
aiohttp-middlewares
===================

.. image:: https://img.shields.io/circleci/project/github/playpauseandstop/aiohttp-middlewares/master.svg
    :target: https://circleci.com/gh/playpauseandstop/aiohttp-middlewares
    :alt: CircleCI

.. image:: https://img.shields.io/pypi/v/aiohttp-middlewares.svg
    :target: https://pypi.org/project/aiohttp-middlewares/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/aiohttp-middlewares.svg
    :target: https://pypi.org/project/aiohttp-middlewares/
    :alt: Python versions

.. image:: https://img.shields.io/pypi/l/aiohttp-middlewares.svg
    :target: https://github.com/playpauseandstop/aiohttp-middlewares/blob/master/LICENSE
    :alt: BSD License

.. image:: https://coveralls.io/repos/playpauseandstop/aiohttp-middlewares/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/playpauseandstop/aiohttp-middlewares
    :alt: Coverage

.. image:: https://readthedocs.org/projects/aiohttp-middlewares/badge/?version=latest
    :target: http://aiohttp-middlewares.readthedocs.org/en/latest/
    :alt: Documentation

Collection of useful middlewares for `aiohttp <http://aiohttp.readthedocs.org/>`_
applications.

- Works on Python 3.6+
- Works with aiohttp 3.5+
- BSD licensed
- Latest documentation `on Read The Docs
  <https://aiohttp-middlewares.readthedocs.io/>`_
- Source, issues, and pull requests `on GitHub
  <https://github.com/playpauseandstop/aiohttp-middlewares>`_

Quickstart
==========

By default ``aiohttp.web`` does not provide many built-in middlewares for
standart web development actions such as handling errors, shielding view
handlers, or providing CORS headers.

``aiohttp-middlewares`` fix this by providing several middlewares that aims to
cover most common web-development needs.

For example, to enable CORS headers for ``http://localhost:8081`` and handle
errors for ``aiohttp.web`` application you need to,

.. code-block:: python

    from aiohttp import web
    from aiohttp_middlewares import cors_middleware, error_middleware


    app = web.Application(
        middlewares=(
            cors_middleware(origins=("http://localhost:8081",)),
            error_middleware(),
        )
    )

Check `documentation <https://aiohttp-middlewares.readthedocs.io/>`_ for
all available middlewares and available initialization options.
