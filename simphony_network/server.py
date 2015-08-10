"""
This is a utility script to start the SimPhoNy server and listen for
incoming commands.
"""
from threading import Thread

from fabric.api import cd, env, prefix, run, task, settings, execute

from simphony_network import SimphonyApplication
from simphony_network.fabfile import setup_env, deploy, start


class SimphonyFarm(object):
    """Helper to deploy and launch SimPhoNy servers.

    Parameters
    ----------
    hosts: list
        list of host names
    """
    def __init__(self, hosts):
        self._hosts = hosts

    def _run(self):
        """Install and run simphony on remote servers."""
        # Set the env variable
        env.hosts = self._hosts
        with settings(parallel=True):
            # Install virtual environment on remote host if it is not there already
            #execute(setup_env)

            # Deploy the dependencies to the remote virtual environment
            #execute(deploy)

            # Start the server on remote machine
            execute(start)

    def start(self):
        """Deploy and launch the servers."""
        # Initialize the remote server
        t = Thread(target=self._run)
        # The thread will terminate if the parent process terminates.
        # this will consequently terminates the server on the remote machine.
        t.setDaemon(True)
        # Start the thread
        t.start()


def run_server():
    # Instanciate the application with default configuration
    app = SimphonyApplication()

    # Run the application on default port and external IP
    app.run()


if __name__ == '__main__':
    run_server()
