from functools import reduce
from operator import iand

from cmd2 import with_argparser, with_category
import argparse
from prettytable import PrettyTable
from peewee import fn

from mqtt_pwn.models.topic import Topic
from mqtt_pwn.models.message import Message
from mqtt_pwn.models.scan import Scan
from mqtt_pwn.shell.base import BaseMixin
from mqtt_pwn.utils import scan_required, prettify_json, export_to_csv


class MessagesMixin(BaseMixin):
    """Messages Mixin Class"""

    messages_parser = argparse.ArgumentParser(description="List Messages that were detected through discovery scans")

    messages_parser.add_argument('-e', '--export', help='export the search results', action="store_true")

    single_message_group = messages_parser.add_argument_group(description="Single Message Arguments")
    multi_message_group = messages_parser.add_argument_group(description="Multi Message Arguments")

    single_message_group.add_argument('-i', '--index',
                                      help='show a message based on an ID',
                                      type=int)
    single_message_group.add_argument('-j', '--json-prettify',
                                      help='JSON prettify the message body',
                                      action="store_true")

    multi_message_group.add_argument('-s', '--show-only-labeled',
                                     help='show only labeled topics',
                                     action="store_true")
    multi_message_group.add_argument('-l', '--limit',
                                     help='get the first X rows',
                                     type=int)
    multi_message_group.add_argument('-mr', '--message-regex',
                                     help='search for a pattern in the message body')
    multi_message_group.add_argument('-tr', '--topic-regex',
                                     help='search for a pattern in the topic name')
    multi_message_group.add_argument('-c', '--case-sensitive',
                                     help='make the regex search case sensitive (default is case insensitive)',
                                     action="store_true")

    @with_category(BaseMixin.CMD_CAT_BROKER_OP)
    @with_argparser(messages_parser)
    def do_messages(self, args):
        """The Messages function method"""

        self._handle_get_messages(args)

    @scan_required
    def _handle_get_messages(self, args):
        """Handles when a user selected the messages method"""

        if not self._validate_messages_parser_args(args):
            return

        # First Group (Single Message)
        if args.index:
            self._show_specific_message(args.index, is_json_prettify=args.json_prettify, export=args.export)

        # Second Group (Multi Message)
        else:
            msgs = self._get_messages(args)
            self._create_messages_table(msgs, export=args.export)

    def _validate_messages_parser_args(self, args):
        """Checks whether the arguments passed are valid"""

        is_valid = True

        if (args.index or args.json_prettify) and \
                (args.show_only_labeled or args.limit or args.message_regex or args.topic_regex or args.case_sensitive):
            self.print_error('Please refrain from using flags from both groups.')
            is_valid = False

        for r in [args.message_regex, args.topic_regex]:
            if r and ('(?i)' in r or '(i?)' in r):
                self.print_error('Please refrain from using case modifiers in the regex, instead use "-c".')
                is_valid = False

        if args.limit:
            if args.limit < 0:
                self.print_error('Please select a limit greater than zero.')
                is_valid = False

        return is_valid

    def _get_messages(self, args):
        """Gets messages from the database"""

        self.print_ok('Fetching data..')
        conditions = [Message.scan == self.current_scan]

        if args.show_only_labeled:
            conditions.append(Topic.not_empty_label())

        if args.message_regex:
            if args.case_sensitive:
                conditions.append(Message.body.regexp(args.message_regex))
            else:
                conditions.append(fn.lower(Message.body).regexp(args.message_regex))

        if args.topic_regex:
            if args.case_sensitive:
                conditions.append(Topic.name.regexp(args.topic_regex))
            else:
                conditions.append(fn.lower(Topic.name).regexp(args.topic_regex))

        return self._generic_fetch_messages(
            reduce(iand, conditions),
            limit=args.limit
        )

    def _show_specific_message(self, index, is_json_prettify=False, export=False):
        """Shows a specific message to the client"""

        m = Message.get_by_id(index)
        body = prettify_json(m.body) if is_json_prettify else m.body
        data = {
            'Topic': m.topic.name,
            'Timestamp': m.ts,
            'Body': body
        }

        if export:
            export_to_csv(headers=['index', 'topic', 'timestamp', 'body'],
                          data=[
                              {
                                  'index': index,
                                  'topic': m.topic.name,
                                  'timestamp': m.ts,
                                  'body': body
                              }
                          ])
            self.print_info(f'Wrote 1 line to "results.csv".')
        else:
            self.print_pairs(f'Message #{index}:', data)

    # noinspection PyUnresolvedReferences
    def _generic_fetch_messages(self, conditions, limit=None):
        """Fetches messages from the database"""

        return Message \
            .select(Message.id, Topic.name, Message.body, Topic.label) \
            .join(Topic) \
            .distinct() \
            .where(conditions) \
            .limit(limit)

    def _create_messages_table(self, messages, export=False):
        """Creates the messages table """

        msgs = []
        msgs_table = PrettyTable(field_names=[
            'ID', 'Topic', 'Message', 'Label'
        ])

        msgs_table.align['Topic'] = "l"
        msgs_table.align['Message'] = "l"
        msgs_table.align['Label'] = "l"

        if not messages:
            self.print_info('No messages')
            return

        for msg in messages:
            msgs_table.add_row(msg.to_list())
            msgs.append(msg.to_dict())

        if export:
            export_to_csv(headers=['id', 'topic', 'message', 'label'], data=msgs)
            self.print_info(f'Wrote {len(msgs)} {"line" if len(msgs) == 1 else "lines"} to "results.csv".')
        else:
            self.ppaged(msg=str(msgs_table))
