# encoding: utf-8

from __future__ import unicode_literals
from argparser import ArgParser, ArgParserError
from utilities import BROWSER_CHROME, BROWSER_SAFARI
from workflow import Workflow

import os
import subprocess
import sys
import utilities

####################################################################
# Alfred Commands
####################################################################
ALFRED_AS_SETTINGS = 'tell application "Alfred 2" to search "lpsettings"'

####################################################################
# Miscellaneous
####################################################################
DEFAULT_COMMAND = 'list-settings'
REPO_URL = 'https://github.com/bachya/lp-vault-manager'

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
    log.debug('Parsed query: {}'.format(ap.query))

    # 1. Commands with no manual entry.
    if ap.delimiter not in ap.query:
        # COMMAND: LastPass Login
        if ap.command == 'lastpass-login':
            log.debug('Executing command: lastpass-login')
            if util.is_logged_in():
                wf.add_item(
                    'You are already logged in.',
                    'The entirety of LastPass Vault Manager is open to you.',
                    valid=False,
                    icon='icons/warning.png')
                wf.send_feedback()
            else:
                subprocess.call([
                    'python',
                    wf.workflowfile('lpsettings_exec.py'),
                    'login'
                ])
            sys.exit(0)

        # COMMAND: List Ambiguous Settings
        elif ap.command == 'list-ambiguous-settings':
            wf.add_item('Yes',
                        'Ambiguous characters should be avoided.',
                        valid=True,
                        arg='set-avoid-ambiguous true',
                        icon='icons/confirm.png')
            wf.add_item('No',
                        'Ambiguous characters should not be avoided.',
                        valid=True,
                        arg='set-avoid-ambiguous false',
                        icon='icons/no.png')

            wf.send_feedback()
            sys.exit(0)

        # COMMAND: List Browsers
        elif ap.command == 'list-browsers':
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
                            autocomplete='lastpass-login',
                            icon='icons/login.png')
                wf.add_item('Logout From LastPass',
                            'You will need to log in again before continuing!',
                            valid=True,
                            arg='logout',
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

        # COMMAND: List Lowercase Settings
        elif ap.command == 'list-lowercase-settings':
            wf.add_item('Yes',
                        'Lowercase letters should be included in generated ' +
                        'passwords.',
                        valid=True,
                        arg='set-use-lowercase true',
                        icon='icons/confirm.png')
            wf.add_item('No',
                        'Lowercase letters should not be included in ' +
                        'generated passwords.',
                        valid=True,
                        arg='set-use-lowercase false',
                        icon='icons/no.png')

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
            wf.add_item('Use Uppercase Letters',
                        'Should uppercase letters should be in generated ' +
                        'passwords?',
                        autocomplete='list-uppercase-settings',
                        icon='icons/password-uppercase.png')
            wf.add_item('Use Lowercase Letters',
                        'Should lowercase letters should be in generated ' +
                        'passwords?',
                        autocomplete='list-lowercase-settings',
                        icon='icons/password-lowercase.png')
            wf.add_item('Use Digits',
                        'Should digits should be in generated passwords?',
                        autocomplete='list-digits-settings',
                        icon='icons/password-digits.png')
            wf.add_item('Use Symbols',
                        'Should symbols should be in generated passwords?',
                        autocomplete='list-symbols-settings',
                        icon='icons/password-symbols.png')
            wf.add_item('Avoid Ambiguous Characters',
                        'Should ambiguous characters be avoided?',
                        autocomplete='list-ambiguous-settings',
                        icon='icons/password-ambiguous.png')

            wf.send_feedback()
            sys.exit(0)

        # COMMAND: List Digits Settings
        elif ap.command == 'list-digits-settings':
            wf.add_item('Yes',
                        'Digits should be included in generated passwords.',
                        valid=True,
                        arg='set-use-digits true',
                        icon='icons/confirm.png')
            wf.add_item('No',
                        'Digits should not be included in generated passwords.',
                        valid=True,
                        arg='set-use-digits false',
                        icon='icons/no.png')

            wf.send_feedback()
            sys.exit(0)

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
                        arg='open-url {}'.format(REPO_URL),
                        icon='icons/github.png')

            wf.send_feedback()
            sys.exit(0)

        # COMMAND: List Symbols Settings
        elif ap.command == 'list-symbols-settings':
            wf.add_item('Yes',
                        'Symbols should be included in generated passwords.',
                        valid=True,
                        arg='set-use-symbols true',
                        icon='icons/confirm.png')
            wf.add_item('No',
                        'Symbols should not be included in generated ' +
                        'passwords.',
                        valid=True,
                        arg='set-use-symbols false',
                        icon='icons/no.png')

            wf.send_feedback()
            sys.exit(0)

        # COMMAND: List Uppercase Settings
        elif ap.command == 'list-uppercase-settings':
            wf.add_item('Yes',
                        'Uppercase letters should be included in generated ' +
                        'passwords.',
                        valid=True,
                        arg='set-use-uppercase true',
                        icon='icons/confirm.png')
            wf.add_item('No',
                        'Uppercase letters should not be included in ' +
                        'generated passwords.',
                        valid=True,
                        arg='set-use-uppercase false',
                        icon='icons/no.png')

            wf.send_feedback()
            sys.exit(0)
        else:
            log.error('Unknown command: {}'.format(ap.command))
            sys.exit(1)

    # 2. Commands with no manual entry.
    else:
        # If the user has backspaced all the way back to the delimiter, reset
        # the whole thing:
        if ap.query.endswith(ap.delimiter):
            subprocess.call(['osascript', '-e', ALFRED_AS_SETTINGS])
            sys.exit(0)

        # COMMAND: Cache
        if ap.command == 'cache':
            existing_cache = wf.settings['general']['cache_bust']
            if existing_cache:
                sub_msg = 'Current cache timeout: {!s}'.format(existing_cache)
            else:
                sub_msg = 'Hit ENTER to confirm.'

            if ap.arg.strip():
                if ap.arg.isdigit():
                    wf.add_item('Set timeout to {!s} seconds.'.format(ap.arg),
                                sub_msg,
                                valid=True,
                                arg='set-timeout {!s}'.format(ap.arg),
                                icon='icons/confirm.png')
                else:
                    wf.add_item(
                        '{!s} is not an integer.'.format(ap.arg),
                        'Please ensure you enter an integer.',
                        icon='icons/warning.png'
                    )
            else:
                wf.add_item(
                    'Input a cache timeout in seconds.',
                    sub_msg,
                    icon='icons/clock.png')

            wf.send_feedback()
            sys.exit(0)

        # COMMAND: lpass Path
        elif ap.command == 'lpass-path':
            existing_path = wf.settings['lastpass']['path']
            if existing_path:
                sub_msg = 'Current path: {}'.format(existing_path)
            else:
                sub_msg = 'Hit ENTER to confirm.'

            if ap.arg.strip():
                if os.path.exists(ap.arg):
                    wf.add_item('Set path to {}'.format(ap.arg),
                                sub_msg,
                                valid=True,
                                arg='set-lpass-path {}'.format(ap.arg),
                                icon='icons/confirm.png')
                else:
                    wf.add_item(
                        '{} is not a valid path.'.format(ap.arg),
                        'Please ensure you enter a valid path.',
                        icon='icons/warning.png'
                    )
            else:
                wf.add_item(
                    'Input a filepath to the `lpass` executable.',
                    sub_msg,
                    icon='icons/clock.png')

            wf.send_feedback()
            sys.exit(0)

        # COMMAND: Password Length
        if ap.command == 'password-length':
            existing_len = wf.settings['passwords']['length']
            if existing_len:
                sub_msg = 'Current password length: {!s}'.format(existing_len)
            else:
                sub_msg = 'Hit ENTER to confirm.'

            if ap.arg.strip():
                if ap.arg.isdigit():
                    wf.add_item('Set length to {!s} characters.'.format(ap.arg),
                                sub_msg,
                                valid=True,
                                arg='set-password-length {!s}'.format(ap.arg),
                                icon='icons/confirm.png')
                else:
                    wf.add_item(
                        '{!s} is not an integer.'.format(ap.arg),
                        'Please ensure you enter an integer.',
                        icon='icons/warning.png'
                    )
            else:
                wf.add_item(
                    'Input a password length in number of characters.',
                    sub_msg,
                    icon='icons/clock.png')

            wf.send_feedback()
            sys.exit(0)

        # COMMAND: Password Number
        if ap.command == 'password-number':
            existing_num = wf.settings['passwords']['number']
            if existing_num:
                sub_msg = 'Current password number: {!s}'.format(existing_num)
            else:
                sub_msg = 'Hit ENTER to confirm.'

            if ap.arg.strip():
                if ap.arg.isdigit():
                    wf.add_item('Set number to {!s} passwords.'.format(ap.arg),
                                sub_msg,
                                valid=True,
                                arg='set-password-number {!s}'.format(ap.arg),
                                icon='icons/confirm.png')
                else:
                    wf.add_item(
                        '{!s} is not an integer.'.format(ap.arg),
                        'Please ensure you enter an integer.',
                        icon='icons/warning.png'
                    )
            else:
                wf.add_item(
                    'Input a number of passwords to generate.',
                    sub_msg,
                    icon='icons/clock.png')

            wf.send_feedback()
            sys.exit(0)
        # COMMAND: Username
        elif ap.command == 'username':
            existing_username = wf.settings['lastpass']['username']
            if existing_username:
                sub_msg = 'Current username: {}'.format(existing_username)
            else:
                sub_msg = 'Hit ENTER to confirm.'

            wf.add_item(
                'Set username to {}'.format(ap.arg),
                sub_msg,
                valid=True,
                arg='set-username {}'.format(ap.arg),
                icon='icons/confirm.png'
            )

            wf.send_feedback()
            sys.exit(0)


if __name__ == '__main__':
    # Configure a Workflow class and a logger:
    wf = Workflow(libraries=['./lib'])
    log = wf.logger

    # Configure a LpvmUtilities class:
    util = utilities.LpvmUtilities(wf)

    # Run!
    sys.exit(wf.run(main))
