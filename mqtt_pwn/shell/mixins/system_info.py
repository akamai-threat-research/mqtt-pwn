from cmd2 import with_argparser, with_category
import argparse

from mqtt_pwn.shell.base import BaseMixin
from mqtt_pwn.utils import connection_required


class SystemInfoMixin(BaseMixin):
    """Scans Mixin Class"""

    system_info_parser = argparse.ArgumentParser()

    @with_category(BaseMixin.CMD_CAT_BROKER_OP)
    @with_argparser(system_info_parser)
    def do_system_info(self, _):
        """The System Information function method"""

        self._print_system_info()

    @connection_required
    def _print_system_info(self):
        """Handles when a user selects the system info method"""

        self.poutput(self.mqtt_client.system_info.to_table())
