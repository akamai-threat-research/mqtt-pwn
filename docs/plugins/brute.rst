Credentials Brute Force
=======================

`MQTT` protocol uses a centralized broker to communicate between entities (device, sensor, etc.). Those brokers can
define a basic authentication mechanism in the form of username / password pair. `MQTT-PWN` provides a credential
brute force module that with a given set of usernames and passwords tries to authenticate to the broker in order to
find valid credentials.

Wordlists
---------

In order to run the credentials brute force plugin, we are required to provide a set of usernames and passwords.
A default set is already provided in the `./resources/wordlists/*` directory, but external ones can be provided. Inline
usernames and passwords are also supported.

Usage
-----

To run the plugins, first make sure you are connected to broker (using the `connect` commands). Lets examine the help
strings for this plugins:

.. code-block:: bash

    localhost:1883 >> bruteforce --help
    usage: bruteforce [-h] [-u USERNAME [USERNAME ...] | -uf USERNAMES_FILE]
                      [-p PASSWORD [PASSWORD ...] | -pf PASSWORDS_FILE]

    Bruteforce credentials of the connected MQTT broker

    optional arguments:
      -h, --help            show this help message and exit
      -u USERNAME [USERNAME ...], --username USERNAME [USERNAME ...]
                            the username to probe the broker with (can be more
                            than one, separated with spaces) (default: None)
      -uf USERNAMES_FILE, --usernames-file USERNAMES_FILE
                            use a usernames file instead (usernames separated with
                            a newline) (default:
                            /mqtt_pwn/resources/wordlists/usernames.txt)
      -p PASSWORD [PASSWORD ...], --password PASSWORD [PASSWORD ...]
                            the password to probe the broker with (can be more
                            than one, separated with spaces) (default: None)
      -pf PASSWORDS_FILE, --passwords-file PASSWORDS_FILE
                            use a password file instead (passwords separated with
                            a newline) (default:
                            /mqtt_pwn/resources/wordlists/passwords.txt)

As we can see, it is possible to provide usernames / passwords file or inline list. Once provided, simply hit enter
and the bruteforce will start. If stopping is desired, simply hit `Ctrl-C`:

.. code-block:: shell

    localhost:1883 >> bruteforce
    [+] Starting brute force!
    [+] Found valid credentials: root:123456
    [+] Found valid credentials: root:password
    [+] Found valid credentials: root:12345678
    [+] Found valid credentials: root:1234
    ^C
    [-] Brute force has stopped...
