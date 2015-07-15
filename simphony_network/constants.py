"""
This module is part of simphony-network package.

Here are the constants that are being used in this package.
"""
from enum import Enum

# Wrapper state changes
WRAPPER_STATE_CHANGE_TOPIC = 10014

# Shout over the network
PUBLISH_SIGNAL = 'publish'


# An enum to represent different states of a wrapper object
class WrapperState(Enum):
    # Wrapper is just instanciated
    init = 'init'
    # Wrapper is running, i.e. `run` method is called
    running = 'running'
    # `run` method is finished successfully
    done = 'done'
    # `run` method call is failed
    failed = 'failed'
