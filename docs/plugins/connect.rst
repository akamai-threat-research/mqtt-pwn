Connect to a Broker
===================

Most of the plugins in `MQTT-PWN` are dependant on a live connection to a MQTT broker. In order to create such
successful connection, the :code:`connect` function comes to the rescue.

Connect
-------

Let's examine the help strings of the command:

.. code-block:: shell

    >> connect --help
    usage: connect [-h] [-o HOST] [-p PORT] [-t TIMEOUT]

    Connect to an MQTT broker

    optional arguments:
      -h, --help            show this help message and exit
      -o HOST, --host HOST  host to connect to (default: m2m.eclipse.org)
      -p PORT, --port PORT  port to use (default: 1883)
      -t TIMEOUT, --timeout TIMEOUT
                            connection timeout (default: 60)

All we need is a live MQTT broker and the port it is using, and we are good to go! Let's try to connect with the
default parameters:

.. code-block:: shell

    >> connect
    [!] Connecting...
    >>
    m2m.eclipse.org:1883 >>

We have successfully connected to the MQTT broker. The connection details such the host and port are preprended to the
command prompt for ease of use.


Disconnect
----------

If we wish to close the connection, simply use the :code:`disconnect`
command:

.. code-block:: shell

    m2m.eclipse.org:1883 >> disconnect
    >>