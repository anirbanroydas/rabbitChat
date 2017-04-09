CI Setup
=========


If you are using the project in a CI setup (like travis, jenkins), then, on every push to github, you can set up your travis build or jenkins pipeline. Travis will use the ``.travis.yml`` file and Jenknis will use the ``Jenkinsfile`` to do their jobs. Now, in case you are using Travis, then run the Travis specific setup commands and for Jenkins run the Jenkins specific setup commands first. You can also use both to compare between there performance.

The setup keys read the values from a ``.env`` file which has all the environment variables exported. But you will notice an example ``env`` file and not a ``.env`` file. Make sure to copy the ``env`` file to ``.env`` and **change/modify** the actual variables with your real values.

The ``.env`` files are not commited to git since they are mentioned in the ``.gitignore`` file to prevent any leakage of confidential data.

After you run the setup commands, you will be presented with a number of secure keys. Copy those to your config files before proceeding.

**NOTE:** This is a one time setup.
**NOTE:** Check the setup scripts inside the ``scripts/`` directory to understand what are the environment variables whose encrypted keys are provided.
**NOTE:** Don't forget to **Copy** the secure keys to your ``.travis.yml`` or ``Jenkinsfile``

**NOTE:** If you don't want to do the copy of ``env`` to ``.env`` file and change the variable values in ``.env`` with your real values then you can just edit the ``travis-setup.sh`` or ``jenknis-setup.sh`` script and update the values their directly. The scripts are in the ``scripts/`` project level directory.


**IMPORTANT:** You have to run the ``travis-setup.sh`` script or the ``jenkins-setup.sh`` script in your local machine before deploying to remote server.




 

Travis Setup
~~~~~~~~~~~~~~~~~

These steps will encrypt your environment variables to secure your confidential data like api keys, docker based keys, deploy specific keys.
::

  $ make travis-setup



Jenkins Setup
~~~~~~~~~~~~~~~~~~~

These steps will encrypt your environment variables to secure your confidential data like api keys, docker based keys, deploy specific keys.
::

  $ make jenkins-setup
