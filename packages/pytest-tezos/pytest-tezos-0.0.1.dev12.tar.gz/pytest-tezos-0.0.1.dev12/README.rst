pytest-ligo
~~~~~~~~~~~

Py.test plugin which adds a tezos fixture to encapsulate boilerplate business
logic. Refer to ``test_pytest_tezos.py`` for example usage.

Install with pip, ie::

    pip install pytest-tezos

Run an auto baking sandbox on localhost::

    docker run -p 8732:8732 yourlabs/tezos

For CI configuration, refer to ``.gitlab-ci.yml``.
