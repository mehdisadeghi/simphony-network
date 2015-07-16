"""
This module is part of simphony-network package.

This module will be loaded into `simphony.engines` entry point as `proxy`.
The `ProxyEngine` which is defined here is the only class that end users
need to know about. They have to wrap their normal wrapper instances inside
this class to take advantage of SimPhoNy network layer.
"""
import logging
from threading import Thread

import zerorpc
from fabric.api import settings
from simphony.cuds.abc_modeling_engine import ABCModelingEngine

from .constants import WrapperState
from .fabfile import setup_env, deploy, start


class ProxyEngine(ABCModelingEngine):
    """A proxy around wrapper methods"""

    def __init__(self, engine, host, port=8020):
        # Store the engine, we only need to extract some information from this
        # engine, actually we don't need it at all.
        self._engine = engine

        self._host = host
        self._port = port

        # Create the proxy to the remote host.
        self._remote = \
            zerorpc.Client("tcp://{host}:{port}".format(host=self._host,
                                                        port=self._port))
        # Tell what we just did
        logging.info('Created zerorpc prox to remote host at %s:%s' % (host, port))

        # Keep the last state of the remote wrapper
        self._last_state = None

        # Keep the id of the remote wrapper internally.
        self._wrapper_id = None

        # Initial state data
        self._state_data = {}

    def _init_remote(self):
        """Install and run simphony on remote server."""
        with settings(host_string=self._host):
            # Install virtual environment on remote host if it is not there already
            setup_env()

            # Deploy the dependencies to the remote virtual environment
            #deploy()

            # Start the server on remote machine
            start()

    @property
    def BC(self):
        """A proxy for remote BC"""
        return self._engine.BC

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
        return self._engine.SP

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
        return self._engine.CM

    @CM.setter
    def CM(self, value):
        """Set computational methods on remote engine.

        Parameters
        ----------
        value: DataContainer
            a dictionary of computational methods
        """
        raise NotImplementedError('Changing CM is not allowed after initializing the proxy.')

    def _get_wrapper_name(self):
        """Return the name of the wrapper."""
        return type(self._engine).__name__

    def run(self):
        """Run the wrapper on the remote host."""
        # Initialize the remote server
        t = Thread(target=self._init_remote)
        # The thread will terminate if the parent process terminates.
        # this will consequently terminates the server on the remote machine.
        t.setDaemon(True)
        # Start the thread
        t.start()

        # Extract wrapper's name out of its type information
        wrapper_name = self._get_wrapper_name()

        # First create the wrapper along with passing model data
        self._wrapper_id = self._remote.create_wrapper(wrapper_name,
                                                       self._engine.BC,
                                                       self._engine.SP,
                                                       self._engine.CM,
                                                       self._state_data)
        print('Got the id: %s' % self._wrapper_id)
        logging.info('Wrapper %s created.' % self._wrapper_id)

        # Now issue the run command
        #self._remote.run_wrapper(self._wrapper_id)

        # Return the id, just for fun
        return self._wrapper_id


    def add_lattice(self, lattice):
        """Add lattice to the correspoinding modeling engine

        Parameters
        ----------
        lattice : ABCLattice
            lattice to be added.

        Returns
        -------
        proxy : ABCLattice
            A lattice to be used to update/query the internal representation
            stored inside the modeling-engine. See get_lattice for more
            information.

        """
        if self._wrapper_id is not None:
            raise Exception('Can not change state data after running the wrapper.')

        # Add latice to the engine
        self._engine.add_lattice(lattice)

        # Queue the lattice to be added to the remote engine
        if 'lattice' not in self._state_data:
            self._state_data['lattice'] = []
        self._state_data['lattice'].append(lattice)

    def add_mesh(self, mesh):
        """Add mesh to the modeling engine

        Parameters
        ----------
        mesh: ABCMesh
            mesh to be added.

        Returns
        -------
        proxy : ABCMesh
            A proxy mesh to be used to update/query the internal representation
            stored inside the modeling-engine. See get_mesh for more
            information.
        """
        raise NotImplementedError()

    def add_particles(self, particles):
        """Add particle container to the corresponding modeling engine

        Parameters
        ----------
        particles: ABCParticles
            particle container to be added.

        Returns
        -------
        ABCParticles
            A particle container to be used to update/query the internal
            representation stored inside the modeling-engine. See
            get_particles for more information.

        """
        raise NotImplementedError()

    def delete_lattice(self, name):
        """Delete a lattice

        Parameters
        ----------
        name: str
            name of lattice to be deleted

        """
        raise NotImplementedError()

    def delete_mesh(self, name):
        """Delete a mesh

        Parameters
        ----------
        name: str
            name of mesh to be deleted

        """
        raise NotImplementedError()

    def delete_particles(self, name):
        """Delete a particle container for the corresponding modeling engine

        Parameters
        ----------
        name: str
            name of particle container to be deleted

        """
        raise NotImplementedError()

    def get_lattice(self, name):
        """ Get lattice

        The returned lattice can be used to query and update the state of the
        lattice inside the modeling engine.

        Returns
        -------
        ABCLattice

        """
        raise NotImplementedError()

    def get_mesh(self, name):
        """ Get mesh

        The returned mesh can be used to query and update the state of the
        mesh inside the modeling engine.

        Returns
        -------
        ABCMesh

        """
        raise NotImplementedError()

    def get_particles(self, name):
        """ Get particle container from the corresponding modeling engine.

        The returned particle container can be used to query and update the
        state of the particle container inside the modeling engine.

        Parameters
        ----------
        name: str
            name of particle container

        Returns
        -------
        ABCParticles

        """
        raise NotImplementedError()

    def iter_lattices(self, names=None):
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

    def iter_meshes(self, names=None):
        """Iterate over a subset or all of the meshes.

        Parameters
        ----------
        names : sequence of str, optional
            names of specific meshes to be iterated over. If names is not
            given, then all meshes will be iterated over.

        Yields
        -------
        ABCMesh

        Raises
        ------
        NotImplementedError
           always.
        """
        raise NotImplementedError()

    def iter_particles(self, names=None):
        """Iterate over a subset or all of the particle containers.

        Parameters
        ----------
        names : sequence of str, optional
            names of specific particle containers to be iterated over.
            If names is not given, then all particle containers will
            be iterated over.

        Yields
        -------
        ABCParticles

        Raises
        ------
        NotImplementedError
           always.
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
