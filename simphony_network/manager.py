"""
This module is part of simphony-network package.

Manager is responsible to handle incoming commands. Moreover,
manager has to keep the state of existing wrappers.
"""
import uuid
import logging
import pkg_resources
import inspect

from simphony.cuds.abc_modeling_engine import ABCModelingEngine

from .proxy import ProxyEngine


class SimphonyManager(object):
    """Middleware between public API and SimPhoNy framework"""
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # A dictionary store to keep created wrappers
        self._wrappers = {}

        # This dictionary keeps results of aforementioned query. Name
        # of wrapper class would be the key and the type (class) would
        # be the value.
        self._wrapper_mapping = {}

        # Find any subclass of ABCModelingEngine which is loaded into
        # `simphony.engine` entry point
        self._find_wrappers()

    def _find_wrappers(self):
        """Find all the loaded wrappers in SimPhoNy entry point"""
        # Load all entry points
        for ep in pkg_resources.iter_entry_points(group="simphony.engine"):
            # Load the modules
            module = ep.load()
            # Iterete over the module contents
            for k, v in module.__dict__.iteritems():
                # If the item is an Engine class add it to the mapping
                if inspect.isclass(v) and issubclass(v, ABCModelingEngine) \
                    and v not in (ABCModelingEngine, ProxyEngine):
                    # Add the type to the mappping dictionary
                    self._wrapper_mapping[k] = v
        self.logger.info('%s wrappers loaded from simphony.engine entry points.' % len(self._wrapper_mapping))

    def create_wrapper(self, wrapper_type, **kwargs):
        """Create a new wrapper of given type and add it to the wrapper store.

        Parameters
        ----------
        wrapper_type: str
            one of the existing wrappers in simphony.engine
        """
        # Check if wrapper is recognized
        if wrapper_type not in self._wrapper_mapping:
            raise Exception('Wrapper %s is not registered.' % wrapper_type)

        # Create a new uuid
        wrapper_id = uuid.uuid4()

        # Instanciate the wrapper
        self._wrappers[str(wrapper_id)] = self._wrapper_mapping[wrapper_type]()

        self.logger.info('Wrapper %s created for %s engine.' % (wrapper_id, wrapper_type))

        return str(wrapper_id)

    def run_wrapper(self, id):
        """Run the modeling engine recognized by the given id.

        Run the modeling engine using the configured settings (e.g. CM, BC,
        and SP) and the configured state data (e.g. particle, mesh and
        lattice data).

        Will raise EngineNotFound error in case of not existing wrapper.
        """
        raise NotImplementedError()

    def add_lattice(self, id, lattice):
        """Add lattice to the correspoinding modeling engine

        Parameters
        ----------
        id: str
            the modeling engine's id
        lattice : ABCLattice
            lattice to be added.

        Returns
        -------
        proxy : ABCLattice
            A lattice to be used to update/query the internal representation
            stored inside the modeling-engine. See get_lattice for more
            information.

        """
        raise NotImplementedError()

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

    def add_particles(self, id, particles):
        """Add particle container to the corresponding modeling engine

        Parameters
        ----------
        id: str
            the modeling engine's id
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

    def delete_particles(self, id, name):
        """Delete a particle container for the corresponding modeling engine

        Parameters
        ----------
        id: str
            the modeling engine's id
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

    def get_particles(self, id, name):
        """ Get particle container from the corresponding modeling engine.

        The returned particle container can be used to query and update the
        state of the particle container inside the modeling engine.

        Parameters
        ----------
        id: str
            the modeling engine's id
        name: str
            name of particle container

        Returns
        -------
        ABCParticles

        """
        raise NotImplementedError()

    def get_wrapper_state(self, wrapper_id):
        """ Get the current state of the given wrapper.

        Parameters
        ----------
        wrapper_id: str
            uuid of the wrapper

        Returns
        -------
        str:
            state of the wrapper according to the WrapperState enum.
        """
        if wrapper_id not in self._wrappers:
            raise Exception('Wrapper[%s] does not exist.' % wrapper_id)

        # Instanciate the wrapper
        #return self._wrappers[wrapper_id].get_state()

        # We have to either introduce WrapperStore to keep track of wrapper states
        # or add state to ABCModelingEngine interface
        raise NotImplementedError()
