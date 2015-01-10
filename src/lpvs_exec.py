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


def copy_value_and_notify(value, success_msg, error_msg):
    """
    Copies a value to the clipboard and, if successful, outputs a success
    message for Alfred to use; otherwise, outputs an error message for Alfred
    to use.
    """
    log.debug('Outputting value to clipboard: {}'.format(value))
    if value:
        util.copy_value_to_clipboard(value)
        util.print_utf8(success_msg)
    else:
        util.print_utf8(error_msg)
    return


def copy_lp_field_and_notify(hostname, field_name):
    log.debug('Getting "{}" field from "{}"...'.format(field_name, hostname))
    value = util.get_value_from_field(hostname, field_name)
    sm = 'Copied {} for "{}" to clipboard.'.format(field_name, hostname)
    em = 'Unable to copy {} for "{}".'.format(field_name, hostname)
    copy_value_and_notify(value, sm, em)
    return


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

    # COMMAND: Get Password
    if ap.command == 'get-password':
        if ap.arg:
            log.debug('Executing command: get-password')
            copy_lp_field_and_notify(ap.arg.split('***')[0], 'password')
        sys.exit(0)

    # COMMAND: Get Raw Value
    elif ap.command == 'get-raw-value':
        if ap.arg:
            log.debug('Executing command: get-raw-value')
            args = ap.arg.split('***')
            sm = 'Copied "{}" for "{}" to clipboard.'.format(args[0], args[2])
            em = 'Unable to copy "{}" for "{}".'.format(args[0], args[2])
            copy_value_and_notify(args[1], sm, em)

    # COMMAND: Get Username
    elif ap.command == 'get-username':
        if ap.arg:
            log.debug('Executing command: get-username')
            copy_lp_field_and_notify(ap.arg.split('***')[0], 'username')
        sys.exit(0)

    # COMMAND: Login
    elif ap.command == 'login':
        log.debug('Executing command: login')
        util.login_to_lastpass()
        util.print_utf8('Hit ENTER to login to LastPass.')
        sys.exit(0)

    # COMMAND: Open URL
    elif ap.command == 'open-url':
        if ap.arg:
            log.debug('Executing command: open-url')
            url = ap.arg.split('***')[1]
            subprocess.call(['open', url])
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
