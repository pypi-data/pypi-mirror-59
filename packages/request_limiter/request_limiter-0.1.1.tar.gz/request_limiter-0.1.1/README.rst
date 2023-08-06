===============
Request Limiter
===============


.. image:: https://img.shields.io/pypi/v/request_limiter.svg
        :target: https://pypi.python.org/pypi/request_limiter

.. image:: https://img.shields.io/travis/matibek/request_limiter.svg
        :target: https://travis-ci.org/matibek/request_limiter

.. image:: https://readthedocs.org/projects/request-limiter/badge/?version=latest
        :target: https://request-limiter.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Request limiter contains a decorator to limit the rate of http request


* Free software: MIT license
* Documentation: https://request-limiter.readthedocs.io.


Features
--------

* A decorator to limit django http request
* A strategy to limit request per interval using requester IP

Get started
-----------

Installation:

.. code-block:: shell

   $ pip install request_limiter

Limit request to django view using a decorator:

.. code-block:: python

    from request_limiter import request_limiter, LimitedIntervalStrategy, django_request_limiter

    @django_request_limiter
    @request_limiter(strategy=LimitedIntervalStrategy(requests=10, interval=60))  # 10 request per minute
    def myview(request):
        # ...

Limit the number of request to function or part of it:

.. code-block:: python

    from request_limiter import request_limiter, LimitedIntervalStrategy, LimitException

    @request_limiter(strategy=LimitedIntervalStrategy(requests=1, interval=60))  # 1 request per minute
    def awesome_work(param):
        # ...

    awesome_work("test")
    try:
        awesome_work("limited")  # raises LimitException
    except LimitException:
        # .. handle limit exception

    limiter = LimitedIntervalStrategy(requests=1, interval=60))  # 1 request per minute

    def another_work(param):
        if not limiter.allow():
            return False
        # ...
        return True

    another_work("job1")  # returns True
    another_work("job2")  # returns False

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
