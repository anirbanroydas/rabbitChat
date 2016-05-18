import tornado.web
import tornado.escape
import tornado.ioloop
import os
import base64

from sockjs.tornado import SockJSConnection
from rabbitChat.apps.rabbitmq.pubsub import RabbitMqClient


print '\n\ninvoked apps.main.views.py\n'


ioloop = tornado.ioloop.IOLoop.instance()




# few utility print functions for IndexHandler
def pii(msg):
    print '\n[IndexHandler] : inside ' + msg.upper() + '()'


def pci(msg):
    print '[IndexHandler] : Calling ' + msg.upper() + '() function...'


def psi(msg):
    print '[IndexHandler] : Call ' + msg.upper() + '() successful'


def pri(msg):
    print '[IndexHandler] : Returning from ' + msg.upper() + '()\n'




# few utility print functions for ChatWebsocketHandler
def pic(msg):
    print '\n[ChatWebsocketHandler] : inside ' + msg.upper() + '()'


def pcc(msg):
    print '[ChatWebsocketHandler] : Calling ' + msg.upper() + '() function...'


def psc(msg):
    print '[ChatWebsocketHandler] : Call ' + msg.upper() + '() successful'


def prc(msg):
    print '[ChatWebsocketHandler] : Returning from ' + msg.upper() + '()\n'






class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    print "\n\ninvoked IndexHandler\n"

    def get(self):

        pii('get')
        pci('self.render')
        self.render('index.html')
        psi('slef.render')

        pri('get')


websocketParticipants = set()


class ChatWebsocketHandler(SockJSConnection):
    print '\n\nInvoked ChatWebsocketHandler\n'


    def on_open(self, info):

        pic('on_open')

        print 'websocket opened'
        # Initialize new pika rabbitmq client object for this websocket.
        pcc('RabbitMqClient')
        self.rabbit_client = RabbitMqClient()
        psc('RabbitMqClient')

        # Assign websocket object to a Pika client object attribute.
        websocketParticipants.add(self)
        self.rabbit_client.websocket = self
        print 'websocket object : ', self
        print 'starting rabbit client....'
        pcc('self.rabbit_client.start')
        self.rabbit_client.start()
        psc('self.rabbit_client.start')
        print 'rabbit_client started'

        prc('on_open')



    def on_message(self, message):

        pic('on_message')

        print 'websocket message received'
        print 'self participant : ', self
        print "message sent : ", message
        res = tornado.escape.json_decode(message)
        print "json_decode message : ", res
        routing_key = res['routing_key']
        msg = res['msg']
        stage = msg['stage']
        print 'stage of message : ', stage
        if stage == 'start':

            print 'inside stage==start'
            name = msg['name']
            print 'name of person : ', name
            print 'assigning name to rabbitclient object'
            self.rabbit_client._person = name
            self.rabbit_client._clientid = self.genid()
            self.rabbit_client._participants = len(websocketParticipants)
            msg['participants'] = len(websocketParticipants)

            print 'client id : ', self.rabbit_client._clientid
            print 'name assigned to rabbit client object : ', self.rabbit_client._person

        msg['clientid'] = self.rabbit_client._clientid
        print 'routing key : ', routing_key
        print 'msg : ', msg
        print 'Publishing the received message to RabbitMQ'
        pcc('self.rabbit_client.publish')
        self.rabbit_client.publish(msg, routing_key)
        psc('self.rabbit_client.publish')

        prc('on_message')



    def on_close(self):

        pic('on_close')

        print 'self object : ', self
        print("WebSocket Closing")
        print 'closing the RabbiMQ connection...'
        print 'initating broadcasting of disconnection message to all participants...'
        msg = {
            'name': self.rabbit_client._person,
            'stage': 'stop',
            'msg_type': 'public',
            'msg': self.rabbit_client._person + ' left',
            'clientid': self.rabbit_client._clientid,
            'participants': len(websocketParticipants) - 1
        }
        routing_key = 'public.*'
        print 'routing key : ', routing_key
        print 'msg : ', msg
        pcc('self.rabbit_client.publish')
        self.rabbit_client.publish(msg, routing_key)
        psc('self.rabbit_client.publish')

        websocketParticipants.remove(self)
        print 'rabbitmq clinet connection closed'
        print 'websocekt closed'

        prc('on_close')



    def genid(self):
        return base64.urlsafe_b64encode(os.urandom(32)).replace('=', 'e')





