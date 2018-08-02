from cmd2 import with_argparser, with_category
import argparse

from mqtt_pwn.shell.base import BaseMixin
from mqtt_pwn.utils import connection_required
from mqtt_pwn.exploits.sonoff import SonoffExploit


class SonoffMixin(BaseMixin):
    """Sonoff Mixin Class"""

    sonoff_parser = argparse.ArgumentParser(
        description="Sonoff devices tend to share certain information on demand. This module looks for those pieces of"
                    " information actively.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    sonoff_parser.add_argument('-p', '--prefix', help='the topic prefix of the sonoff device', default='sonoff/')
    sonoff_parser.add_argument('-t', '--timeout', help='for how long to listen', default=10, type=int)

    @with_category(BaseMixin.CMD_CAT_BROKER_OP)
    @with_argparser(sonoff_parser)
    def do_sonoff(self, args):
        """The Sonoff function method"""

        self._sonoff(args.prefix, args.timeout)

    @connection_required
    def _sonoff(self, prefix, timeout):
        """Handles when a user selects the sonoff method"""

        self.print_info('Sonoff exploit running ...')
        SonoffExploit.run(prefix, timeout, self)
