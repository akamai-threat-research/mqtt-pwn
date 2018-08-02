from threading import Thread
import json
import re
from pathlib import Path

from mqtt_pwn.models.message import Message
from mqtt_pwn import config


class Definition(object):
    """A class that represents a match definition for labeling"""

    def __init__(self, definition_obj):
        """The class initializer"""

        self.pattern = re.compile(definition_obj.get('pattern'))
        self.label = definition_obj.get('label')

    def match(self, candidate):
        """Matches the class pattern to a candidate"""

        if self.pattern.search(candidate):
            return self.label

        return None


class PassiveParser(object):
    """Passive Parser that uses a definition file to label topics"""

    def __init__(self, definitions_path='definitions.json', scan_instance=None):
        """The class initializer"""

        self.scan_instance = scan_instance

        if not Path(definitions_path).exists():
            definitions_path = config.DEFINITIONS_PATH

        self.definitions_path = definitions_path

    def load_definitions(self):
        """Loads the definitions from file"""

        with open(self.definitions_path, 'r') as f:
            return json.load(f)

    def parse(self):
        """Parses the topics from database and match their definitions"""

        d = self.load_definitions()
        definitions = [Definition(definition) for definition in d]

        topics = [
            m.topic
            for m in
            Message.select(Message.topic).distinct().where(Message.scan == self.scan_instance)
        ]

        for t in topics:
            labels = []

            for definition in definitions:
                label = definition.match(t.name)

                if label:
                    labels.append(label)

            t.label = ', '.join(labels)
            t.save()

    @staticmethod
    def start(scan_instance):
        """Starts a scan """

        PassiveParser(
            scan_instance=scan_instance,
        ).parse()

    @staticmethod
    def start_async(scan_instance):
        """Starts a scan asynchronously"""

        Thread(target=PassiveParser.start, args=(scan_instance,)).start()

