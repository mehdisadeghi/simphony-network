simphony-network
================

Client-server functionality for the SimPhoNy framework.

This packages provides a proxy engine which can be used to
launch a wrapper on a remote host. This proxy wrapper
follows the interface of ABCModelingEngine abstract class.


.. image:: https://travis-ci.org/simphony/simphony-network.svg?branch=master
    :target: https://travis-ci.org/simphony/simphony-network

.. image:: https://coveralls.io/repos/simphony/simphony-network/badge.svg
   :target: https://coveralls.io/r/simphony/simphony-network

Repository
----------

Simphony-network is hosted on github: https://github.com/simphony/simphony-network

Requirements
------------
- `simphony-common`_ >= 0.1.1

.. _simphony-common: https://github.com/simphony/simphony-common

- `gevent`_ >= 1.0

.. _gevent: http://cython.org/

- `pyzmq`_ >= 13.1.0

.. _pyzmq: https://zeromq.github.io/pyzmq/

- `msgpack-python`_ >= 0.4.6

.. _msgpack-python: https://pypi.python.org/pypi/msgpack-python/

- `msgpack-numpy`_ >= 0.3.6

.. _msgpack-numpy: https://pypi.python.org/pypi/msgpack-numpy

- `zerorpc`_ >= 0.5.1

.. _zerorpc: http://www.zerorpc.io/

- `Fabric`_ >= 1.10.2

.. _Fabric: http://www.fabfile.org/


.. note::
  `pyzmq` package will try to find a local `libzmq` library or otherwise will
  try to compile it as an extension. In this case proper build tools should be
  available on local machine, including a C compiler.

Installation
------------

.. note::
  `msgpack-python` should have been compiled with C extensions, otherwise
  the client-server communication will not work. After installation one should
  be able to import the following module::

      from msgpack import _packer, _unpacker

  if the following import fails, the `msgpack-python` should be reinstalled after
  installing `cython`: https://pypi.python.org/pypi/Cython/.

The package requires python 2.7.x, and aforementioned dependencies.
These dependencies are listed inside `requirements.txt` file which should
be installed first::

    # Clone the repository
    git clone https://github.com/simphony/simphony-network.git

    # Install required dependencies
    pip install -r requirements.txt

The next step is straight forward and is based on setuptools::

    # build and install
    python setup.py install

or::

    # build for in-place development
    python setup.py develop


How to Use
~~~~~~~~~~

After installation a new module called `proxy` will be added to the
`simphony.engine` entry point. This module contains a proxy wrapper
which accepts an instance of `ABCModelingEngine` and a `host` name
as input parameters and proxies the wrappers methods to point to a
wrapper which is running remotely on the provided host.

  # Import the proxy wrapper
  from simphony.engine.proxy import ProxyEngine

  # Create a proxy around an existing wrapper
  proxy = ProxyEngine(wrapper, host='pc-115')

  # Access proxy methods
  proxy.run()

.. note::
  `ProxyEngine` only supports `ABCModelingEngine` API and a few custom
  ones which will be explained. Any changes which are applied to `wrapper`
  parameter after initializing the proxy will not be respected.

Testing
-------

To run the full test-suite run::

    python -m unittest discover

Directory structure
-------------------

- simphony_network -- holds the package's implementation
