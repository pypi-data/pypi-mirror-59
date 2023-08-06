pytest-ligo
~~~~~~~~~~~

Py.test plugin which adds a tezos fixture to encapsulate boilerplate business
logic.

- ``test_pytest_tezos.py``: example usage,
- ``.gitlab-ci.yml``: to adapt to your own use.

Install with pip, ie::

    pip install -e git+http://gitlab.com/jpic/pytest-ligo.git#egg=pytest-tezos
    pip install -e git+http://gitlab.com/jpic/pytest-ligo.git#egg=pytest-ligo

Run an auto baking sandbox::

    docker run -p 8732:8732 yourlabs/tezos
