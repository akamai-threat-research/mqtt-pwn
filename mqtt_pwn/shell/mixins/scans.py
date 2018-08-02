from cmd2 import with_argparser, with_category
import argparse
from prettytable import PrettyTable

from mqtt_pwn.models.scan import Scan
from mqtt_pwn.shell.base import BaseMixin


class ScansMixin(BaseMixin):
    """Scans Mixin Class"""

    scans_parser = argparse.ArgumentParser()
    scans_parser.add_argument('-i', '--id', help='select a specific scan by id')
    scans_parser.add_argument('-t', '--tail', action="store_true", help='show only the tail of the scans table')

    @with_category(BaseMixin.CMD_CAT_BROKER_OP)
    @with_argparser(scans_parser)
    def do_scans(self, args):
        """The Scans function method"""

        if args.id:
            self._select_scan(args.id)
        else:
            self._show_all_scans(args.tail)

    # noinspection PyUnresolvedReferences
    def _show_all_scans(self, tail):
        """Shows all scans in a table"""

        scans_table = PrettyTable(field_names=[
            'ID', 'Type', 'Created At', 'Is Done'
        ])

        if tail:
            scans = Scan.select().order_by(Scan.id.desc()).limit(5)[::-1]
        else:
            scans = Scan.select()

        for s in scans:
            scans_table.add_row(s.to_list())

        self.ppaged(msg=str(scans_table))

    # noinspection PyUnresolvedReferences
    def _select_scan(self, scan_id):
        """Selects a scan as the global context scan variable"""

        s = Scan.select().where(Scan.id == scan_id).first()

        if not s:
            self.print_error('Scan ID does not exist!')
            return

        if not s.is_done:
            self.print_error('Scan has not finished yet, please wait.')
            return

        self.current_scan = s
        self.update_prompt()

