from prettytable import PrettyTable


class SystemInfo(object):
    """Represents System Info of the broker"""

    topics = {
        ('$SYS/broker/version', 0),
        ('$SYS/broker/timestamp', 0),
        ('$SYS/broker/uptime', 0),
        ('$SYS/broker/subscriptions/count', 0),
        ('$SYS/broker/clients/connected', 0),
        ('$SYS/broker/clients/expired', 0),
        ('$SYS/broker/clients/disconnected', 0),
        ('$SYS/broker/clients/maximum', 0),
        ('$SYS/broker/clients/total', 0)
    }

    def __init__(self):
        """The class initializer"""
        self.data = {}

    @property
    def topic_list(self):
        """A property that contains only the topic names"""
        return [t[0] for t in SystemInfo.topics]

    def update(self, topic, payload):
        """Updates the system info data dict accordingly"""
        self.data[topic.split('/')[-1]] = payload.decode()

    def to_table(self):
        """Converts the data property to a `prettytable` table"""

        table = PrettyTable(field_names=['Property', 'Value'])

        table.align['Property'] = 'l'
        table.align['Value'] = 'l'

        for key, value in self.data.items():
            table.add_row([key, value])

        return table
