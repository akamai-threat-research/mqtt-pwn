Enumeration
===========

The `MQTT` protocol allows by design to every entity (device, sensor etc.) to subscribe to any topic it wishes (as long
the broker hasn't enabled any security measures, which by default are off). Using this method, we developed what we
called - the :code:`discovery` plugin, which subscribes for a certain amount of time, to all topics (using wildcard
notation) by that enumerating all available topics at a certain time.

Wildcard Topic
--------------

`MQTT` supports subscribing to topics using 2 wildcard options:

Single Level
~~~~~~~~~~~~
A single level wildcard replaces one topic level using the :code:`+` sign, in example:

.. code-block:: text

    home/daniel/+/open

This means that every topic matching the pattern above will match, in example considering the following topics:

- home/daniel/door/status
- home/daniel/lights/status
- home/daniel/garage/status

All of them are going to match.


Multi Level
~~~~~~~~~~~

In contrast to the single level wildcard, the multi level comes handy when we don't now the tail of the topic, and we
want to wildcard more than one level, it is used with the :code:`#` sign. In example:

.. code-block:: text

    home/daniel/#

This means every topic from this level and below will match, considering the topics bellow:

- home/daniel/door/status
- home/daniel/door/opened
- home/daniel/lights/status
- home/daniel/lights/closed
- home/daniel/garage/status
- home/daniel/garage/closed

All of them are going to match.


Discover
--------

In order to enumerate topics, first make sure you are connected to a MQTT broker (using the :code:`connect` command).
Let's examine the :code:`discovery` command:

.. code-block:: text

    localhost:1883 >> discovery --help
    usage: discovery [-h] [-t TIMEOUT] [-p TOPICS [TOPICS ...]] [-q QOS]

    Discover new topics/messages in the current connected broker

    optional arguments:
      -h, --help            show this help message and exit
      -t TIMEOUT, --timeout TIMEOUT
                            for how long to discover (default: 60)
      -p TOPICS [TOPICS ...], --topics TOPICS [TOPICS ...]
                            which topics to listen to (default: ['$SYS/#', '#'])
      -q QOS, --qos QOS     which quality of service (default: 0)


Now, let's run the discovery for 10 seconds with quality of service of 0:

.. code-block:: text

    localhost:1883 >> discovery -t 10 -q 0
    [!] Starting MQTT discovery (id #1) ...
    localhost:1883 >>
    localhost:1883 >>
    [+] Scan #1 has finished!

We can observe that the scan is asynchronous (runs on a different thread), so are free to handle more operations in
the meanwhile. We can see the status of scans using the :code:`scans` command:

.. code-block:: text

    localhost:1883 >> scans
    +----+-----------------+----------------------------+---------+
    | ID |       Type      |         Created At         | Is Done |
    +----+-----------------+----------------------------+---------+
    | 1  | topic_discovery | 2018-07-19 15:10:07.988613 |   True  |
    +----+-----------------+----------------------------+---------+

We see that the can is finished, in order to see which topics/messages we have enumerated, we need to select it first.
This can be done using the :code:`scans` command as well:

.. code-block:: text

    localhost:1883 >> scans -i 1
    localhost:1883 [Scan #1] >>

The scan has been chosen and added as a global context variables, meaning that choosing scan number `1` will affect
the output of further plugins now.


Topics
------

To explore which topics we have enumerated, make sure we have selected a scan (explained in the last section). Then,
simply use the :code:`topics` command:

.. code-block:: text

    localhost:1883 [Scan #1] >> topics
    [+] Fetching data..
    +-------+-------------------------------------------+----------+
    |   ID  | Topic                                     |   Label  |
    +-------+-------------------------------------------+----------+
    |  2609 | some/topic/we_caught                      |          |
    |   5   | $SYS/broker/clients/maximum               |          |
    |  2427 | some/other/topic/we_caught                |          |

    ....

The list goes on and one, similarly to the output of a `more` command. However, the plugin supports many useful flags,
let's examine the help strings:

.. code-block:: text

    localhost:1883 [Scan #1] >> topics --help
    usage: topics [-h] [-s] [-l LIMIT] [-r REGEX] [-c]

    List topics that were detected through discovery scans

    optional arguments:
      -h, --help            show this help message and exit
      -s, --show-only-labeled
                            show only labeled topics
      -l LIMIT, --limit LIMIT
                            get the first X rows
      -r REGEX, --regex REGEX
                            search for a pattern in the topic name
      -c, --case-sensitive  make the regex search case sensitive (default is case
                            insensitive)


First of all, we see a flag called `--show-only-labeled`, we have came up with a list of known topic patterns (the list
can be found in `./resources/definitions.json`. It contains the topic pattern and a friendly name. Turning this flag,
shows only topics that we have found in the `definitions.json` file.

Furthermore, we can limit the results and search for a specific regular expression pattern withing the topic name.


Messages
--------

Aside from topics enumeration, `MQTT-PWN` supports also message enumeration, as part of the `discovery` the scan also
stores the messages body. They can be viewed, similarly to the `topics` plugin, using the :code:`messages` plugin:

.. code-block:: text

    localhost:1883 [Scan #1] >> messages
    [+] Fetching data..
    +-------+----------------------------+------------------+-----------+
    |   ID  | Topic                      | Message          | Label     |
    +-------+----------------------------+------------------+-----------+
    | 2096  | some/topic/we_caught       | hello world      |           |

    ...

It has similar flags as the `topics` plugin:

.. code-block:: text

    localhost:1883 [Scan #1] >> messages --help
    usage: messages [-h] [-i INDEX] [-j] [-s] [-l LIMIT] [-mr MESSAGE_REGEX]
                    [-tr TOPIC_REGEX] [-c]

    List Messages that were detected through discovery scans

    optional arguments:
      -h, --help            show this help message and exit

      Single Message Arguments

      -i INDEX, --index INDEX
                            show a message based on an ID
      -j, --json-prettify   JSON prettify the message body

      Multi Message Arguments

      -s, --show-only-labeled
                            show only labeled topics
      -l LIMIT, --limit LIMIT
                            get the first X rows
      -mr MESSAGE_REGEX, --message-regex MESSAGE_REGEX
                            search for a pattern in the message body
      -tr TOPIC_REGEX, --topic-regex TOPIC_REGEX
                            search for a pattern in the topic name
      -c, --case-sensitive  make the regex search case sensitive (default is case
                            insensitive)

There are a couple of differences, the first one is that we have two operational modes here;

Multi
~~~~~

Similarly to the :code:`topics` plugin, we can set a limit to the messages and look for regular expressions patterns (either
in the topic name or the message body), along with setting the search case sensitive or not. Because the message body
can be extremely long, they are pruned after a certain amount of characters.


Single
~~~~~~

Using the :code:`-i` flag, we can select a single message, by that showing the full length of the body, along of a special
flag :code:`-j` that enables JSON formatting, in example:

.. code-block:: text

    localhost:1883 [Scan #1] >> messages -i 27607 -j
    Message #27607:
     - Topic: owntracks/daniel/iPhone7
     - Timestamp: 2018-07-25 13:18:33.237445
     - Body: {
        "_type": "location",
        "tid": "n5",
        "acc": 17,
        "batt": 56,
        "conn": "w",
        "lat": 32.1657401,
        "lon": 34.8116074,
        "t": "c",
        "tst": 1532513147
    }