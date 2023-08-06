=====
Usage
=====

.. code-block:: shell

   $ pip install request_limiter


Using as a decorator on django view:

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


Using as a decorator on any function:

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


Using the strategy to limit part of logic:

.. code-block:: python

    from request_limiter import LimitedIntervalStrategy

    limiter = LimitedIntervalStrategy(requests=1, interval=60))  # 1 request per minute

    def awesome_work(param):
        if not limiter.allow():
            return False
        # ...
        return True

    awesome_work("job1")  # returns True
    awesome_work("job2")  # returns False
