Installation
=============

Prerequisites
--------------

1. python 2.7+
2. tornado
3. sockjs-tornado
4. sockjs-client
5. pika
6. rabbitMQ
   
   
Install
-------
::
        
        $ pip install rabbitChat
        
                               
If above dependencies do not get installed by the above command, then use the below steps to install them one by one.
 
 **Step 1 - Install pip**
 
 Follow the below methods for installing pip. One of them may help you to install pip in your system.
 
 * **Method 1 -**  https://pip.pypa.io/en/stable/installing/
   
 * **Method 2 -** http://ask.xmodulo.com/install-pip-linux.html
   
 * **Method 3 -** If you installed python on MAC OS X via ``brew install python``, then **pip** is already installed along with python.
   
   
 **Step 2 - Install tornado**::
         
         $ pip install tornado


 **Step 3 - Install sockjs-tornado** ::
         
         $ pip install sockjs-tornado
         
 **Step 4 - Install pika** ::
         
         $ pip install pika 
         
 **Step 5 - Install RabbitMQ**  
 
 * *For* ``Mac`` *Users*  

   1. Brew Install RabbitMQ ::
      
      $ brew install rabbitmq   


   2. Configure RabbitMq, follow this `link <https://www.rabbitmq.com/install-homebrew.html>`_, this `one <https://www.rabbitmq.com/install-standalone-mac.html>`_ and  `this <https://www.rabbitmq.com/configure.html>`_. 
      
 * *For* ``Ubuntu/Linux`` *Users* 
   
   1. Enable RabbitMQ application repository
      ::                      
              
              $ echo "deb http://www.rabbitmq.com/debian/ testing main" >> /etc/apt/sources.list   
           
   2. Add the verification key for the package
      ::
              
              $ wget -o http://www.rabbitmq.com/rabbitmq-signing-key-public.asc | sudo apt-key add -
   
   3. Update the sources with our new addition from above ::
      
      $ apt-get update 
      
   4. And finally, download and install RabbitMQ 
      ::
              
              $ sudo apt-get install rabbitmq-server   
   5. Configure RabbitMQ, follow this `link <http://www.rabbitmq.com/install-debian.html>`_, this `one <https://www.rabbitmq.com/configure.html>`_  and `this <https://www.digitalocean.com/community/tutorials/how-to-install-and-manage-rabbitmq>`_. 




