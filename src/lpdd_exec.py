# encoding: utf-8

from __future__ import unicode_literals
from argparser import ArgParser, ArgParserError
from workflow import Workflow

import re
import sys
import utilities

####################################################################
# Globals
####################################################################
log = None
util = None


def main(wf):
    """
    The main function, which executes the program. You know. :)
    """
    log.debug('Exec arguments: {}'.format(wf.args))

    # Parse the query into a command into a query:
    try:
        ap = ArgParser(wf.args)

        # Since 'get-password' is the default command that comes in, it's
        # possible that the argument will be prefixed with that string. If so,
        # we remove it here so that we have a clean argument.
        if ap.arg and ap.arg.startswith('get-password'):
            ap.arg = re.sub('get-password ', '', ap.arg)

        log.debug('Parsed command: {}'.format(ap.command))
        log.debug('Parsed argument: {}'.format(ap.arg))
        log.debug('Parsed delimiter: {}'.format(ap.delimiter))
    except ArgParserError, e:
        log.error('Argument parsing failed: {}'.format(e))
        sys.exit(1)

    # COMMAND: Download Data
    if ap.command == 'download-data':
        log.debug('Executing command: download-data')
        data = util.download_data()
        if data:
            wf.cache_data('vault_items', data)
            util.print_utf8('LastPass metadata successfully downloaded.')
        else:
            util.print_utf8('LastPass metadata download failed.')
        sys.exit(0)
    else:
        log.error('Unknown command: {}'.format(ap.command))

if __name__ == '__main__':
    # Configure a Workflow class and a logger:
    wf = Workflow()
    log = wf.logger

    # Configure a LpvmUtilities class:
    util = utilities.LpvmUtilities(wf)

    # Run!
    sys.exit(wf.run(main))
