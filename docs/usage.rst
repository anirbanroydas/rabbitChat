Usage
=====
There are two types of Usage. One using rabbitChat as a binary by installaing from pip and running the application in  the local machine directly. Another method is running the application from Docker. Hence another set of usage steps for the Docker use case.


[Docker Method] 
----------------

After having installed the above dependencies, and ran the **Optional** (If not using any CI Server) or **Required** (If using any CI Server) **CI Setup** Step, then just run the following commands to use it:


You can run and test the app in your local development machine or you can run and test directly in a remote machine. You can also run and test in a production environment. 



[Docker Method] Run
--------------------

The below commands will start everythin in development environment. To start in a production environment, suffix ``-prod`` to every **make** command.

For example, if the normal command is ``make start``, then for production environment, use ``make start-prod``. Do this modification to each command you want to run in production environment. 

**Exceptions:** You cannot use the above method for test commands, test commands are same for every environment. Also the  ``make system-prune`` command is standalone with no production specific variation (Remains same in all environments).

* **Start Applcation**
  ::

      $ make clean
      $ make build
      $ make start

      # OR

      $ docker-compose up -d


    
  
* **Stop Application**
  ::

      $ make stop

      # OR

      $ docker-compose stop


* **Remove and Clean Application**
  ::

      $ make clean

      # OR

      $ docker-compose rm --force -v
      $ echo "y" | docker system prune


* **Clean System**
  ::

      $ make system-prune

      # OR

      $ echo "y" | docker system prune






[Docker Method] Logging
------------------------


* To check the whole application Logs
  ::

      $ make check-logs

      # OR

      $ docker-compose logs --follow --tail=10



* To check just the python app\'s logs
  ::

      $ make check-logs-app

      # OR

      $ docker-compose logs --follow --tail=10 identidock




[Standalone Binary Method] Run
--------------------------------

After having installed rabbitChat via pip, just the run the following commands to use it:

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




