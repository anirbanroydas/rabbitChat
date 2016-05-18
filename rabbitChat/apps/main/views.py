"""
This is the main view module which manages main tornado connections. This module
provides request handlers for managing simple HTTP requests as well as Websocket requests.

Although the websocket requests are actually sockJs requests which follows the sockjs protcol, thus it
provide interface to sockjs connection handlers behind the scene.
"""




import tornado.web
import tornado.escape
import tornado.ioloop
import os
import base64
import logging



from sockjs.tornado import SockJSConnection
from rabbitChat.apps.rabbitmq.pubsub import RabbitMqClient


LOGGER = logging.getLogger(__name__)

# Main threads ioloop, not to be confused with current thread's ioloop
# which is ioloop.IOLoop.current()
ioloop = tornado.ioloop.IOLoop.instance()


# Handles the general HTTP connections
class IndexHandler(tornado.web.RequestHandler):
    """This handler is a basic regular HTTP handler to serve the chatroom page.

    """

    def get(self):
        """
        This method is called when a client does a simple GET request,
        all other HTTP requests like POST, PUT, DELETE, etc are ignored.

        :return: Returns the rendered main requested page, in this case its the chat page, index.html
        """

        LOGGER.info('[IndexHandler] HTTP connection opened')

        self.render('index.html')

        LOGGER.info('[IndexHandler] index.html served')


# no. of websocket connections
websocketParticipants = set()



# Handler for Websocket Connections or Sockjs Connections
class ChatWebsocketHandler(SockJSConnection):
    """ Websocket Handler implementing the sockjs Connection Class which will
    handle the websocket/sockjs connections.
    """

    def on_open(self, info):
        """
        This method is called when a websocket/sockjs connection is opened for the first time.
        
        :param      self  The object
        :param      info  The information
        
        :return:    It returns the websocket object

        """

        LOGGER.info('[ChatWebsocketHandler] Websocket connecition opened: %s ' % self)

        # Initialize new pika rabbitmq client object for this websocket.
        self.rabbit_client = RabbitMqClient()
        # Assign websocket object to a Pika client object attribute.
        websocketParticipants.add(self)
        self.rabbit_client.websocket = self
        # connect to rabbitmq
        self.rabbit_client.start()



    def on_message(self, message):
        """
        This method is called when a message is received via the websocket/sockjs connection
        created initially.
        
        :param      self     The object
        :param      message  The message received via the connection.
        
        :return:     Returns the published message back to all other subscribers.

        """

        LOGGER.info('[ChatWebsocketHandler] message received on Websocket: %s ' % self)

        res = tornado.escape.json_decode(message)
        routing_key = res['routing_key']
        msg = res['msg']
        stage = msg['stage']

        if stage == 'start':
            LOGGER.info('[ChatWebsocketHandler] Message Stage : START')

            name = msg['name']
            # assign name to rabbit client
            self.rabbit_client._person = name
            # assign clientid to rabbit client
            self.rabbit_client._clientid = self.genid()
            # add no. of current participants/websocket connections
            self.rabbit_client._participants = len(websocketParticipants)
            msg['participants'] = len(websocketParticipants)

        msg['clientid'] = self.rabbit_client._clientid

        LOGGER.info('[ChatWebsocketHandler] Publishing the received message to RabbitMQ')

        self.rabbit_client.publish(msg, routing_key)



    def on_close(self):
        """
        This method is called when a websocket/sockjs connection is closed.
        
        :param      self  The object
        
        :return:     Doesn't return anything, except a confirmation of closed connection back to web app.
        """

        LOGGER.info('[ChatWebsocketHandler] Websocket conneciton close event %s ' % self)

        msg = {
            'name': self.rabbit_client._person,
            'stage': 'stop',
            'msg_type': 'public',
            'msg': self.rabbit_client._person + ' left',
            'clientid': self.rabbit_client._clientid,
            'participants': len(websocketParticipants) - 1
        }

        routing_key = 'public.*'

        # publishing the close connection info to rest of the rabbitmq subscribers/clients
        self.rabbit_client.publish(msg, routing_key)

        # removing the connection of global list
        websocketParticipants.remove(self)

        LOGGER.info('[ChatWebsocketHandler] Websocket connection closed')



    def genid(self):
        return base64.urlsafe_b64encode(os.urandom(32)).replace('=', 'e')





