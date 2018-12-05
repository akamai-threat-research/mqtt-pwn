from mqtt_pwn.shell.base import BaseCLI

from mqtt_pwn.shell.mixins.back import BackMixin
from mqtt_pwn.shell.mixins.bruteforce import BruteforceMixin
from mqtt_pwn.shell.mixins.commands import CommandsMixin
from mqtt_pwn.shell.mixins.connect import ConnectMixin
from mqtt_pwn.shell.mixins.discover import DiscoveryMixin
from mqtt_pwn.shell.mixins.messages import MessagesMixin
from mqtt_pwn.shell.mixins.shodan import ShodanMixin
from mqtt_pwn.shell.mixins.sonoff import SonoffMixin
from mqtt_pwn.shell.mixins.victims import VictimsMixin
from mqtt_pwn.shell.mixins.execute import ExecuteMixin
from mqtt_pwn.shell.mixins.scans import ScansMixin
from mqtt_pwn.shell.mixins.system_info import SystemInfoMixin
from mqtt_pwn.shell.mixins.topics import TopicsMixin
from mqtt_pwn.shell.mixins.owntracks import OwnTracksMixin


_mixins = [
    VictimsMixin,
    ExecuteMixin,
    CommandsMixin,
    ScansMixin,
    SystemInfoMixin,
    TopicsMixin,
    DiscoveryMixin,
    ConnectMixin,
    BackMixin,
    OwnTracksMixin,
    SonoffMixin,
    BruteforceMixin,
    MessagesMixin,
    ShodanMixin
]


class MqttPwnCLI(BaseCLI, *_mixins):
    """The Mqtt-Pwn Custom Command Line Interface that includes our mixins"""
