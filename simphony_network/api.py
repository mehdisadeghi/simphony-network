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
                             boundary_conditions,
                             system_parameters,
                             computational_methods,
                             initial_state_data,
                             **kwargs):
        """Create a new wrapper of given type and add it to the wrapper store.

        Parameters
        ----------
        wrapper_type: str
            one of the existing wrappers loaded in simphony.engine, such as
            'JYUEngine'. Bascially this is the class name of the wrapper.

            TODO: This should be changed because it allows to run any arbitrary
            code which is loaded into that entry point.

        boundary_conditions: DataContainer
            boundary conditions

        system_parameters: DataContainer
            boundary conditions

        computational_methods: DataContainer
            boundary conditions

        initial_state_data: dict
            contains 'lattice', 'mesh' and 'particle' keys each with a
            corresponding list containing the elements.

        Returns
        -------
        str
            a uuid string identifying the wrapper
        """
        return self._manager.create_wrapper(wrapper_type,
                                            boundary_conditions,
                                            system_parameters,
                                            computational_methods,
                                            initial_state_data,
                                            **kwargs)

    def run_wrapper(self, wrapper_id):
        """Run the modeling engine recognized by the given id.

        Run the modeling engine using the configured settings (e.g. CM, BC,
        and SP) and the configured state data (e.g. particle, mesh and
        lattice data).
        """
        return self._manager.run_wrapper(wrapper_id)

    def get_wrapper_state(wrapper_id):
        """Return the wrapper state.

        Parameters
        ----------
        wrapper_id: str
            uuid string of the wrapper's id
        """
        return self._manager.get_wrapper_state(wrapper_id)

    def add_lattice(self, wrapper_id, lattice):
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
        return self._manager.add_latice(wrapper_id, lattice)

    def add_mesh(self, wrapper_id, mesh):
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
        return self._manager.add_mesh(wrapper_id, mesh)

    def add_particles(self, wrapper_id, particles):
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
        return self._manager.add_particles(wrapper_id, particles)

    def delete_lattice(self, wrapper_id, name):
        """Delete a lattice

        Parameters
        ----------
        name: str
            name of lattice to be deleted

        """
        return self._manager.delete_lattice(wrapper_id, name)

    def delete_mesh(self, wrapper_id, name):
        """Delete a mesh

        Parameters
        ----------
        name: str
            name of mesh to be deleted

        """
        return self._manager.delete_mesh(wrapper_id, name)

    def delete_particles(self, wrapper_id, name):
        """Delete a particle container for the corresponding modeling engine

        Parameters
        ----------
        id: str
            the modeling engine's id
        name: str
            name of particle container to be deleted

        """
        return self._manager.delete_particles(wrapper_id, name)

    def get_lattice(self, wrapper_id, name):
        """ Get lattice

        The returned lattice can be used to query and update the state of the
        lattice inside the modeling engine.

        Returns
        -------
        ABCLattice

        """
        return self._manager.get_lattice(wrapper_id, name)

    def get_mesh(self, wrapper_id, name):
        """ Get mesh

        The returned mesh can be used to query and update the state of the
        mesh inside the modeling engine.

        Returns
        -------
        ABCMesh

        """
        return self._manager.get_mesh(wrapper_id, name)

    def get_particles(self, wrapper_id, name):
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
        return self._manager.get_particles(wrapper_id, name)

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
