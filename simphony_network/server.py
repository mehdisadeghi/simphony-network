"""
This is a utility script to start the SimPhoNy server and listen for
incoming commands.
"""
from simphony_network import SimphonyApplication

def run_server():
    # Instanciate the application with default configuration
    app = SimphonyApplication()

    # Run the application on default port and external IP
    app.run()


if __name__ == '__main__':
    run_server()
