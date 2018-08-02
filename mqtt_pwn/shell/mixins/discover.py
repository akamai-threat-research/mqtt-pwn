from cmd2 import with_argparser, with_category
import argparse

from mqtt_pwn.connection.active_scanner import ActiveScanner
from mqtt_pwn.models.scan import Scan
from mqtt_pwn.shell.base import BaseMixin
from mqtt_pwn.utils import connection_required

DEFAULT_TOPICS = ['$SYS/#', '#']


class DiscoveryMixin(BaseMixin):
    """Discovery Mixin Class"""

    discover_parser = argparse.ArgumentParser(
        description="Discover new topics/messages in the current connected broker",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    discover_parser.add_argument('-t', '--timeout', help='for how long to discover', default=60)
    discover_parser.add_argument('-p', '--topics', help='which topics to listen to', default=DEFAULT_TOPICS, nargs='+')
    discover_parser.add_argument('-q', '--qos', help='which quality of service', default=0, type=int)

    @with_category(BaseMixin.CMD_CAT_BROKER_OP)
    @with_argparser(discover_parser)
    def do_discovery(self, args):
        """The Discovery function method"""

        self._start_discovery(args.timeout, args.topics, args.qos)

    @connection_required
    def _start_discovery(self, timeout, topics, qos):
        """Starts a discovery scan"""

        s = Scan.create()

        topics = [
            (topic_name, qos)
            for topic_name in topics
        ]

        self.print_info(f"Starting MQTT discovery (id #{s.id}) ...")
        ActiveScanner.start_async(self, s, timeout, topics)
