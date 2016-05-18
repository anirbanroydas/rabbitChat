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


Features
---------

* Public chat
* Shows who joined and who left
* Shows number of people online
* Shows who is typing and who is not
* Join/Leave chat room features




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
 
 * *For* ``Mac`` *Users*
 
   1. Brew Install RabbitMQ
   ::

         $ brew install rabbitmq

   2. Configure RabbitMq, follow this `link <https://www.rabbitmq.com/install-homebrew.html>`_, this `one <https://www.rabbitmq.com/install-standalone-mac.html>`_ and  `this <https://www.rabbitmq.com/configure.html>`_.

 * *For* ``Ubuntu/Linux`` *Users*

   1. Enable RabbitMQ application repository
   ::
           
           $ echo "deb http://www.rabbitmq.com/debian/ testing main" >> /etc/apt/sources.list

   2. Add the verification key for the package
   ::

         $ wget -o http://www.rabbitmq.com/rabbitmq-signing-key-public.asc | sudo apt-key add -

   3. Update the sources with our new addition from above
   :: 

         $ apt-get update

  
   4. And finally, download and install RabbitMQ
   ::

         $ sudo apt-get install rabbitmq-server

 

   5. Configure RabbitMQ, follow this `link <http://www.rabbitmq.com/install-debian.html>`_, this `one <https://www.rabbitmq.com/configure.html>`_  and `this <https://www.digitalocean.com/community/tutorials/how-to-install-and-manage-rabbitmq>`_. 



Usage
-----

After having installed rabbitChat, just the run the following commands to use it:

* **RabbitMQ Server**
  
  1. *For* ``Mac`` *Users*
  ::
          
          # start normally
          $ rabbitmq-server
           
          # If you want to run in background
          $ rabbitmq-server --detached 

          # start using brew rervices (doesn't work with tmux)
          $ brew services rabbitmq start

  2. *For* ``Ubuntu/LInux`` *Users*
  ::

          # start normally
          $ rabbitmq-server

          # If you want to run in background
          $ rabbitmq-server --detached

          # To start using service
          $ service rabbitmq-server start

          # To stop using service
          $ service rabbitmq-server stop
          
          # To restart using service
          $ service rabbitmq-server restart
          
          # To check the status
          $ service rabbitmq-server status



* **Start rabbitChat Server**
  ::

          $ rabbitChat [options]

  - **Options**

    :--port: Port number where the chat server will start


  - **Example**
    ::

          $ rabbitChat --port=9191

  
* **Stop rabbitChat Server**

  Click ``Ctrl+C`` to stop the server.



Todo
-----

1. Add Private Chat functionality.
   
2. Manage Presence Management, sent, delivered acknowledgements.

3. Message Persistence and delivery of messages to offline clinets.

4. Add Blog post regarding this topic.


