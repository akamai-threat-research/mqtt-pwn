Introduction
============

`MQTT-PWN` intends to be a one-stop-shop for IoT Broker penetration-testing and security assessment operations,
as it combines enumeration, supportive functions and exploitation modules while packing it all within
command-line-interface with an easy-to-use and extensible shell-like environment.


Prerequisites
-------------

Generally speaking, `MQTT-PWN` relies on 2 main components:

- Python 3.X environment
- A database backend (`PostgreSQL <https://www.postgresql.org/>`_)

The framework can be instantiated using docker or directly on the host.


Installation
------------

In order to install `MQTT-PWN` simply clone or download the `repository <https://github.com/akamai-threat-research/mqtt-pwn>`_
and follow your preferred deployment method:

- Directly on host
- Using Docker (skip to :ref:`docker_usage`)


Database
--------

In order for the application to work properly, a `PostgreSQL` database is required. After configuring it correctly,
follow the next section to install the virtual environment, on the first run of the application, it will create
automatically all required tables.


Virtual Environment
-------------------

As a ground rule, I recommend using virtual environments using the `pyenv <https://github.com/pyenv/pyenv>`_.
Make sure you have a working installation of `pyenv` before proceeding, once you have it, first create a virtual
environment using:

.. code-block:: shell

    daniel@lab ~/mqtt_pwn ⇒ pyenv virtualenv mqtt_pwn_env

Now, install the requirements python packages using pip:

.. code-block:: shell

    daniel@lab ~/mqtt_pwn ⇒ pip install -r requirements.txt

We now have a fully operational virtual environment containing all required packages. To run the application, simply type:

.. code-block:: shell

    daniel@lab ~/mqtt_pwn ⇒ python run.py

    ╔╦╗╔═╗╔╦╗╔╦╗  ╔═╗┬ ┬╔╗╔
    ║║║║═╬╗║  ║───╠═╝│││║║║
    ╩ ╩╚═╝╚╩  ╩   ╩  └┴┘╝╚╝

        by @Akamai

    >>




.. _docker_usage:

Docker Usage
------------

Sometimes installing a database or a specific python environment on the host machine can be somewhat cumbersome.
In order to ease the usage of this tool, we provided a dockerized version of the tool so it can be easily installed and deployed.
Make sure you have installed `Docker <https://www.docker.com/>`_ and `Docker-Compose <https://docs.docker.com/compose/>`_ first.

We are using `Docker Compose <https://docs.docker.com/compose/>`_ to instantiate a 2 containers (`db`, `cli`) and a network so they can interact with each other.
First, let's create and build those containers/network:

.. code-block:: shell

    daniel@lab ~/mqtt_pwn ⇒ docker-compose up --build --detach

This will build and create our containers in detached mode, meaning they will run in the background.
Let's confirm they are indeed running:

.. code-block:: shell

    daniel@lab ~/mqtt_pwn ⇒ docker-compose ps

                Name                           Command               State             Ports
    -------------------------------------------------------------------------------------------------
    359a8bd33718_mqtt_pwn_db_1      docker-entrypoint.sh postgres   Up         0.0.0.0:5431->5432/tcp
    mqtt_pwn_v2_cli_1               python /mqtt_pwn/run.py         Exit 255

As we can see the `postgres` instance is up and running, while our `cli` is down. That's perfectly fine, since need it running
only when needed.

Now, let's test if the `cli` works:

.. code-block:: shell

    daniel@lab ~/mqtt_pwn ⇒ docker-compose run cli

    ╔╦╗╔═╗╔╦╗╔╦╗  ╔═╗┬ ┬╔╗╔
    ║║║║═╬╗║  ║───╠═╝│││║║║
    ╩ ╩╚═╝╚╩  ╩   ╩  └┴┘╝╚╝

        by @Akamai

    >>

If you are seeing what is described above, were good to go!


Resource Script
---------------

Usually, some options tend to be needed from the start of the application, therefor this application support a global
resources script that gets executed every time the application starts. The script is located under
`./resources/shell_startup.rc`. The format of the script is as follows:

- Every line contains a command, such as `connect -p 1883` etc.
- A line can be commented when it starts with a `#`.
