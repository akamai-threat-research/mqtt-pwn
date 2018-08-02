from cmd2 import with_argparser, with_category
import argparse
from prettytable import PrettyTable

from mqtt_pwn.models.victim import Victim
from mqtt_pwn.shell.base import BaseMixin


class VictimsMixin(BaseMixin):
    """Victims Mixin Class"""

    victims_parser = argparse.ArgumentParser()
    victims_parser.add_argument('-i', '--id', help='select a specific victim by id')

    @with_category(BaseMixin.CMD_CAT_VICTIM_OP)
    @with_argparser(victims_parser)
    def do_victims(self, args):
        """The Victims function method"""

        if args.id:
            self._select_victim(args.id)
        else:
            self._show_all_victims()

    # noinspection PyUnresolvedReferences
    def _select_victim(self, victim_id):
        """Selected a victim as the global context current_victim variable"""

        v = Victim.select().where(Victim.id == victim_id).first()

        if not v:
            self.print_error('Victim ID does not exist!')
            return

        self.current_victim = v
        self.update_prompt()

    def _show_all_victims(self):
        """Show all victims in a table"""

        victims_table = PrettyTable(field_names=[
            'ID', 'UUID', 'OS', 'Hostname', 'First Seen', 'Last Seen'
        ])

        for victim in Victim.select():
            victims_table.add_row(victim.to_list())

        self.poutput(str(victims_table))