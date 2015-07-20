"""
This module is part of simphony-network package.

"""
from simphony.core.data_container import DataContainer
from simphony.cuds.abstractlattice import ABCLattice
from simphony.cuds.abstractmesh import ABCMesh
from simphony.cuds.abstractparticles import ABCParticles


class CUDS(dict):
    """Common Universal Data Structure DTO.

    CUDS objects keep all the information required to run a simulation.

    Attributes
    ----------
    BC : DataContainer
        container of attributes related to the boundary conditions
    CM : DataContainer
        container of attributes related to the computational method
    SP : DataContainer
        container of attributes related to the system parameters/conditions
    SD : list
        container of entities related to the state data
    """
    def __init__(self, bc=None, cm=None, sp=None, sd=None):
        self._BC = bc or DataContainer()
        self._CM = cm or DataContainer()
        self._SP = sp or DataContainer()
        self._SD = sd or {} #Some JYU containers are not included in cuba

    @property
    def BC(self):
        """Boundary conditions"""
        return self._BC

    @property
    def SP(self):
        """System parameters"""
        return self._SP

    @property
    def CM(self):
        """Computational methods"""
        return self._CM

    @property
    def SD(self):
        """State data"""
        return self._SD
