import pika.adapters
import pika
import uuid
import json


EXCHANGE = 'chatexchange'
EXCHANGE_TYPE = 'topic'
BINDING_KEY_DEFAULT = 'public.*'
PORT = 5672


# few utility print functions
def pi(msg):
    print '\n[RabbitMQClient] : inside ' + msg.upper() + '()'


def pc(msg):
    print '[RabbitMQClient] : Calling ' + msg.upper() + '() function...'


def ps(msg):
    print '[RabbitMQClient] : Call ' + msg.upper() + '() successful'


def pr(msg):
    print '[RabbitMQClient] : Returning from ' + msg.upper() + '()\n'


def pp(self, msg):
    print '[RabbitMQClient] : ' + msg.upper() + ' PARAMETERS : '
    print 'self._connection = ', self._connection
    print 'self._connected = ', self._connected
    print 'self._connecting = ', self._connecting
    print 'self._channel = ', self._channel
    print 'self._closing = ', self._closing
    print 'self._closed = ', self._closed
    print 'self._consumer_tag = ', self._consumer_tag
    print 'self._deliveries = ', self._deliveries
    print 'self._acked = ', self._acked
    print 'self._nacked = ', self._nacked
    print 'self._message_number = ', self._message_number
    print 'self._credentials = ', self._credentials
    print 'self._parameters = ', self._parameters
    print 'self._queue = ', self._queue
    print 'self.websocket = ', self.websocket
    print 'self._status = ', self._status
    print 'self._person = ', self._person
    print 'self._clientid = ', self._clientid
    print 'self._participants = ', self._participants


class RabbitMqClient(object):
    """
    This is a RabbitMQ Client using the TornadoConnection Adapter that will
    handle unexpected interactions with RabbitMQ such as channel and connection closures.

    If RabbitMQ closes the connection, it will reopen it. You should
    look at the output, as there are limited reasons why the connection may
    be closed, which usually are tied to permission related issues or
    socket timeouts.

    If the channel is closed, it will indicate a problem with one of the
    commands that were issued and that should surface in the output as well.

    It alos uses delivery confirmations and illustrates one way to keep track of
    messages that have been sent and if they've been confirmed by RabbitMQ.

    """

    def __init__(self):
        """Create a new instance of the consumer class, passing in the AMQP
        URL used to connect to RabbitMQ.
        """

        pi('__init__')

        self._connection = None
        self._connected = False
        self._connecting = False
        self._channel = None
        self._closing = False
        self._closed = False
        self._consumer_tag = None
        self._deliveries = []
        self._acked = 0
        self._nacked = 0
        self._message_number = 0
        self._credentials = pika.PlainCredentials('guest', 'guest')
        self._parameters = pika.ConnectionParameters(host='localhost',
                                                     port=PORT,
                                                     virtual_host='/',
                                                     credentials=self._credentials)
        self._queue = 'queue-' + str(uuid.uuid4())
        self.websocket = None
        self._status = 0
        self._person = None
        self._clientid = None
        self._participants = 0

        pp(self, '__INIT__')

        pr('__init__')

    def connect(self):
        """This method connects to RabbitMQ via the Torando Connectoin Adapter, returning the 
        connection handle.

        When the connection is established, the on_connection_open method
        will be invoked by pika.

        :rtype: pika.SelectConnection

        """

        pi('connect')

        if self._connecting:
            print 'RabbitMQClient: Already connecting to RabbitMQ'
            return

        print 'RabbitMQClient: Connecting to RabbitMQ on localhost:5672, Object: %s' % (self,)
        self._connecting = True

        pp(self, 'CONNECT')

        return pika.adapters.TornadoConnection(parameters=self._parameters,
                                               on_open_callback=self.on_connection_opened,
                                               stop_ioloop_on_close=False)

    def on_connection_opened(self, connection):
        """This method is called by pika once the connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.

        :type connection: pika.adapters.TornadoConnection

        """

        pi('on_connection_opened')

        self._status = 1
        self._connected = True
        self._connection = connection
        pc('add_on_connection_close_callback')
        self.add_on_connection_close_callback()
        ps('add_on_connection_close_callback')
        pc('open_channel')
        self.open_channel()
        ps('open_channel')

        pp(self, 'ON_CONNECTION_OPENED')
        pr('on_connection_opened')

    def add_on_connection_close_callback(self):
        """This method adds an on close callback that will be invoked by pika
        when RabbitMQ closes the connection to the publisher unexpectedly.

        """

        pi('add_on_connection_close_callback')

        pc('self._connection.add_on_close_callback')
        self._connection.add_on_close_callback(callback_method=self.on_connection_closed)
        ps('self._connection.add_on_close_callback')

        pp(self, 'ADD_ON_CONNECTION_CLOSE_CALLBACK')
        pr('add_on_connection_close_callback')

    def on_connection_closed(self, connection, reply_code, reply_text):
        """This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.

        :param pika.connection.Connection connection: The closed connection obj
        :param int reply_code: The server provided reply_code if given
        :param str reply_text: The server provided reply_text if given

        """

        pi('on_connection_closed')

        self._channel = None
        self._connecting = False
        self._connected = False
        self._status = 0
        if self._closing:
            print 'connection already closing'
            return
        else:
            print "Connection closed, reopening in 5 seconds: reply_code : [%d] : reply_text : %s " % (reply_code, reply_text)
            pc('self._connection.add_timeout')
            self._connection.add_timeout(5, self.reconnect)
            ps('self._connection.add_timeout')

        pp(self, 'on_connection_closed')
        pr('on_connection_closed')

    def reconnect(self):
        """Will be invoked by the IOLoop timer if the connection is
        closed. See the on_connection_closed method.

        """

        pi('reconnect')

        if not self._closing:

            # Create a new connection
            pc('self.connect')
            self._connection = self.connect()
            ps('self.connect')

        pp(self, 'reconnect')
        pr('reconnect')

    def close_connection(self):
        """This method closes the connection to RabbitMQ."""

        pi('close_connection')

        print 'closing connection'
        if self._closing:
            print 'connection is already closing...'
            return
        self._closing = True
        print 'invoking connection.close() method'
        pc('self._connection.close')
        self._connection.close()
        ps('self._connection.close')
        print 'connnection closed'
        self._connecting = False
        self._connected = False
        if self._channel:
            self._channel = None
        if self._connection:
            self._connection = None
        if self._consumer_tag:
            self._consumer_tag = None
        if self._queue:
            self._queue = None
        if self.websocket:
            self.websocket = None
        self._parameters = None
        self._credentials = None
        self._status = 0
        self._closed = True
        self._person = None

        pp(self, 'close_connection')
        pr('close_connection')

    def open_channel(self):
        """Open a new channel with RabbitMQ by issuing the Channel.Open RPC
        command. When RabbitMQ responds that the channel is open, the
        on_channel_open callback will be invoked by pika.

        """

        pi('open_channel')

        print 'Creating a new channel for connection : ', self._connection
        pc('self._connection.channel')
        self._channel = self._connection.channel(on_open_callback=self.on_channel_open)
        ps('self._connection.channel')

        pp(self, 'open_channel')
        pr('open_channel')

    def on_channel_open(self, channel):
        """This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.

        Since the channel is now open, we'll declare the exchange to use.

        :param pika.channel.Channel channel: The channel object

        """

        pi('on_channel_open')

        self._status = 2
        print 'Channel opened'
        self._channel = channel
        pc('self.add_on_channel_close_callback')
        self.add_on_channel_close_callback()
        ps('self.add_on_channel_close_callback')
        pc('self.setup_exchange')
        self.setup_exchange()
        ps('self.setup_exchange')

        pp(self, 'on_channel_open')
        pr('on_channel_open')

    def close_channel(self):
        """Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.

        """

        pi('close_channel')

        print 'Closing the channel... '
        pc('self._channel.close')
        self._status = 1
        self._channel.close()
        ps('self._channel.close')
        # self._channel = None
        print 'channel closed'
        if self._channel:
            self._channel = None

        pp(self, "close_channel")
        pr('close_channel')

    def add_on_channel_close_callback(self):
        """This method tells pika to call the on_channel_closed method if
        RabbitMQ unexpectedly closes the channel.

        """

        pi('add_on_channel_close_callback')

        print 'Adding channel close callback'
        pc('self._channel.add_on_close_callback')
        self._channel.add_on_close_callback(self.on_channel_closed)
        ps('self._channel.add_on_close_callback')

        pp(self, 'add_on_channel_close_callback')
        pr('add_on_channel_close_callback')

    def on_channel_closed(self, channel, reply_code, reply_text):
        """Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Channels are usually closed if you attempt to do something that
        violates the protocol, such as re-declare an exchange or queue with
        different parameters. In this case, we'll close the connection
        to shutdown the object.

        :param pika.channel.Channel: The closed channel
        :param int reply_code: The numeric reason the channel was closed
        :param str reply_text: The text reason the channel was closed

        """

        pi('on_channel_closed')

        print "Channel %i was closed: reply_code : [%d] reply_text : %s " % (channel, reply_code, reply_text)
        self._status = 1
        print 'now closing connection invoked..'
        pc('self.on_channel_closed')
        self.close_connection()
        ps('self.on_channel_closed')

        pp(self, 'on_channel_closed')
        pr('on_channel_closed')

    def setup_exchange(self):
        """Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC
        command. When it is complete, the on_exchange_declareok method will
        be invoked by pika.

        :param str|unicode exchange_name: The name of the exchange to declare

        """

        pi('setup_exchange')

        print 'Declaring exchange : ', EXCHANGE
        pc('self._channel.exchange_declare')
        self._channel.exchange_declare(exchange=EXCHANGE,
                                       exchange_type=EXCHANGE_TYPE,
                                       durable=True,
                                       auto_delete=False,
                                       nowait=False,
                                       callback=self.on_exchange_declareok)
        ps('self._channel.exchange_declare')

        pp(self, 'setup_exchange')
        pr('setup_exchange')

    def on_exchange_declareok(self, frame):
        """Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC
        command.

        :param pika.Frame.Method unused_frame: Exchange.DeclareOk response frame

        """

        pi('on_exchange_declareok')

        self._status = 3
        print 'Exchange declared'
        pc('self.setup_queue')
        self.setup_queue()
        ps('self.setup_queue')

        pp(self, 'on_exchange_declareok')
        pr('on_exchange_declareok')

    def setup_queue(self):
        """Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.

        :param str|unicode queue_name: The name of the queue to declare.

        """

        pi('setup_queue')

        print 'Declaring queue : for channel object :  ', self._channel
        pc('self._channel.queue_declare')
        self._channel.queue_declare(queue=self._queue,
                                    durable=True,
                                    exclusive=False,
                                    auto_delete=True,
                                    nowait=False,
                                    arguments=None,
                                    callback=self.on_queue_declareok)
        ps('self._channel.queue_declare')

        pp(self, 'setup_queue')
        pr('setup_queue')

    def on_queue_declareok(self, method_frame):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. mand is complete, the on_bindok method will
        be invoked by pika.

        :param pika.frame.Method method_frame: The Queue.DeclareOk frame

        """

        pi('on_queue_declareok')

        self._status = 4
        print 'calling bind_queue method with default BINDING_KEY'
        pc('self.bind_queue')
        self.bind_queue(BINDING_KEY_DEFAULT)
        ps('self.bind_queue')

        pp(self, 'on_queue_declareok')
        pr('on_queue_declareok')

    def bind_queue(self, binding_key):
        """In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command.

        :param string binding_key: The routing_key argument

        """

        pi('bind_queue')

        print 'Binding %s to %s with %s ' % (EXCHANGE, self._queue, binding_key)
        pc('self.channel.queue_bind')
        self._channel.queue_bind(callback=self.on_bindok,
                                 queue=self._queue,
                                 exchange=EXCHANGE,
                                 routing_key=binding_key,
                                 nowait=False,
                                 arguments=None)
        ps('self._ch.queue_bind')

        pp(self, 'bind_queue')
        pr('bind_queue')

    def on_bindok(self, unused_frame):
        """Invoked by pika when the Queue.Bind method has completed. At this
        point we will start consuming messages by calling start_consuming
        which will invoke the needed RPC commands to start the process.
        It will also set channel for publishing.

        :param pika.frame.Method unused_frame: The Queue.BindOk response frame

        """

        pi('on_bindok')

        self._status = 5
        print 'Queue bound '
        print 'invoke setup_publishing and then start_consuming'
        pc('self.setup_publishing')
        self.setup_publishing()
        ps('self.setup_publishing')
        pc('self.start_consuming')
        self.start_consuming()
        ps('self.start_consuming')

        pp(self, 'on_bindok')
        pr('on_bindok')

    def setup_publishing(self):
        """
        In this method we will setup the channel for publishing by making it available
        for delivery confirmations and publisher confirmations.

        """

        pi('setup_publishing')

        print 'enabling delivery confirmations'
        pc('self.enable_delivery_confirmations')
        self.enable_delivery_confirmations()
        ps('self.enable_delivery_confirmations')

        pp(self, 'setup_publishing')
        pr('setup_publishing')

    def enable_delivery_confirmations(self):
        """Send the Confirm.Select RPC method to RabbitMQ to enable delivery
        confirmations on the channel. The only way to turn this off is to close
        the channel and create a new one.

        When the message is confirmed from RabbitMQ, the
        on_delivery_confirmation method will be invoked passing in a Basic.Ack
        or Basic.Nack method from RabbitMQ that will indicate which messages it
        is confirming or rejecting.

        """

        pi('enable_delivery_confirmations')

        print 'Issuing Confirm.Select RPC command'
        pc('self._channel.confirm_delivery')
        self._channel.confirm_delivery(callback=self.on_delivery_confirmation)
        ps('self._channel.confirm_delivery')
        self._status = 6

        pp(self, 'enable_delivery_confirmations')
        pr('enable_delivery_confirmations')

    def on_delivery_confirmation(self, method_frame):
        """Invoked by pika when RabbitMQ responds to a Basic.Publish RPC
        command, passing in either a Basic.Ack or Basic.Nack frame with
        the delivery tag of the message that was published. The delivery tag
        is an integer counter indicating the message number that was sent
        on the channel via Basic.Publish. Here we're just doing house keeping
        to keep track of stats and remove message numbers that we expect
        a delivery confirmation of from the list used to keep track of messages
        that are pending confirmation.

        :param pika.frame.Method method_frame: Basic.Ack or Basic.Nack frame

        """

        pi('on_delivery_confirmation')

        confirmation_type = method_frame.method.NAME.split('.')[1].lower()
        print 'Received %s for delivery tag: %i ' % (confirmation_type,
                                                     method_frame.method.delivery_tag)
        if confirmation_type == 'ack':
            self._acked += 1
        elif confirmation_type == 'nack':
            self._nacked += 1
        self._deliveries.remove(method_frame.method.delivery_tag)
        print 'Published %i messages, %i have yet to be confirmed, %i were acked and %i were nacked ' % (self._message_number, len(self._deliveries), self._acked, self._nacked)

        pp(self, 'on_delivery_confirmation')
        pr('on_delivery_confirmation')

    def publish(self, msg, routing_key):
        """If the class is not stopping, publish a message to RabbitMQ,
        appending a list of deliveries with the message number that was sent.
        This list will be used to check for delivery confirmations in the
        on_delivery_confirmations method.

        Once the message has been sent, schedule another message to be sent.
        The main reason I put scheduling in was just so you can get a good idea
        of how the process is flowing by slowing down and speeding up the
        delivery intervals by changing the PUBLISH_INTERVAL constant in the
        class.

        :param: string msg: Message to be published to Channel
        :param: string routing_key: Routing Key to direct message via the Exchange

        """

        pi('publish')

        print 'msg received : ', msg
        print 'type (msg) : ', type(msg)


        properties = pika.BasicProperties(content_type='application/json',
                                          headers=msg,
                                          delivery_mode=2,
                                          app_id=self._person
                                          )


        print 'convertin msg to json.dumps(msg)..'
        msg = json.dumps(msg, ensure_ascii=False)
        print 'msg after jsonifying : ', msg
        print 'type(msg) after jsonifyin  : ', type(msg)
        pc('self.channel.basic_publish')
        self._channel.basic_publish(exchange=EXCHANGE,
                                    routing_key=routing_key,
                                    body=msg,
                                    properties=properties)
        ps('self.channel.basic_publish')

        self._message_number += 1
        self._deliveries.append(self._message_number)
        print 'Published message '

        pp(self, 'publish')
        pr('publish')

    def start_consuming(self):
        """This method sets up the consumer by first calling
        add_on_cancel_callback so that the object is notified if RabbitMQ
        cancels the consumer. It then issues the Basic.Consume RPC command
        which returns the consumer tag that is used to uniquely identify the
        consumer with RabbitMQ. We keep the value to use it when we want to
        cancel consuming. The on_message method is passed in as a callback pika
        will invoke when a message is fully received.

        """

        pi('start_consuming')

        print 'Issuing consumer related RPC commands'
        pc('self.add_on_cancel_callback')
        self.add_on_cancel_callback()
        ps('self.add_on_cancel_callback')
        pc('self._channel.basic_consume')
        self._consumer_tag = self._channel.basic_consume(consumer_callback=self.on_message,
                                                         queue=self._queue,
                                                         no_ack=False,
                                                         exclusive=True,
                                                         )
        ps('self._channel.basic_consume')
        self._status = 7
        print 'self._status ==7 now'
        print ' rabbit client and now publish/consume msessag. sending first published'
        m = {'msg_type': 'rabbitmqOK'}
        print 'message to be sent before jsonigying : ', m
        pc('slef.websocket.send')
        self.websocket.send(json.dumps(m))
        ps('self.websocket.send')

        pp(self, 'start_consuming')
        pr('start_consuming')

    def add_on_cancel_callback(self):
        """Add a callback that will be invoked if RabbitMQ cancels the consumer
        for some reason. If RabbitMQ does cancel the consumer,
        on_consumer_cancelled will be invoked by pika.

        """

        pi('add_on_cancel_callback')

        print 'Adding consumer cancellation callback'
        pc('self._channel.add_on_cancel_callback')
        self._channel.add_on_cancel_callback(callback=self.on_consumer_cancelled)
        ps('self._channel.add_on_cancel_callback')

        pp(self, 'add_on_cancel_callback')
        pr('add_on_cancel_callback')

    def on_consumer_cancelled(self, method_frame):
        """Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
        receiving messages.

        :param pika.frame.Method method_frame: The Basic.Cancel frame

        """

        pi('on_consumer_cancelled')

        print 'Consumer was cancelled remotely, shutting down.... sent method_frame ', method_frame
        print 'self._channel : ', self._channel
        if self._channel:
            print "inside self._channel not None"
            pc('self.close_channel')
            self.close_channel()
            ps('self.close_channel')

        pp(self, 'on_consumer_cancelled')
        pr('on_consumer_cancelled')

    def on_message(self, unused_channel, basic_deliver, properties, body):
        """Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.

        :param pika.channel.Channel unused_channel: The channel object
        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param str|unicode body: The message body

        """

        pi('on_message')

        print 'Received message # %s from %s : %s ' % (basic_deliver.delivery_tag, properties.app_id, body)
        print 'type of body : ', type(body)
        print 'json decoding the body...'
        json_decoded_body = json.loads(body)
        print 'body after jsong decoded : ', json_decoded_body
        print 'type of json_decoded_body : ', type(json_decoded_body)
        stage = json_decoded_body['stage']
        print 'stage of message : ', stage
        print 'acknowledge the consumed message'
        pc('self.acknowledge_message')
        self.acknowledge_message(basic_deliver.delivery_tag)
        ps('self.acknowledge_message')

        if stage == 'stop' and self._person == json_decoded_body['name']:
            print 'skipping sending messaget to websocket since webscoket is closed.'
            print 'initating closing of rabbitmq Client Connection.....'
            pc('self.stop')
            self.stop()
            ps('self.stop')
        else:
            print 'sending the jsonified string message to websoket...'
            pc('self.websocket.send')
            self.websocket.send(body)
            ps('self.websocket.send')
            

        pp(self, 'on_message')
        pr('on_message')

    def acknowledge_message(self, delivery_tag):
        """Acknowledge the message delivery from RabbitMQ by sending a
        Basic.Ack RPC method for the delivery tag.

        :param int delivery_tag: The delivery tag from the Basic.Deliver frame

        """

        pi('acknowledge_message')

        print 'Acknowledging message ', delivery_tag
        pc('self._channel.basic_ack')
        self._channel.basic_ack(delivery_tag)
        ps('self._channel.basic_ack')

        pp(self, 'acknowledge_message')
        pr('acknowledge_message')

    def stop_consuming(self):
        """Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.

        """

        pi('stop_consuming')

        print 'self._channel : ', self._channel
        if self._channel:
            print 'inside self._channel not None '
            print 'Sending a Basic.Cancel RPC command to RabbitMQ'
            pc('self._channel.basic_cancel')
            self._channel.basic_cancel(callback=self.on_cancelok,
                                       consumer_tag=self._consumer_tag)
            ps('self._channel.basic_cancel')

        pp(self, 'stop_consuming')
        pr('stop_consuming')

    def on_cancelok(self, unused_frame):
        """This method is invoked by pika when RabbitMQ acknowledges the
        cancellation of a consumer. At this point we will close the channel.
        This will invoke the on_channel_closed method once the channel has been
        closed, which will in-turn close the connection.

        :param pika.frame.Method unused_frame: The Basic.CancelOk frame

        """

        pi('on_cancelok')

        print 'RabbitMQ acknowledged the cancellation of the consumer'
        if self._consumer_tag:
            self._consumer_tag = None
        pc('self.close_channel')
        self.close_channel()
        ps('self.close_channel')
        pc('self.close_connection')
        self.close_connection()
        pr('self.close_connection')

        pp(self, 'on_cancelok')
        pr('on_cancelok')

    def start(self):
        """Run the example consumer by connecting to RabbitMQ and then
        starting the IOLoop to block and allow the SelectConnection to operate.

        """

        pi('start')

        pc('self.connect')
        self._connection = self.connect()
        ps('self.connect')
        # self._connection.ioloop.start()

        pp(self, 'start')
        pr('start')

    def stop(self):
        """Cleanly shutdown the connection to RabbitMQ by stopping the consumer
        with RabbitMQ. When RabbitMQ confirms the cancellation, on_cancelok
        will be invoked by pika, which will then closing the channel and
        connection. The IOLoop is started again because this method is invoked
        when CTRL-C is pressed raising a KeyboardInterrupt exception. This
        exception stops the IOLoop which needs to be running for pika to
        communicate with RabbitMQ. All of the commands issued prior to starting
        the IOLoop will be buffered but not processed.

        """

        pi('stop')

        print 'Stopping RabbitMQClient object... : ', self
        pc('self.stop_consuming')
        self.stop_consuming()
        ps('self.stop_consuming')

        print 'RabbitMQClient Stopped'

        pp(self, 'stop')
        pr('stop')

    def status(self):
        """Gives the status of the RabbitMQClient Connection.

        :rtype: self._status

        """

        pi('status')

        return self._status








