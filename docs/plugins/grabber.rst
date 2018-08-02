Information Grabber
===================

The MQTT brokers (specifically `mosquitto <https://mosquitto.org/>`_), tend to send some metadata about the broker itself, the clients connected
and more.


Broker Status
-------------

The information (metadata) we grab from the broker can be grabbed through a successful subscription to certain special
topics. Those topics are located within the `$SYS` hierarchy. There are quite a lot of them, but we mainly focus on
9 important topics.

To see the broker information, first create a successful connection using the :code:`connect` command, then use the
:code:`system_info` command as follows:

.. code-block:: shell

    localhost:1883 >> system_info
    +--------------+--------------------------+
    | Property     | Value                    |
    +--------------+--------------------------+
    | timestamp    | 2018-04-11 06:55:09-0400 |
    | uptime       | 699152 seconds           |
    | maximum      | 228887                   |
    | count        | 582668                   |
    | disconnected | 225697                   |
    | total        | 228882                   |
    | connected    | 3185                     |
    | version      | mosquitto version 1.4.15 |
    +--------------+--------------------------+


Selected Topics
---------------

The topics we are focusing our plugin on are the following (the description was taken directly from the `mosquitto`
documentation):

$SYS/broker/version
~~~~~~~~~~~~~~~~~~~
The version of the broker

$SYS/broker/timestamp
~~~~~~~~~~~~~~~~~~~~~
The timestamp at which this particular build of the broker was made.

$SYS/broker/uptime
~~~~~~~~~~~~~~~~~~
The amount of time in seconds the broker has been online.

$SYS/broker/subscriptions/count
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The total number of subscriptions active on the broker.

$SYS/broker/clients/connected
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The number of currently connected clients.

$SYS/broker/clients/expired
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The number of disconnected persistent clients that have been expired and removed through the persistent_client_expiration option.

$SYS/broker/clients/disconnected
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The total number of persistent clients (with clean session disabled) that are registered at the broker but are currently disconnected.

$SYS/broker/clients/maximum
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The maximum number of clients that have been connected to the broker at the same time.

$SYS/broker/clients/total
~~~~~~~~~~~~~~~~~~~~~~~~~
The total number of active and inactive clients currently connected and registered on the broker.
