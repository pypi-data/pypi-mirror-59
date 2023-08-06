=====
Usage
=====

.. code-block:: shell

   $ pip install request_limiter


To use Request Limiter in a project:

.. code-block:: python

    from request_limiter import request_limiter, LimitedIntervalStrategy, django_request_limiter

    @django_request_limiter
    @request_limiter(strategy=LimitedIntervalStrategy(requests=10, interval=60))  # 10 request per minute
    def myview(request):
        # ...

    @django_request_limiter
    @request_limiter(strategy=LimitedIntervalStrategy(requests=100, interval=24*60*60))  # 100 request per day
    def anotherview(request):
        # ...
