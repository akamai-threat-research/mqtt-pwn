from peewee import DateTimeField, ForeignKeyField, TextField
from mqtt_pwn import utils

from .base import BaseModel
from .victim import Victim

MAX_LINE_SIZE = 77
MAX_LINES = 2


class Command(BaseModel):
    """A model that describes a command"""

    victim = ForeignKeyField(Victim, backref='output')
    command = TextField()
    output = TextField(default='')
    ts = DateTimeField(default=utils.now)

    def to_payload_format(self):
        """Formats the current instance to fit the message scheme"""

        return {
            'command': self.command,
            'command_id': self.id
        }

    def to_list(self):
        """Formats the current instance to a list"""

        return [
            self.id,
            str(self.command).strip(),
            self.short_output.strip(),
            self.ts
        ]

    @property
    def normalized_output(self):
        out = str(self.output)

        return out if (
            out.count('\n') == 1 and out[-1] == '\n'
        ) else '\n' + out

    @property
    def short_output(self):
        def shorten_line(line):
            return line if (
                len(line) < MAX_LINE_SIZE
            ) else line[:MAX_LINE_SIZE] + '...'

        out = str(self.output).strip()
        parts = [
            shorten_line(part)
            for part in out.split('\n')
            if part
        ]

        return '\n'.join(parts[:MAX_LINES]) if (
            len(parts) <= MAX_LINES
         ) else '\n'.join(parts[:MAX_LINES]) + '\n <redacted...>'

    def __repr__(self):
        """A proper representation of the class instance"""

        return 'Command [' \
               f'victim={self.victim.id}, ' \
               f'command={self.command}, ' \
               f'output={self.output}, ' \
               f'ts={self.ts}' \
               ']'
