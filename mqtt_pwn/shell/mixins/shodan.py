import shodan as shodan
from cmd2 import with_argparser, with_category
import argparse

from prettytable import PrettyTable

from mqtt_pwn.shell.base import BaseMixin
from mqtt_pwn.config import SHODAN_API_KEY
from mqtt_pwn.utils import shodan_key_required, export_table, import_shodan_table


class ShodanMixin(BaseMixin):
    """Shodan Mixin Class"""

    shodan_parser = argparse.ArgumentParser(
        description="Search through the Shodan.io API to gather info on available MQTT brokers.")

    shodan_parser.add_argument('-c', '--cached', action='store_true', help='Get the last results previously fetched')

    @with_category(BaseMixin.CMD_CAT_GENERAL)
    @with_argparser(shodan_parser)
    def do_shodan(self, args):
        """The Shodan function method"""

        self._handle_shodan(args)

    @shodan_key_required
    def _handle_shodan(self, args):
        if args.cached:
            self._handle_shodan_from_cache()
        else:
            self._handle_shodan_from_api()

    def _handle_shodan_from_cache(self):
        table = import_shodan_table()

        if not table:
            self.print_error('No cached Shodan data yet')
        else:
            self.print_info('Fetching Shodan data from cache...')
            self.ppaged(msg=table)

    def _handle_shodan_from_api(self):
        api = shodan.Shodan(SHODAN_API_KEY)
        table = PrettyTable(field_names=[
            'IP', 'Port', 'ASN', 'Version', 'Organization', 'Hostnames'
        ])

        table.align['ASN'] = "l"
        table.align['Organization'] = "l"
        table.align['Hostnames'] = "l"

        self.print_info('Fetching Shodan data...')

        for item in api.search_cursor('MQTT Connection Code: 0'):
            table.add_row([
                item.get('ip_str', '-'),
                item.get('port', 0),
                item.get('asn', '-'),
                item.get('version', '-'),
                item.get('org', '-'),
                ', '.join(item.get('hostnames', [])) or '-',
            ])

        self.ppaged(msg=str(table))
        export_table(table)

