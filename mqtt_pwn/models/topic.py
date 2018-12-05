from peewee import CharField

from .base import BaseModel


class Topic(BaseModel):
    """A model that describes a MQTT topic"""

    name = CharField(max_length=1024, unique=True)
    label = CharField(max_length=1024, default='')

    # noinspection PyUnresolvedReferences
    def to_list(self):
        """Formats the current instance to a list"""

        return [self.id, self.name, self.label]

    @staticmethod
    def not_empty_label():
        """Returns whether the label is not empty"""

        return Topic.label != '' or Topic.label is not None

    def to_dict(self):
        return {
            'id': self.id,
            'topic': self.name,
            'label': self.label
        }

    def __repr__(self):
        """A proper representation of the class instance"""

        return f'Topic [' \
               f'id={self.id}, ' \
               f'name={self.name}, ' \
               f'label={self.label}' \
               f']'
