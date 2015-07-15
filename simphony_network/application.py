"""
This module is part of simphony-network package.

`SimphonyApplication` class acts as a network server that provides
means of network interaction. Upon running the application it will
listen to incoming messages on the given port. Moreover it can send
messages to the interestd clients about the events which happen inside
the server.

This class acts like a router, it forwards the messags to the manager
object which is defined in the beginning. The rest of interactions between
application object and the rest of application will hapen utilizing signals.
"""
import logging

import gevent
import zmq.green as zmq
import zerorpc
import msgpack
# Monkey patching msgpack to support numpy arrays
import msgpack_numpy as mn
mn.patch()
from blinker import signal

from . import constants
from .api import SimphonyAPI
from .manager import SimphonyManager


class SimphonyApplication(object):
    """Top level SimPhoNy server"""
    def __init__(self, config=None):
        """Create a SimPhoNy appliction object.

        Parameters
        ----------
        config: dict
            a dictionary containing configuration key/values.
        """
        if not config:
            config = {'API_PORT': 8020,
                      'PUB_PORT': 8021,
                      'SERVER_IP': '0.0.0.0',
                      'LOG_LEVEL': logging.DEBUG}
        self.config = config
        self.manager = SimphonyManager(self.config)
        # Configure main logger
        self.logger = logging.getLogger('simphony')
        self.logger.propagate = False
        ch = logging.StreamHandler()
        fmt = '%(levelname)s:%(name)s:l%(lineno)s:p' + str(config['API_PORT']) + '\t %(message)s'
        formatter = logging.Formatter(fmt)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.setLevel(config['LOG_LEVEL'])

    def get_api_endpoint(self):
        """Return the api endpoint
        """
        return "tcp://%s:%s" % (self.config['SERVER_IP'], self.config['API_PORT'])

    def run(self):
        """Run SimPhoNy server loop. Will run for ever."""
        gevent.joinall([gevent.spawn(self._run_api_listener),
                        gevent.spawn(self._run_publisher)])

    def _run_api_listener(self):
        """Run API listener. Will listen for incoming commands."""
        conn_string = "tcp://{ip}:{port}".format(ip=self.config['SERVER_IP'],
                                                 port=self.config['API_PORT'])
        self.logger.info("Starting API at %s" % conn_string)
        #self._register_handlers()
        self.api = SimphonyAPI(self.manager)
        s = zerorpc.Server(self.api)
        s.bind(conn_string)
        s.run()

    def _run_publisher(self):
        """Run the publisher channel. Will publish messages."""
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        self.logger.info('Starting publisher at tcp://*:%s' % self.config['PUB_PORT'])
        socket.bind("tcp://%s:%s" % (self.config['SERVER_IP'], self.config['PUB_PORT']))

        def publish_handler(sender, topic=None, **kwargs):
            """Handle publish requests.

            Parameters
            ----------
            topic: int
                an integer designating type of a message.
            """
            if not topic:
                raise Exception("No topic given. Won't publish anything without it.")

            # ZMQ only transports the messages, it's up to us to decide the format
            packed = msgpack.packb(kwargs)

            # Send the packed message with corresponding topic.
            # Topics will be used to categorize published messages.
            # Listener can ignore certain topics and only get what they want.
            socket.send('%s %s' % (topic, packed))

        # Here we create the publish signal. Anyone intrested in publishing
        # a message to clients will have to get this signal instance and use
        # it to send a message. Afterwards the publish_hander defined below
        # will send the message to subscribers. This way the coupling between
        # application and other parts of it is much weaker, which is desired.
        publish = signal(constants.PUBLISH_SIGNAL)
        # passing `weak` parameter we make sure that the handler will not be
        # removed when it goes out of scope.
        publish.connect(publish_handler, weak=False)
