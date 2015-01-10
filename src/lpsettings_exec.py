# encoding: utf-8

from __future__ import unicode_literals
from argparser import ArgParser, ArgParserError
from utilities import BROWSER_CHROME, BROWSER_SAFARI
from workflow import Workflow

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
        log.debug('Parsed command: {}'.format(ap.command))
        log.debug('Parsed argument: {}'.format(ap.arg))
        log.debug('Parsed delimiter: {}'.format(ap.delimiter))
    except ArgParserError, e:
        log.error('Argument parsing failed: {}'.format(e))
        sys.exit(1)

    # COMMAND: Edit Config
    if ap.command == 'edit-config':
        log.debug('Executing command: edit-config')
        util.edit_config_file()
        util.print_utf8('Have at it, power user.')
        sys.exit(0)

    # COMMAND: Login
    elif ap.command == 'login':
        log.debug('Executing command: login')
        util.login_to_lastpass()
        util.print_utf8('Hit ENTER to login to LastPass.')
        sys.exit(0)

    # COMMAND: Logout
    elif ap.command == 'logout':
        log.debug('Executing command: logout')
        util.logout_from_lastpass()
        util.print_utf8('LastPass logout successful.')
        sys.exit(0)

    # COMMAND: Open URL
    elif ap.command == 'open-url':
        if ap.arg:
            log.debug('Executing command: open-url')
            subprocess.call(['open', ap.arg])
            util.print_utf8('Enjoy the repository and join in!')
        sys.exit(0)

    # COMMAND: Set Avoid Ambiguous
    elif ap.command == 'set-avoid-ambiguous':
        if ap.arg:
            value = util.str2bool(ap.arg)
            log.debug('Executing command: set-use-ambiguous')
            util.set_config_value('passwords', 'avoid_ambiguous', value)
            util.print_utf8('Setting ambiguous use to "{}".'.format(ap.arg))

    # COMMAND: Set Browser
    elif ap.command == 'set-browser':
        if ap.arg:
            log.debug('Executing command: set-browser')
            util.set_config_value('general', 'browser', ap.arg)

            arg = int(ap.arg)
            if arg == BROWSER_CHROME:
                browser = 'Chrome'
            elif arg == BROWSER_SAFARI:
                browser = 'Safari'
            util.print_utf8('Setting default browser to {}.'.format(browser))
        sys.exit(0)

    # COMMAND: Set lpass Path
    elif ap.command == 'set-lpass-path':
        if ap.arg:
            log.debug('Executing command: set-lpass-path')
            util.set_config_value('lastpass', 'path', ap.arg)
            util.print_utf8('Setting path to "{}".'.format(ap.arg))

    # COMMAND: Set Password Length
    elif ap.command == 'set-password-length':
        if ap.arg:
            log.debug('Executing command: set-password-length')
            util.set_config_value('passwords', 'length', ap.arg)
            util.print_utf8('Setting length to {} characters.'.format(ap.arg))

    # COMMAND: Set Password Number
    elif ap.command == 'set-password-number':
        if ap.arg:
            log.debug('Executing command: set-password-number')
            util.set_config_value('passwords', 'number', ap.arg)
            util.print_utf8('Setting number to {} passwords.'.format(ap.arg))

    # COMMAND: Set Timeout
    elif ap.command == 'set-timeout':
        if ap.arg:
            log.debug('Executing command: set-timeout')
            util.set_config_value('general', 'cache_bust', ap.arg)
            util.print_utf8('Setting timeout to {} seconds.'.format(ap.arg))

    # COMMAND: Set Use Digits
    elif ap.command == 'set-use-digits':
        if ap.arg:
            value = util.str2bool(ap.arg)
            log.debug('Executing command: set-use-digits')
            util.set_config_value('passwords', 'use_digits', value)
            util.print_utf8('Setting digit use to "{}".'.format(ap.arg))

    # COMMAND: Set Use Lowercase
    elif ap.command == 'set-use-lowercase':
        if ap.arg:
            value = util.str2bool(ap.arg)
            log.debug('Executing command: set-lpass-lowercase')
            util.set_config_value('passwords', 'use_lowercase', value)
            util.print_utf8('Setting lowercase use to "{}".'.format(ap.arg))

    # COMMAND: Set Use Symbols
    elif ap.command == 'set-use-symbols':
        if ap.arg:
            value = util.str2bool(ap.arg)
            log.debug('Executing command: set-use-symbols')
            util.set_config_value('passwords', 'use_symbols', value)
            util.print_utf8('Setting symbol use to "{}".'.format(ap.arg))

    # COMMAND: Set Use Uppercase
    elif ap.command == 'set-use-uppercase':
        if ap.arg:
            value = util.str2bool(ap.arg)
            log.debug('Executing command: set-lpass-uppercase')
            util.set_config_value('passwords', 'use_uppercase', value)
            util.print_utf8('Setting uppercase use to "{}".'.format(ap.arg))

    # COMMAND: Set Username
    elif ap.command == 'set-username':
        if ap.arg:
            log.debug('Executing command: set-username')
            util.set_config_value('lastpass', 'username', ap.arg)
            util.print_utf8('Setting username to "{}".'.format(ap.arg))
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
