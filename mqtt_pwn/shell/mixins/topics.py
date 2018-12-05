from cmd2 import with_argparser, with_category
import argparse
from prettytable import PrettyTable
from peewee import fn
from operator import iand
from functools import reduce

from mqtt_pwn.models.topic import Topic
from mqtt_pwn.models.message import Message
from mqtt_pwn.shell.base import BaseMixin
from mqtt_pwn.utils import scan_required, export_to_csv


class TopicsMixin(BaseMixin):
    """Topics Mixin Class"""

    topics_parser = argparse.ArgumentParser(description="List topics that were detected through discovery scans")
    topics_parser.add_argument('-e', '--export', help='export the search results', action="store_true")
    topics_parser.add_argument('-s', '--show-only-labeled',
                               help='show only labeled topics',
                               action="store_true")
    topics_parser.add_argument('-l', '--limit',
                               help='get the first X rows',
                               type=int)
    topics_parser.add_argument('-r', '--regex',
                               help='search for a pattern in the topic name')
    topics_parser.add_argument('-c', '--case-sensitive',
                               help='make the regex search case sensitive (default is case insensitive)',
                               action="store_true")

    @with_category(BaseMixin.CMD_CAT_BROKER_OP)
    @with_argparser(topics_parser)
    def do_topics(self, args):
        """The Topics function method"""

        self._handle_get_topics(args)

    @scan_required
    def _handle_get_topics(self, args):
        """Handles when a user selects the topics method"""

        if not self._validate_topics_parser_args(args):
            return

        topics = self._get_topics(args)

        if args.export:
            export_to_csv(headers=['id', 'topic', 'label'], data=[t.to_dict() for t in topics])
            self.print_info(f'Wrote {len(topics)} {"line" if len(topics) == 1 else "lines"} to "results.csv".')
        else:
            self._create_topics_table(topics)

    def _validate_topics_parser_args(self, args):
        """Checks whether the arguments are valid"""

        is_valid = True

        if args.regex:
            if '(?i)' in args.regex or '(i?)' in args.regex:
                self.print_error('Please refrain from using case modifiers in the regex, instead use "-c".')
                is_valid = False

        if args.limit:
            if args.limit < 0:
                self.print_error('Please select a limit greater than zero.')
                is_valid = False

        return is_valid

    def _get_topics(self, args):
        """Gets the topics from the database"""

        self.print_ok('Fetching data..')
        conditions = [Message.scan == self.current_scan]

        if args.show_only_labeled:
            conditions.append(Topic.not_empty_label())

        if args.regex:
            if args.case_sensitive:
                conditions.append(Topic.name.regexp(args.regex))
            else:
                conditions.append(fn.lower(Topic.name).regexp(args.regex))

        return self._generic_fetch_topics(
            reduce(iand, conditions),
            limit=args.limit
        )

    def _generic_fetch_topics(self, conditions, limit=None):
        """Fetches the topics from the database"""

        return Topic \
            .select() \
            .join(Message) \
            .distinct() \
            .where(conditions) \
            .limit(limit)

    def _create_topics_table(self, topics):
        """Creates a table for the topics to show to the user"""

        topics_table = PrettyTable(field_names=[
            'ID', 'Topic', 'Label'
        ])

        topics_table.align['Topic'] = "l"

        if not topics_table:
            self.print_info('No topics')
            return

        for topic in topics:
            topics_table.add_row(topic.to_list())

        self.ppaged(msg=str(topics_table))
