from cmd2 import with_argparser, with_category
import argparse

from mqtt_pwn.shell.base import BaseMixin
from mqtt_pwn.connection.mqtt_client import MqttClient
from mqtt_pwn.utils import connection_required
from mqtt_pwn.config import DEFAULT_BROKER_HOST, DEFAULT_BROKER_PORT, DEFAULT_BROKER_USERNAME, DEFAULT_BROKER_PASSWORD


class ConnectMixin(BaseMixin):
    """Connect Mixin Class"""

    disconnect_parser = argparse.ArgumentParser(
        description='Disconnect from an MQTT broker',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    connect_parser = argparse.ArgumentParser(
        description='Connect to an MQTT broker',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    connect_parser.add_argument('-o', '--host', help='host to connect to', default=DEFAULT_BROKER_HOST)
    connect_parser.add_argument('-p', '--port', help='port to use', type=int, default=DEFAULT_BROKER_PORT)
    connect_parser.add_argument('-t', '--timeout', help='connection timeout', type=int, default=60)

    connection_parser = connect_parser.add_subparsers(help='Connection type command', dest='connect_type')
    userpass_parser = connection_parser.add_parser('USERPASS')
    userpass_parser.add_argument('-u', '--username', help='username to authenticate with', default=DEFAULT_BROKER_USERNAME)
    userpass_parser.add_argument('-w', '--password', help='password to authenticate with', default=DEFAULT_BROKER_PASSWORD)
    clientcert_parser = connection_parser.add_parser('CLIENTCERT')
    clientcert_parser.add_argument('--ca-cert', help='path to server CA certificate')
    clientcert_parser.add_argument('--crt', help='path to client certificate')
    clientcert_parser.add_argument('--pkey', help='path to client private key file')
    

    @with_category(BaseMixin.CMD_CAT_BROKER_OP)
    @with_argparser(connect_parser)
    def do_connect(self, args):
        """The Connect function method"""

        self._connect(args)

    @with_category(BaseMixin.CMD_CAT_BROKER_OP)
    @with_argparser(disconnect_parser)
    @connection_required
    def do_disconnect(self, args):
        """ Disconnected a client """

        self.mqtt_client.stop()
        self.mqtt_client = None
        self.update_prompt()

    def _connect(self, args):
        """Handles when a user selects the connect method"""

        if self.mqtt_client is not None:
            self.do_disconnect(None)

        self.print_info('Connecting...')

        try:

            if args.connect_type == 'USERPASS':
                self.mqtt_client = MqttClient.from_user_password(
                    host=args.host,
                    port=args.port,
                    timeout=args.timeout,
                    username=args.username,
                    password=args.password,
                    cli=self
                )
            elif  args.connect_type == 'CLIENTCERT':
                self.mqtt_client = MqttClient.from_client_cert(
                    host=args.host,
                    port=args.port,
                    timeout=args.timeout,
                    ca_cert=args.ca_cert,
                    client_cert=args.crt,
                    client_private_key=args.pkey,
                    cli=self
                )

            self.mqtt_client.run()
        except KeyboardInterrupt:
            self.print_error('Connection interrupted!', start='\n')
            self.do_disconnect(None)
