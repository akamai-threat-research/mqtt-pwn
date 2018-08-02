from peewee import CharField, DateTimeField, BooleanField

from mqtt_pwn import utils
from .base import BaseModel


class Scan(BaseModel):
    """A model the describes a scan"""

    type_of_scan = CharField(default='topic_discovery')
    ts = DateTimeField(default=utils.now)
    is_done = BooleanField(default=False)

    # noinspection PyUnresolvedReferences
    def to_list(self):
        """Formats the current instance to a list"""

        return [
            self.id,
            self.type_of_scan,
            self.ts,
            self.is_done
        ]

    def __repr__(self):
        """A proper representation of the class instance"""

        return f'Scan [' \
               f'type_of_scan={self.type_of_scan}' \
               f'ts={self.ts}' \
               f'is_done={self.is_done}' \
               f']'
