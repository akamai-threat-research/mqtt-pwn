from pathlib import Path
from paho.mqtt.client import Client, MQTT_ERR_SUCCESS
import time


class ConnectionResult(object):
    """Represents a connection result (success/fail)"""

    def __init__(self):
        self._return_code = None

    @property
    def did_succeed(self):
        """A property that contains data whether the connection has succeeded"""
        return self._return_code == MQTT_ERR_SUCCESS

    def set_return_code(self, return_code):
        """Sets the return code field"""
        self._return_code = return_code


class AuthBruteForce(object):
    """The class responsible from brute force a broker"""

    valid_criterias = ('usernames', 'passwords')

    def __init__(self, cli, host, port, usernames, passwords):
        self.cli = cli

        self.host = host
        self.port = port

        self.timeout = 2

        self.usernames = usernames
        self.passwords = passwords
        self._errors_found = False

    def _are_valid_credentials(self, username, password):
        """Checks whether credentials are valid"""

        def _on_connect(client, userdata, flags, rc):
            """A callback that matches the MQTT client signature, that triggers when connection was established"""
            userdata.set_return_code(rc)
            client.disconnect()

            client.loop_stop()
            client.should_stop = True

        con_result = ConnectionResult()
        client = Client(userdata=con_result)

        client.username_pw_set(username, password)
        client.on_connect = _on_connect

        start_time = time.time()
        client.should_stop = False
        client.connect_async(self.host, self.port)
        client.loop_start()

        while not client.should_stop and time.time() - start_time < self.timeout:
            time.sleep(0.001)

        return con_result.did_succeed

    def _brute(self):
        """Start the actual bruteforce effort"""

        for username in self._create_generator_for('usernames'):
            if self._errors_found:
                break

            for password in self._create_generator_for('passwords'):
                if self._are_valid_credentials(username, password):
                    self.cli.print_ok(f'Found valid credentials: {username}:{password}')

    def brute(self):
        """A wrapper for the _brute method, mainly to catch keyboard interrupts"""
        try:
            self._brute()
        except KeyboardInterrupt:
            self.cli.print_error('Brute force has stopped...', start='\n')

    def _validate_criteria(self, criteria):
        """Validates whether the criteria resides within the valid criteria list"""

        if criteria not in AuthBruteForce.valid_criterias:
            raise ValueError('Criteria not valid')

    def _create_generator_for(self, criteria):
        """Created a generator for a certain criteria, agnostic to whether its a file or a list"""

        self._validate_criteria(criteria)
        self_criteria = getattr(self, criteria)

        if isinstance(self_criteria, list):
            for item in self_criteria:
                yield item

        elif isinstance(self_criteria, str):
            path = Path(self_criteria)

            if path.exists() and path.is_file():
                with open(self_criteria, 'r') as f:
                    for line in f:
                        yield line.strip()
            else:
                self.cli.print_error(f'Path "{path}" does not exist!')
                self._errors_found = True


