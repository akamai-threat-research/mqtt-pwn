from paho.mqtt import client as mqtt
from threading import Thread
from time import time, sleep

from mqtt_pwn.config import DEFAULT_BROKER_HOST, DEFAULT_BROKER_PORT, DEFAULT_BROKER_USERNAME, DEFAULT_BROKER_PASSWORD
from mqtt_pwn.models.topic import Topic
from mqtt_pwn.models.message import Message
from mqtt_pwn.parsers.passive_parser import PassiveParser


class ActiveScanner(object):
    def __init__(self, client_id=None, host=DEFAULT_BROKER_HOST, port=DEFAULT_BROKER_PORT, timeout=60, topics=None,
                 listen_timeout=60, scan_instance=None, cli=None):
        """Active Scanner object initiation"""

        self._mqtt_client = mqtt.Client(client_id)
        self.cli = cli

        if cli:
            self.host = cli.mqtt_client.host
            self.port = cli.mqtt_client.port
        else:
            self.host = host
            self.port = port

        self.timeout = timeout
        self.topics = topics
        self.listen_timeout = int(listen_timeout)
        self.scan_instance = scan_instance

        self._base_topic = '$SYS/test123'
        self._mqtt_client.on_message = self.mqtt_on_message

    def mqtt_on_message(self, mqtt_client, obj, msg):
        """Handles when a new message arrives"""

        body = msg.payload.decode("utf-8", "ignore").encode('ascii', errors='replace').replace(b'\x00', b'')
        t, _ = Topic.get_or_create(name=msg._topic.decode('utf-8', 'replace'))

        Message.create(
            topic=t,
            scan=self.scan_instance,
            body=body,
            qos=msg.qos
        )

    def run(self):
        """The Scanner driver function"""

        if self.cli.mqtt_client.username and self.cli.mqtt_client.password:
            self._mqtt_client.username_pw_set(self.cli.mqtt_client.username, self.cli.mqtt_client.password)
            
        self._mqtt_client.connect(self.host, self.port, self.timeout)
        self._mqtt_client.subscribe(self.topics)

        Thread(target=self.check_for_timeout).start()

        self._mqtt_client.loop_start()

    def check_for_timeout(self):
        """Checks if we should stop the loop based on `self.listen_timeout`"""

        start_time = time()

        while True:
            if time() > start_time + self.listen_timeout:
                self._mqtt_client.loop_stop()

                PassiveParser.start(scan_instance=self.scan_instance)

                self.scan_instance.is_done = True
                self.scan_instance.save()
                break

            sleep(0.5)

        self.cli.print_ok(f'Scan #{self.scan_instance.id} has finished!', start='\n', end='')

    @staticmethod
    def start(cli, scan_instance, listen_timeout, topics):
        """Start A specific active scan - topic discovery"""
        ActiveScanner(
            cli=cli,
            scan_instance=scan_instance,
            topics=topics,
            listen_timeout=listen_timeout
        ).run()

    @staticmethod
    def start_async(cli, scan_instance, listen_timeout, topics):
        """Starts an active scan asynchronously"""
        Thread(target=ActiveScanner.start, args=(cli, scan_instance, listen_timeout, topics)).start()
