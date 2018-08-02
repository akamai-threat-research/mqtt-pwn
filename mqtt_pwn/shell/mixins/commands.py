from cmd2 import with_argparser, with_category
import argparse

from prettytable import PrettyTable

from mqtt_pwn.models.command import Command
from mqtt_pwn.shell.base import BaseMixin
from mqtt_pwn.utils import victim_required


class CommandsMixin(BaseMixin):
    """Commands Mixin Class"""

    commands_parser = argparse.ArgumentParser(
        description='Show commands that were executed on the current victim',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    commands_parser.add_argument('-i', '--id', help='show only a specific command id')

    @with_category(BaseMixin.CMD_CAT_VICTIM_OP)
    @with_argparser(commands_parser)
    def do_commands(self, args):
        """The Commands function method"""

        if args.id:
            self._print_specific_command(args.id)
        else:
            self._print_commands()

    @victim_required
    def _print_commands(self):
        """Prints commands to the console"""

        commands_table = PrettyTable(field_names=[
            'ID', 'Command', 'Output', 'Time'
        ])

        commands_table.align['Command'] = "l"
        commands_table.align['Output'] = "l"

        commands = Command \
            .select() \
            .where(Command.victim == self.current_victim)

        for command in commands:
            commands_table.add_row(
                command.to_list()
            )

        self.poutput(str(commands_table))

    @victim_required
    def _print_specific_command(self, command_id):
        """Prints a specific command to the console"""

        cmd: Command = Command.get_by_id(command_id)

        if not cmd:
            self.print_error('Command does not exist!')
            return

        self.print_pairs(f'Command #{command_id}:', {
            'Timestamp': cmd.ts,
            'Command': cmd.command,
            'Output': cmd.normalized_output
        })
