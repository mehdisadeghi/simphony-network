"""
This module is part of simphony-network package.

This module will be loaded into `simphony.engines` entry point as `proxy`.
The `ProxyEngine` which is defined here is the only class that end users
need to know about. They have to wrap their normal wrapper instances inside
this class to take advantage of SimPhoNy network layer.
"""
import logging

from simphony.cuds.abc_modeling_engine import ABCModelingEngine

from .constants import WrapperState


class ProxyEngine(ABCModelingEngine):
    """A proxy around wrapper methods"""
    def __init__(self, engine, host, port=8020):
        # Store the engine, we only need to extract some information from this
        # engine, actually we don't need it at all.
        self._local_engine = engine

        # Create the proxy to the remote host.
        self._remote = \
            zerorpc.Client("tcp://{host}:{port}".format(host=host,
                                                        port=port))
        # Tell what we just did
        logging.info('Created zerorpc prox to remote host at %s:%s' % (host, port))

        # Keep the last state of the remote wrapper
        self._last_state = None

        # Keep the id of the remote wrapper internally.
        self._wrapper_id = None

    def run(self):
        """Run the wrapper on the remote host."""
        # First create the wrapper
        self._wrapper_id = self._remote.create_wrapper(self.engine.__name__)

        # Now issue the run command
        self._remote.run_wrapper(self._wrapper_id)

        # Return the id, just for fun
        return self._wrapper_id

    # Proxy specific methods, not available in the base class
    def get_state(self):
        """Return the current state of the wrapper"""
        # Complain if the wrapper_id is not known yet, give some hints.
        if self._wrapper_id is None:
            raise Exception("I don't have the wrapepr_id yet. Did you run the wrapper?")

        # Ask the remote simphony for the state of the given wrapper_id
        return self._remote.get_wrapper_state(self._wrappre_id)
