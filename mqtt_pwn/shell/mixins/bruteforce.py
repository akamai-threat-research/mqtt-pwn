from cmd2 import with_argparser, with_category
import argparse

from mqtt_pwn.config import DEFAULT_BROKER_HOST, DEFAULT_BROKER_PORT
from mqtt_pwn.shell.base import BaseMixin
from mqtt_pwn.connection.brute_forcer import AuthBruteForce
from mqtt_pwn import config


class BruteforceMixin(BaseMixin):
    """Bruteforce Mixin Class"""

    bt_parser = argparse.ArgumentParser(
        description='Bruteforce credentials of the connected MQTT broker',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    user_group = bt_parser.add_mutually_exclusive_group()
    pass_group = bt_parser.add_mutually_exclusive_group()

    bt_parser.add_argument('--host', help='host to connect to', default=DEFAULT_BROKER_HOST)
    bt_parser.add_argument('--port', help='port to use', type=int, default=DEFAULT_BROKER_PORT)

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

        self._start_brute_force(args.host, args.port, username, password)

    def _start_brute_force(self, host, port, username, password):
        """Handles when a user selects the back method"""

        self.print_info('Starting brute force!')
        AuthBruteForce(self, host, port, username, password).brute()
