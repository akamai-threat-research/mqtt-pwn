Sonoff Exploiter
================

Sonoff is a smart switch made for smart home automation. Sonoff devices connected to an MQTT broker can be manipulated
by publishing certain special crafted messages.

Flow
----

A sonoff device that is connected to our MQTT broker will subscribe to certain topics in order to get
commands from its operator. We can utilize this fact to send the same messages to those topics but from
our end.

When we publish the message to a certain topic, the sonoff device will execute that command and send the
results to the :code:`RESULT` topic (with the same prefix as the former topic).

Topics
------

We currently support 17 types of commands:

- FullTopic
- Hostname
- IPAddress1
- MqttClient
- MqttHost
- MqttPassword
- MqttUser
- Password
- Password2
- SSId
- SSId2
- WebConfig
- WebPassword
- WebServer
- WifiConfig
- otaU


Usage
-----

In order to execute this exploit, a special plugin was created. Let's examine the help strings:

.. code-block:: text

    >> sonoff --help
    usage: sonoff [-h] [-p PREFIX] [-t TIMEOUT]

    Sonoff devices tend to share certain information on demand. This module looks
    for those pieces of information actively.

    optional arguments:
      -h, --help            show this help message and exit
      -p PREFIX, --prefix PREFIX
                            the topic prefix of the sonoff device (default:
                            sonoff/)
      -t TIMEOUT, --timeout TIMEOUT
                            for how long to listen (default: 10)

First, we need to find out what is the topic prefix of our victim. We can achieve this by using the
:code:`topics` command. Once we have it, simply feed it to the :code:`sonoff` plugin and look for output.