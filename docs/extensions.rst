Extensions
==========

`MQTT-PWN` was built with extendability as its one of its major key points. Therefor, new plugins are encouraged to be
developed.

The Mixin Notion
----------------

The CLI main class, which holds within all logic of the command loop, is built on top of a class inheritance notion
called `Mixin`. Basically, we create a class inheritance chain where every class that we inherit from adds more
functionalities to our command loop.

First, we start with our main mixin, which holds all the main logic such as the command prompt format, etc. Then,
as we can see from the code sample below, we create a class called :code:`MqttPwnCLI` which inherits from
:code:`BaseClI` (which is an empty class) and a list of mixins:

.. code-block:: python
    :linenos:

    _mixins = [
        VictimsMixin,
        ExecuteMixin,
        CommandsMixin,
        ScansMixin,
        SystemInfoMixin,
        TopicsMixin,
        DiscoveryMixin,
        ConnectMixin,
        BackMixin,
        OwnTracksMixin,
        SonoffMixin,
        BruteforceMixin,
        MessagesMixin
    ]


    class MqttPwnCLI(BaseCLI, *_mixins):
        """The Mqtt-Pwn Custom Command Line Interface that includes our mixins"""

The list of mixins define all the functionalities we want our command loop to have.


Adding New Plugin
-----------------

In order to create a new plugin, we need to create a new `Mixin`. We'll get familiar with the structure of the `Mixin`.
Let's take for example the `bruteforce` plugin:

.. code-block:: python
    :linenos:

    class BruteforceMixin(BaseMixin):
        """Bruteforce Mixin Class"""

        bt_parser = argparse.ArgumentParser(
            description='Bruteforce credentials of the connected MQTT broker',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        user_group = bt_parser.add_mutually_exclusive_group()
        pass_group = bt_parser.add_mutually_exclusive_group()

        user_group.add_argument('-u', '--username',
                                help='the username to probe the broker with (can be more than one, separated with spaces)',
                                nargs='+')

        user_group.add_argument('-uf', '--usernames-file',
                                help='use a usernames file instead (usernames separated with a newline)',
                                default=config.DEFAULT_USERNAME_LIST)

        pass_group.add_argument('-p', '--password',
                                help='the password to probe the broker with (can be more than one, separated with spaces)',
                                nargs='+')

        pass_group.add_argument('-pf', '--passwords-file',
                                help='use a password file instead (passwords separated with a newline)',
                                default=config.DEFAULT_PASSWORD_LIST)

        @with_category(BaseMixin.CMD_CAT_BROKER_OP)
        @with_argparser(bt_parser)
        def do_bruteforce(self, args):
            """The Bruteforce function method"""

            username = args.username if args.username else args.usernames_file
            password = args.password if args.password else args.passwords_file

            self._start_brute_force(username, password)

        @connection_required
        def _start_brute_force(self, username, password):
            """Handles when a user selects the back method"""

            self.print_ok('Starting brute force!')
            AuthBruteForce(self, username, password).brute()

Let's break it down to three main components:

Class Name
~~~~~~~~~~

The class name has to be in the form of `PluginName` + `Mixin`. Then, it must inherit from :code:`BaseMixin`, so we
would have a similar interface to all the mixins, from the example above:

.. code-block:: python
    :emphasize-lines: 1
    :linenos:

    class BruteforceMixin(BaseMixin):
        """Bruteforce Mixin Class"""

Argument Parser
~~~~~~~~~~~~~~~

In order for the plugin to handle arguments, we use argument parser from :code:`argparse`. Since we are harnessing the
power of the `Cmd2` library, we can use this argument parser to catch arguments directly from our plugin, in example for
the `bruteforce` plugin:

.. code-block:: python
    :emphasize-lines: 1
    :linenos:

        bt_parser = argparse.ArgumentParser(
            description='Bruteforce credentials of the connected MQTT broker',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        user_group = bt_parser.add_mutually_exclusive_group()
        pass_group = bt_parser.add_mutually_exclusive_group()

        user_group.add_argument('-u', '--username',
                                help='the username to probe the broker with (can be more than one, separated with spaces)',
                                nargs='+')
        ...

We declare a static field called :code:`bt_parser` that holds all the argument parsing logic behind our plugin.

"Do" Function
~~~~~~~~~~~~~

In order to register as a command, we have to declare a class function that starts with :code:`do_`:

.. code-block:: python
    :emphasize-lines: 3
    :linenos:

        @with_category(BaseMixin.CMD_CAT_BROKER_OP)
        @with_argparser(bt_parser)
        def do_bruteforce(self, args):
            """The Bruteforce function method"""
        ...

We decorate the function with the :code:`with_argparser` decorator to couple our function with its argument parser.
Notice, that the function receives one argument which are the parsed arguments from our parser.

Useful Decorators
~~~~~~~~~~~~~~~~~

Besides the :code:`with_argparser` (which we got from the `Cmd2` library), we have some useful decorators to enforce
some global context variables such as:

- :code:`connection_required` to enforce having a connection first
- :code:`victim_required` to enforce choosing a victim first
- :code:`scan_required` to enforce selecting a scan from the list first

Simply decorate the function you desire with them to activate the enforcement. All of them are defined in the
`mqtt_pwn/utils` folder.
