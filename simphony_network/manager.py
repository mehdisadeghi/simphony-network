"""
This module is part of simphony-network package.

Manager is responsible to handle incoming commands. Moreover,
manager has to keep the state of existing wrappers.
"""
import uuid
import pickle
import logging
import pkg_resources
import inspect

from simphony.cuds.abc_modeling_engine import ABCModelingEngine

from .proxy import ProxyEngine


class SimphonyManager(object):
    """Middleware between public API and SimPhoNy framework"""
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('simphony')

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

    def create_wrapper(self, wrapper_type,
                             cuds,
                             **kwargs):
        """Create a new wrapper of given type and add it to the wrapper store.

        Parameters
        ----------
        wrapper_type: str
            one of the existing wrappers in simphony.engine

        cuds: CUDSModel
            contains the following attributes
                BC: DataContainer
                    boundary conditions

                SP: DataContainer
                    system_parameters

                CM: DataContainer
                    computational_methods

                SD: dict
                    contains CUDS datasets e.g. 'lattice', 'mesh' and 'particle'

        Returns
        -------
        str
            a uuid string identifying the wrapper
        """
        # Check if wrapper is recognized
        if wrapper_type not in self._wrapper_mapping:
            self.logger.error('Wrapper %s is not registered.' % wrapper_type)
            raise Exception('Wrapper %s is not registered.' % wrapper_type)

        # Create a new uuid
        wrapper_id = uuid.uuid4()

        # Instanciate the wrapper
        wrapper = self._wrapper_mapping[wrapper_type]()

        # Unpickle cuds
        cuds = pickle.loads(cuds)

        # Assign model data to the wrapper
        wrapper.BC = cuds.BC #boundary_conditions
        wrapper.CM = cuds.CM #computational_methods
        wrapper.SP = cuds.SP #system_parameters

        # Report back
        self.logger.debug('Model data assigned to the wrapper %s' % wrapper_id)

        # Add initial state data
        for ds in cuds.SD.itervalues():
            wrapper.add_dataset(ds)

        # Keep the reference to the wrapper
        self._wrappers[str(wrapper_id)] = wrapper

        # Report back
        self.logger.info('Wrapper %s created for %s engine.' % (wrapper_id, wrapper_type))

        # Reutrn the wrapper id
        return str(wrapper_id)

    def run_wrapper(self, wrapper_id):
        """Run the modeling engine recognized by the given id.

        Run the modeling engine using the configured settings (e.g. CM, BC,
        and SP) and the configured state data (e.g. particle, mesh and
        lattice data).

        Parameters
        ----------
        wrapper_: str
            the modeling engine's id
        """
        wrapper = self._wrappers[wrapper_id]
        wrapper.run()

    def add_dataset(self, wrapper_id, dataset):
        """Add a dataset to the correspoinding modeling engine

        Parameters
        ----------
        id: str
            the modeling engine's id
        dataset : ABCLattice, ABCMesh or ABCParticles
            dataset to be added.
        """
        raise NotImplementedError()

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
