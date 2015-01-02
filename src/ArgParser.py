# encoding: utf-8

from __future__ import unicode_literals
from workflow import Workflow

import re


class ArgParser:
    DEFAULT_DELIMITER = '>'
    PIECES_REGEX = r'(.+\.py)\s([^\s]+)(?:\s?{}?\s?(.+))?'

    def __init__(self, query, delimiter=DEFAULT_DELIMITER):
        """
        Initialize an ArgParser instance and split out the passed query into
        its component parts.
        """
        # Store a Workflow instance:
        self.wf = Workflow()

        try:
            # Parse the query into its component pieces and save them:
            matches = re.match(self.PIECES_REGEX.format(delimiter), query)
            self.script = matches.group(1)
            self.command = matches.group(2)
            self.argument = matches.group(3)
            self.query = re.sub(r'{}\s?'.format(self.script), '', query)
            self.delimiter = delimiter

            # Output all the properties we just set to the debug log:
            self.wf.logger.debug('Regex successfully matched.')
            self.debug_properties()
        except AttributeError, e:
            self.wf.logger.error('No regex match: ' + query)
            self.wf.logger.debug(e)

    def debug_properties(self):
        """
        Dump out the properties of this class instance.
        """
        self.wf.logger.debug('Query: ' + self.query)
        self.wf.logger.debug('Script: ' + self.script)
        self.wf.logger.debug('Command: ' + self.command)
        self.wf.logger.debug('Argument: ' + self.argument)
        self.wf.logger.debug('Delimiter: ' + self.delimiter)

    def import_script(self):
        """
        Attempt to import the script referenced in the query (stripped of its
        ".py" extension, of course).
        """
        module_name = self.script[:-3]
        try:
            __import__(module_name)
            self.wf.logger.debug('Imported module: ' + module_name)
        except ImportError:
            self.wf.logger.error('Unable to import module: ' + module_name)

ap = ArgParser('lpvm.py password-number > 10')
ap.import_script()
