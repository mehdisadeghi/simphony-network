"""
This module is part of simphony-network package.

This module will be loaded into `simphony.engines` entry point as `proxy`.
The `ProxyEngine` which is defined here is the only class that end users
need to know about. They have to wrap their normal wrapper instances inside
this class to take advantage of SimPhoNy network layer.
"""
import logging

import msgpack_numpy as mn
mn.patch()
import zerorpc
from simphony.cuds.abc_modeling_engine import ABCModelingEngine

from .constants import WrapperState
from .fabfile import setup_env, deploy, start


class ProxyEngine(ABCModelingEngine):
    """A proxy around wrapper methods.

    Args:
        cuds: CUDS
            the object containing all the model data
        engine: str
            name of the engine to run the model
        host: str
            the host to run the simulation there
        port: int
            port for the server to listen at
    """

    def __init__(self, cuds, engine, host, port=8020):
        # The CUDS object contains all the data regarding the model
        self._cuds = cuds

        # Name of the engine to execute
        self._engine_name = engine

        # The remote host to connect to
        self._host = host

        # The remote port to connect to
        self._port = port

        # Create the proxy to the remote host.
        self._remote = \
            zerorpc.Client("tcp://{host}:{port}".format(host=self._host,
                                                        port=self._port))
        # Tell what we just did
        logging.info('Created zerorpc proxy to remote host at %s:%s' % (host, port))

        # Keep the last state of the remote wrapper
        self._last_state = None

        # Keep the id of the remote wrapper internally.
        self._wrapper_id = None

        # Initial state data
        self._state_data = {}

    @property
    def BC(self):
        """A proxy for remote BC"""
        return self._cuds.BC

    @BC.setter
    def BC(self, value):
        """Set boundary conditions on remote engine.

        Parameters
        ----------
        value: DataContainer
            a dictionary of boundary conditions
        """
        raise NotImplementedError('Changing BC is not allowed after initializing the proxy.')

    @property
    def SP(self):
        """A proxy for remote SP"""
        return self._cuds.SP

    @SP.setter
    def SP(self, value):
        """Set system parameters on remote engine.

        Parameters
        ----------
        value: DataContainer
            a dictionary of system parameters
        """
        raise NotImplementedError('Changing SP is not allowed after initializing the proxy.')

    @property
    def CM(self):
        """A proxy for remote CM"""
        return self._cuds.CM

    @CM.setter
    def CM(self, value):
        """Set computational methods on remote engine.

        Parameters
        ----------
        value: DataContainer
            a dictionary of computational methods
        """
        raise NotImplementedError('Changing CM is not allowed after initializing the proxy.')

#    def _get_wrapper_name(self):
#        """Return the name of the wrapper."""
#        return type(self._engine).__name__

    def run(self):
        """Run the wrapper on the remote host."""
        # Extract wrapper's name out of its type information
        #wrapper_name = self._get_wrapper_name()
        wrapper_name = self._engine_name

        print self._cuds.SD
        print self._cuds.BC
        print self._cuds.SP
        print self._cuds.CM
        # First create the wrapper along with passing model data
        self._wrapper_id = self._remote.create_wrapper(wrapper_name,
                                                       self._cuds.BC,
                                                       self._cuds.SP,
                                                       self._cuds.CM,
                                                       self._cuds.SD)
        print('Got the id: %s' % self._wrapper_id)
        logging.info('Wrapper %s created.' % self._wrapper_id)

        # Now issue the run command
        self._remote.run_wrapper(self._wrapper_id)

        # Return the id, just for fun
        return self._wrapper_id

    def add_dataset(self, dataset):
        """Add a dataset to the correspoinding modeling engine

        Parameters
        ----------
        dataset : ABCLattice, ABCMesh or ABCParticles
            dataset to be added.

        Returns
        -------
        proxy : ABCLattice, ABCMesh or ABCParticles
            A dataset to be used to update/query the internal representation
            stored inside the modeling-engine.
        """
        if self._wrapper_id is not None:
            raise Exception('Can not change state data after running the wrapper.')

        # Add latice to the engine
        self._engine.add_dataset(dataset)

        if dataset is ABCLattice:
            # Queue the lattice to be added to the remote engine
            if 'lattice' not in self._state_data:
                self._state_data['lattice'] = []
            self._state_data['lattice'].append(lattice)
        print('Hey, I am proxy.py and here is the state data %s' % self._state_data)

    def remove_dataset(self, wrapper_id, name):
        """Remove a dataset from the correspoinding modeling engine

        Parameters
        ----------
        id: str
            the modeling engine's id
        name: str
            name of the dataset to be deleted
        """
        raise NotImplementedError()


    def get_dataset(self, wrapper_id, name):
        """Get a dataset from the correspoinding modeling engine

        Parameters
        ----------
        id: str
            the modeling engine's id
        name: str
            name of the dataset

        Returns
        -------
        ABCMesh or ABCLattice or ABCParticles
        """
        raise NotImplementedError()

    def iter_datasets(self, names=None):
        """Iterate over a subset or all of the lattices.

        Parameters
        ----------
        names : sequence of str, optional
            names of specific lattices to be iterated over. If names is not
            given, then all lattices will be iterated over.

        Yields
        -------
        ABCLattice
        """
        raise NotImplementedError()

    # Proxy specific methods, not available in the base class
    def get_state(self):
        """Return the current state of the wrapper"""
        # Complain if the wrapper_id is not known yet, give some hints.
        if self._wrapper_id is None:
            raise Exception("I don't have the wrapepr_id yet. Did you run the wrapper?")

        # Ask the remote simphony for the state of the given wrapper_id
        return self._remote.get_wrapper_state(self._wrapper_id)
