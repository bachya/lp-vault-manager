# encoding: utf-8

from __future__ import unicode_literals
from argparser import ArgParser, ArgParserError
from utilities import BROWSER_CHROME, BROWSER_SAFARI
from workflow import Workflow

import sys
import utilities

####################################################################
# Miscellaneous
####################################################################
DEFAULT_COMMAND = 'list-settings'

####################################################################
# Globals
####################################################################
log = None
util = None


def main(wf):
    """
    The main function, which executes the program. You know. :)
    """
    log.debug('Query arguments: {}'.format(wf.args))

    # Parse the query into a command into a query:
    try:
        ap = ArgParser(wf.args)
    except ArgParserError:
        ap = ArgParser([DEFAULT_COMMAND])

    log.debug('Parsed command: {}'.format(ap.command))
    log.debug('Parsed argument: {}'.format(ap.arg))
    log.debug('Parsed delimiter: {}'.format(ap.delimiter))

    # COMMAND: List Settings
    if ap.command == 'list-browsers':
        wf.add_item('Google Chrome',
                    'Hit ENTER to use Google Chrome.',
                    valid=True,
                    arg='set-browser {!s}'.format(BROWSER_CHROME),
                    icon='icons/chrome.png')
        wf.add_item('Safari',
                    'Hit ENTER to use Safari.',
                    valid=True,
                    arg='set-browser {!s}'.format(BROWSER_SAFARI),
                    icon='icons/safari.png')

        wf.send_feedback()
        sys.exit(0)

    # COMMAND: List LastPass Settings
    elif ap.command == 'list-lp-settings':
        if wf.settings['lastpass']['username'] == '':
            wf.add_item('No LastPass username in settings!',
                        'Hit ENTER to add one.',
                        autocomplete='username {} '.format(ap.delimiter),
                        icon='icons/warning.png')
        else:
            wf.add_item('Login To LastPass',
                        'You will enter your master password in Terminal.',
                        valid=True,
                        arg='lastpass-login',
                        icon='icons/login.png')
            wf.add_item('Logout From LastPass',
                        'You will need to log in again before continuing!',
                        valid=True,
                        arg='lastpass-logout',
                        icon='icons/logout.png')
            wf.add_item('Set LastPass Username',
                        'Enter your LastPass username or email address.',
                        autocomplete='username {} '.format(ap.delimiter),
                        icon='icons/user.png')
            wf.add_item('Set Cache Timeout',
                        'Enter the number of seconds to keep the cache.',
                        autocomplete='cache {} '.format(ap.delimiter),
                        icon='icons/clock.png')
            wf.add_item('Set `lpass` Filepath',
                        'Enter the absolute path to `lpass`.',
                        autocomplete='lpass-path {} '.format(ap.delimiter),
                        icon='icons/filepath.png')

        wf.send_feedback()
        sys.exit(0)

    # COMMAND: List Password Settings
    elif ap.command == 'list-password-settings':
        wf.add_item('Set Number of Passwords',
                    'Enter the number of passwords that `lppg` creates.',
                    autocomplete='password-number {} '.format(ap.delimiter),
                    icon='icons/password-number.png')
        wf.add_item('Set Password Length',
                    'Enter the length of a generated password.',
                    autocomplete='password-length {} '.format(ap.delimiter),
                    icon='icons/password-length.png')

        wf.send_feedback()

    # COMMAND: List Settings
    elif ap.command == 'list-settings':
        wf.add_item('Set Default Browser',
                    'Set the browser used by `lpbrowser`.',
                    autocomplete='list-browsers',
                    icon='icons/browser.png')
        wf.add_item('Modify LastPass Settings',
                    'Username, cache settings, etc.',
                    autocomplete='list-lp-settings',
                    icon='icons/lastpass.png')
        wf.add_item('Modify Password Settings',
                    'Number of passwords, password length, etc.',
                    autocomplete='list-password-settings',
                    icon='icons/password.png')
        wf.add_item('Edit Config File',
                    'Manually edit the config JSON.',
                    valid=True,
                    arg='edit-config',
                    icon='icons/pencil.png')
        wf.add_item('View Repository',
                    'Open GitHub repository in your browser.',
                    valid=True,
                    arg='open-url https://github.com/bachya/lp-vault-manager',
                    icon='icons/github.png')

        wf.send_feedback()
        sys.exit(0)
    else:
        log.error('Unknown command: {}'.format(ap.command))
        sys.exit(1)


if __name__ == '__main__':
    # Configure a Workflow class and a logger:
    wf = Workflow(libraries=['./lib'])
    log = wf.logger

    # Configure a LpvmUtilities class:
    util = utilities.LpvmUtilities(wf)

    # Run!
    sys.exit(wf.run(main))
