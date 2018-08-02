import os
from peewee import PostgresqlDatabase, SqliteDatabase, ProgrammingError

from mqtt_pwn.models import database_proxy
from mqtt_pwn.models.victim import Victim
from mqtt_pwn.models.command import Command
from mqtt_pwn.models.topic import Topic
from mqtt_pwn.models.message import Message
from mqtt_pwn.models.scan import Scan
from mqtt_pwn import config


_all_tables = [Victim, Command, Topic, Message, Scan]


def create_db_connection():
    """ Creates a database connection with the postgres db"""

    is_test_env = os.getenv('MQTT_PWN_TESTING_ENV')

    if is_test_env:
        db = SqliteDatabase(':memory:')
    else:
        db = PostgresqlDatabase(
            config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT
        )

    database_proxy.initialize(db)

    return db


def create_tables(db, tables):
    """ Creates the given tables """

    try:
        db.create_tables(tables)
    except ProgrammingError:
        pass


def create_all_tables(db):
    """ Creates all the tables """

    create_tables(db, _all_tables)


def truncate_all_tables(db):
    """ Truncates all database tables """

    db.drop_tables(_all_tables)
    create_tables(db, _all_tables)

