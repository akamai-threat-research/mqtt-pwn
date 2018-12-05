from peewee import TextField, ForeignKeyField, DateTimeField, IntegerField, CharField

from mqtt_pwn import utils
from .base import BaseModel
from .topic import Topic
from .scan import Scan

BODY_LENGTH = 77


class Message(BaseModel):
    """A model that describes a MQTT message"""

    scan = ForeignKeyField(Scan, backref='message')
    topic = ForeignKeyField(Topic, backref='message')
    body = TextField()
    qos = IntegerField()
    label = CharField(default='')
    ts = DateTimeField(default=utils.now)

    @property
    def short_body(self):
        """Creates a shortened instance of the body"""

        return self.body if len(str(self.body)) < BODY_LENGTH else self.body[:BODY_LENGTH] + '...'

    def to_list(self):
        """Converts the instance to a list"""

        return [self.id, self.topic.name, self.short_body, self.topic.label]

    def to_dict(self):
        return {
            'id': self.id,
            'topic': self.topic.name,
            'message': self.short_body,
            'label': self.topic.label
        }

    def __repr__(self):
        """A proper representation of the class instance"""

        return f'Message [' \
               f'topic={self.topic}, ' \
               f'body={self.body}' \
               f'ts={self.ts}' \
               f'label={self.label}' \
               f']'
