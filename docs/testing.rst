Testing
========

**NOTE:** Testing is only done using the Docker Method. anyway, it should not matter whether you run your application using the Docker Method or the Standalone Method. Testing is independent of it.

Now, testing is the main deal of the project. You can test in many ways, namely, using ``make`` commands as mentioned in the below commands, which automates everything and you don't have to know anything else, like what test library or framework is being used, how the tests are happening, either directly or via ``docker`` containers, or may be different virtual environments using ``tox``. Nothing is required to be known.

On the other hand if you want fine control over the tests, then you can run them directly, either by using ``pytest`` commands, or via ``tox`` commands to run them in different python environments or by using ``docker-compose`` commands to run differetn tests. 

But running the make commands is lawasy the go to strategy and reccomended approach for this project.

**NOTE:** Tox can be used directly, where ``docker`` containers will not be used. Although we can try to run ``tox`` inside our test contianers that we are using for running the tests using the ``make`` commands, but then we would have to change the ``Dockerfile`` and install all the ``python`` dependencies like ``python2.7``, ``python3.x`` and then run ``tox`` commands from inside the ``docker`` containers which then run the ``pytest`` commands which we run now to perform our tests inside the current test containers. 

**CAVEAT:** The only caveat of using the make commands directly and not using ``tox`` is we are only testing the project in a single ``python`` environment, nameley ``python 3.6``.



* To Test everything
  ::

      $ make test


  Any Other method without using make will involve writing a lot of commands. So use the make command preferrably


* To perform Unit Tests
  ::

      $ make test-unit


* To perform Component Tests
  ::

      $ make test-component


* To perform Contract Tests
  ::

      $ make test-contract


* To perform Integration Tests
  ::

      $ make test-integration


* To perform End To End (e2e) or System or UI Acceptance or Functional Tests
  ::

      $ make test-e2e

      # OR

      $ make test-system

      # OR  

      $ make test-ui-acceptance

      # OR

      $ make test-functional


