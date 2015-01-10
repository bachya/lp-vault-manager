# encoding: utf-8

from __future__ import unicode_literals
from argparser import ArgParser, ArgParserError
from workflow import Workflow

import re
import subprocess
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

    # COMMAND: Login
    if ap.command == 'login':
        log.debug('Executing command: login')
        util.login_to_lastpass()
        util.print_utf8('Hit ENTER to login to LastPass.')
        sys.exit(0)

    # COMMAND: Open URL
    elif ap.command == 'open-url':
        if ap.arg:
            log.debug('Executing command: open-url')
            subprocess.call(['open', ap.arg])
            util.print_utf8('Enjoy the repository and join in!')
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
