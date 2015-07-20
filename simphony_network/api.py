"""
This module is part of simphony-network package.

The public API of the running simphony application is defined here.
Only these methods will be available remotely.
"""
import zerorpc


class SimphonyAPI(object):
    """
    Public API to be exposed.
    """
    def __init__(self, manager):
        self._manager = manager

    def echo(self, msg):
        """Echos the given message.

        Parameters
        ----------
        msg: str
            a text message
        """
        return msg

    def create_wrapper(self, wrapper_type,
                             cuds,
                             **kwargs):
        """Create a new wrapper of given type and add it to the wrapper store.

        Parameters
        ----------
        wrapper_type: str
            one of the existing wrappers loaded in simphony.engine, such as
            'JYUEngine'. Bascially this is the class name of the wrapper.

            TODO: This should be changed because it allows to run any arbitrary
            code which is loaded into that entry point.

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
        return self._manager.create_wrapper(wrapper_type,
                                            cuds,
                                            **kwargs)

    def run_wrapper(self, wrapper_id):
        """Run the modeling engine recognized by the given id.

        Run the modeling engine using the configured settings (e.g. CM, BC,
        and SP) and the configured state data (e.g. particle, mesh and
        lattice data).
        """
        return self._manager.run_wrapper(wrapper_id)

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
        return self._manager.get_wrapper_state(wrapper_id)

    def add_dataset(self, wrapper_id, dataset):
        """Add a dataset to the correspoinding modeling engine

        Parameters
        ----------
        id: str
            the modeling engine's id
        dataset : ABCLattice, ABCMesh or ABCParticles
            dataset to be added.
        """
        return self._manager.add_dataset(wrapper_id, dataset)

    def remove_dataset(self, wrapper_id, name):
        """Remove a dataset from the correspoinding modeling engine

        Parameters
        ----------
        id: str
            the modeling engine's id
        name: str
            name of the dataset to be deleted
        """
        return self._manager.remove_dataset(wrapper_id, name)


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
        return self._manager.get_dataset(wrapper_id, name)
