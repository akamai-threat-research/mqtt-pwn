from peewee import CharField, DateTimeField

from mqtt_pwn import utils
from .base import BaseModel


class Victim(BaseModel):
    """A model that describes a victim"""

    uuid = CharField(unique=True)
    os = CharField()
    hostname = CharField()
    first_seen = DateTimeField()
    last_seen = DateTimeField(default=utils.now)

    @classmethod
    def create_from_dict(cls, d):
        """Created a new instance from a dict"""

        v = cls.create(
            uuid=d.get('uuid'),
            os=d.get('os'),
            hostname=d.get('hostname'),
            first_seen=d.get('ts')
        )

        return v

    # noinspection PyUnresolvedReferences
    def to_list(self):
        """Formats the current instance to a list"""

        return [
            self.id,
            self.uuid,
            self.os,
            self.hostname,
            self.first_seen,
            self.last_seen
        ]

    def __repr__(self):
        """A proper representation of the class instance"""

        return f'Victim [' \
               f'uuid={self.uuid}, ' \
               f'os={self.os}, ' \
               f'hostname={self.hostname}' \
               f'first_seen={self.first_seen}, ' \
               f'last_seen={self.first_seen}' \
               f']'
