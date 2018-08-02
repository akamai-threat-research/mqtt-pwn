from peewee import Model
from . import database_proxy


class BaseModel(Model):
    """The base model class"""

    class Meta:
        # We use a proxy object so we can initialize it later
        database = database_proxy
