Usage
=====

After having installed rabbitChat, just the run the following commands to use it:

RabbitMQ Server
----------------

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
           
          
rabbitChat Server
------------------------

1. Start Server
   ::          
        
        $ rabbitChat [options]
        
2. Options    
   
   :--port: Port number where the chat server will start
   
   * **Example**
     :: 
             
             $ rabbitChat --port=9191
             
             
3. Stop rabbitChat Server
   
   Click ``Ctrl+C`` to stop the server.



