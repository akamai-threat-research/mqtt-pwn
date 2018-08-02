from cmd2 import with_argparser, with_category
import argparse

from mqtt_pwn.shell.base import BaseMixin
from mqtt_pwn.exploits.owntracks import OwnTracksExploit
from mqtt_pwn.utils import scan_required


class OwnTracksMixin(BaseMixin):
    """OwnTracks Mixin Class"""

    owntracks_parser = argparse.ArgumentParser(
        description="Owntracks shares publicly their users coordinates. "
                    "Simply discover some topics, choose that scan and pick"
                    " a user+device to look for.")
    owntracks_parser.add_argument('-u', '--user', help='user to find owntracks coordinates')
    owntracks_parser.add_argument('-d', '--device', help='device to find owntracks coordinates')

    @with_category(BaseMixin.CMD_CAT_BROKER_OP)
    @with_argparser(owntracks_parser)
    def do_owntracks(self, args):
        """The Owntracks function method"""

        if args.user and args.device:
            self._owntracks_single(args.user, args.device)
        else:
            self._owntracks_table()

    @scan_required
    def _owntracks_single(self, user, device):
        """Handles getting a single owntracks URL"""

        ote = OwnTracksExploit(self.current_scan.id)
        url = ote.google_maps_url(user, device)

        self.print_ok('Google Maps Url: ' + url)

    @scan_required
    def _owntracks_table(self):
        """Handles getting a multiple owntracks URLs"""

        ote = OwnTracksExploit(self.current_scan.id)
        t = ote.create_urls_table()

        self.poutput(t)

