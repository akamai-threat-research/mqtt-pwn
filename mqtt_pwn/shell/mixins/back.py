from cmd2 import with_argparser, with_category
import argparse

from mqtt_pwn.shell.base import BaseMixin


class BackMixin(BaseMixin):
    """Back Mixin Class"""

    back_parser = argparse.ArgumentParser(
        description="Deselect a variable like current_victim or current_scan...",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    back_parser.add_argument('variable', choices=BaseMixin.variables_choices)

    @with_category(BaseMixin.CMD_CAT_GENERAL)
    @with_argparser(back_parser)
    def do_back(self, args):
        """The Back function method"""
        self._back(args.variable)

    def _back(self, variable):
        """Handles when a user selects the back method"""
        if variable == 'scan':
            self.current_scan = None

        if variable == 'victim':
            self.current_victim = None

        self.update_prompt()
