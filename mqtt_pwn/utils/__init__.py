import json
from base64 import b64encode, b64decode
from datetime import datetime
from blessings import Terminal
from threading import Thread
import os
import csv

from pygments import highlight, lexers, formatters
from mqtt_pwn.config import SHODAN_API_KEY
from prettytable import PrettyTable


t: Terminal = Terminal()


def banner():
    """The banner we want to display"""

    return t.bright_blue("""
    ╔╦╗╔═╗╔╦╗╔╦╗  ╔═╗┬ ┬╔╗╔
    ║║║║═╬╗║  ║───╠═╝│││║║║
    ╩ ╩╚═╝╚╩  ╩   ╩  └┴┘╝╚╝
    """) + f"""
        {t.underline_bright_cyan("by @Akamai")}
    """


def encode(data):
    """Encodes a message"""
    return b64encode(json.dumps(data).encode())


def decode(data):
    """Decodes a message"""
    return json.loads(b64decode(data).decode())


def now():
    """Returns the current time in iso format"""
    return datetime.now().isoformat()


def get_prompt(cli):
    """Handles the prompt line with colors"""
    client = cli.mqtt_client
    end_prompt = t.bold_cyan(">> ")
    parts = []

    if client:
        client_part = t.magenta(client.host) + ':' + t.yellow(str(client.port))
        parts.append(client_part)

    if cli.current_victim:
        victim_part = t.cyan_underline(f"[Victim #{cli.current_victim.id}]")
        parts.append(victim_part)

    if cli.current_scan:
        scan_part = t.cyan_underline(f"[Scan #{cli.current_scan.id}]")
        parts.append(scan_part)

    not_empty_parts = [p for p in parts if p]

    if len(not_empty_parts) == 0:
        return end_prompt

    return ' '.join(not_empty_parts) + ' ' + end_prompt


def new_victim_notification(cli):
    """Notifies the user when a new victim has registered"""
    def _print_threaded():
        cli.print_ok(t.bold_underline_blue('<< New victim has registered! >>'), end='', start='\n')

    Thread(target=_print_threaded).start()


def victim_required(func):
    """A decorator that enforces a CLI instance mixin function to select a victim first"""
    def _victim_required(*args, **kwargs):
        self = args[0]

        if not self.current_victim:
            self.print_error('Please select a victim first!')
            return

        return func(*args, **kwargs)

    return _victim_required


def connection_required(func):
    """A decorator that enforces a CLI instance mixin function to connect first"""
    def _connection_required(*args, **kwargs):
        self = args[0]

        if not self.mqtt_client:
            self.print_error('Please create a connection first!')
            return

        return func(*args, **kwargs)

    return _connection_required


def scan_required(func):
    """A decorator that enforces a CLI instance mixin function to select a scan first"""

    def _scan_required(*args, **kwargs):
        self = args[0]

        if not self.current_scan:
            self.print_error('Please select a scan first!')
            return

        return func(*args, **kwargs)

    return _scan_required


def shodan_key_required(func):
    """A decorator that enforces the Shodan API key to exist"""

    def _shodan_key_required(*args, **kwargs):
        self = args[0]

        if not SHODAN_API_KEY:
            self.print_error(f'Shodan API key missing! Please fill in in the config file.')
        else:
            return func(*args, **kwargs)
    return _shodan_key_required


def drop_none(lst):
    return [x for x in lst if x]


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# noinspection PyBroadException,PyUnresolvedReferences
def prettify_json(some_text):
    try:
        return highlight(
            json.dumps(json.loads(some_text), indent=4),
            lexers.JsonLexer(),
            formatters.TerminalFormatter())
    except:
        return some_text


def export_to_csv(headers, data, filename='results.csv'):
    with open(filename, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)

        writer.writeheader()
        writer.writerows(data)


def export_table(table: PrettyTable):
    with open('shodan.txt', 'w') as f:
        f.write(table.get_string())


def import_shodan_table():
    try:
        with open('shodan.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None
