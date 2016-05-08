=====================
rabbitChat
=====================

A Chat-Server/Chat-System based on AMQP protocol(RabbitMQ Message Broker)

**Home Page :** https://pypi.python.org/pypi/rabbitChat


Details
--------

:Author: Anirban Roy Das
:Email: anirban.nick@gmail.com
:Copyright(C): 2016, Anirban Roy Das <anirban.nick@gmail.com>

Check ``rabbitChat/LICENSE`` file for full Copyright notice.


Overview
---------

rabbitChat is a very simple Chat Server which can be set up locally to chat in your LAN. It supports both **Public Chat** among all participants connected simultaneously at a particular time and also **Private Chat** betweent those individual participants.

It uses the `AMQP <https://www.amqp.org/>`_  protocol to implement the real time message passing system. **AMQP** is implemented in many languages and in many softwares, once of such is `RabbitMQ <https://www.rabbitmq.com/>`_ , which is a message broker implementing the `AMQP <https://www.amqp.org/>`_ protocol.

The connection is created using the `sockjs <https://github.com/sockjs/sockjs-client>`_ protocol. **SockJS** is implemented in many languages, primarily in Javascript to talk to the servers in real time, which tries to create a duplex bi-directional connection between the **Client(browser)** and the **Server**. Ther server should also implement the **sockjs** protocol. Thus using the  `sockjs-tornado <https://github.com/MrJoes/sockjs-tornado>`_ library which exposes the **sockjs** protocol in `Tornado <http://www.tornadoweb.org/>`_ server.

It first tries to create a `Websocket <https://en.wikipedia.org/wiki/WebSocket>`_ connection, and if it fails then it fallbacks to other transport mechanisms, such as **Ajax**, **long polling**, etc. After the connection is established, the tornado server**(sockjs-tornado)** connects to **rabbitMQ** via AMQP protocol using the **AMQP Python Client Library**, `Pika <https://pypi.python.org/pypi/pika>`_. 

Thus the connection is *web-browser* to *tornado* to *rabbitMQ* and vice versa.



Technical Specs
----------------


:sockjs-client: Advanced Websocket Javascript Client
:Tornado: Async Python Web Library + Web Server
:sockjs-tornado: SockJS websocket server implementation for Tornado
:AMQP: Advance Message Queuing Protocol used in Message Oriented Middleware
:pika: AMQP Python Client Library
:RabbitMQ: A Message Broker implementing AMQP


Installation
------------

Prerequisites
~~~~~~~~~~~~~

1. python 2.7+
2. tornado
3. sockjs-tornado
4. sockjs-client
5. pika
6. rabbitMQ


Install
~~~~~~~
::

        $ pip install rabbitChat

If above dependencies do not get installed by the above command, then use the below steps to install them one by one.

 **Step 1 - Install pip**

 Follow the below methods for installing pip. One of them may help you to install pip in your system.

 * **Method 1 -**  https://pip.pypa.io/en/stable/installing/

 * **Method 2 -** http://ask.xmodulo.com/install-pip-linux.html

 * **Method 3 -** If you installed python on MAC OS X via ``brew install python``, then **pip** is already installed along with python.


 **Step 2 - Install tornado**
 ::

         $ pip install tornado

 **Step 3 - Install sockjs-tornado**
 ::

         $ pip install sockjs-tornado


 **Step 4 - Install pika**
 ::

         $ pip install pika

 **Step 5 - Install RabbitMQ**
 ::

         $ brew install rabbitmq


Usage
-----

After having installed rabbitChat, just the run the following commands to use it:

* **Start Server**
  ::

          $ rabbitChat [options]

* **Options**

  :--port: Port number where the chat server will start


* **Example**
  ::

          $ rabbitChat --port=9191

  
* **Stop Server**

  Click ``Ctrl+C`` to stop the server.


TODO

1. Add Private Chat functionality.
   
2. Manage Presence Management, sent, delivered acknowledgements.

3. Message Persistence and delivery of messages to offline clinets.

4. Add Blog post regarding this topic.


