# encoding: utf-8

from __future__ import unicode_literals

from lpvm import BROWSER_CHROME, BROWSER_SAFARI
from workflow import Workflow

import argparse
import os
import subprocess
import sys

####################################################################
# Constants
####################################################################
ALFRED_AS_LOGIN = 'tell application "Alfred 2" to search ">{} login {} && exit"'
ALFRED_AS_SETTINGS = 'tell application "Alfred 2" to search "lpsettings"'
DEFAULT_COMMAND = 'list-settings'
DELIMITER = '⟩'
GITHUB_URL = 'https://github.com/bachya/lp-vault-manager'


def determine_query_pieces(query):
    if DELIMITER in query:
        command, query = [s.strip() for s in query.split(DELIMITER)]
        if not query:
            query = None
    else:
        command = query
        query = None

    if not command:
        command = DEFAULT_COMMAND

    log.debug('Command: {}'.format(command))
    log.debug('Query: {}'.format(query))
    return [command, query]


def main(wf):
    # Create an argument parser to handle the arguments coming in
    # from Alfred:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs='?')
    parser.add_argument("--browser", nargs='?', type=int)
    parser.add_argument("--lpass_path", nargs='?')
    parser.add_argument("--password_number", nargs='?', type=int)
    parser.add_argument("--password_length", nargs='?', type=int)
    parser.add_argument("--timeout", nargs='?', type=int)
    parser.add_argument("--username", nargs='?')
    args = parser.parse_args(wf.args)

    ####################################################################
    # 1. Actions with no command or query
    ####################################################################
    if args.browser:
        value = int(args.browser)
        log.debug('Setting browser to {!s}'.format(value))
        wf.settings['general']['browser'] = value
        wf.settings.save()
        if value == BROWSER_CHROME:
            browser = 'Google Chrome'
        elif value == BROWSER_SAFARI:
            browser = 'Safari'
        print('Browser set: {!s}'.format(browser))
        return 0

    if args.lpass_path:
        value = args.lpass_path
        log.debug('Setting filepath to {}'.format(value))
        wf.settings['lastpass']['path'] = value
        wf.settings.save()
        print('Filepath set: {}'.format(value))
        return 0

    if args.password_number:
        value = int(args.password_number)
        log.debug('Setting number of passwords to {!s}'.format(value))
        wf.settings['passwords']['number'] = value
        wf.settings.save()
        print('Password number set: {!s} passwords'.format(value))
        return 0

    if args.password_length:
        value = int(args.password_length)
        log.debug('Setting length of passwords to {!s}'.format(value))
        wf.settings['passwords']['length'] = value
        wf.settings.save()
        print('Password length set: {!s} chars'.format(value))
        return 0

    if args.timeout:
        value = int(args.timeout)
        log.debug('Setting cache timeout to {!s}'.format(value))
        wf.settings['general']['cache_bust'] = value
        wf.settings.save()
        print('Cache timeout set: {!s} seconds'.format(value))
        return 0

    if args.username:
        value = args.username
        log.debug('Setting LastPass username to {}'.format(value))
        wf.settings['lastpass']['username'] = value
        wf.settings.save()
        print('LastPass username set: {}'.format(value))
        return 0

    # Determine what "pieces" (command/query) the passed string has:
    command, query = determine_query_pieces(args.query)

    ####################################################################
    # 2. Actions with only a command
    ####################################################################
    if DELIMITER not in args.query:
        if command == 'cache-timeout':
            wf.add_item('Input a cache timeout in seconds.',
                        'Current timeout: '
                        + str(wf.settings['general']['cache_bust']),
                        icon='icons/clock.png')

            wf.send_feedback()
            return 0
        elif command == 'edit-config':
            subprocess.call(['open', wf.settings_path])
            return 0
        elif command == 'lastpass-login':
            lpass_path = wf.settings['lastpass']['path']
            username = wf.settings['lastpass']['username']
            subprocess.call([
                'osascript',
                '-e',
                ALFRED_AS_LOGIN.format(lpass_path, username)
            ])
            return 0
        elif command == 'lastpass-logout':
            lpass_path = wf.settings['lastpass']['path']
            subprocess.call([lpass_path, 'logout', '--force'])
            return 0
        elif command == 'list-browsers':
            wf.add_item('Google Chrome',
                        'Hit ENTER to use Google Chrome.',
                        valid=True,
                        arg='--browser {!s}'.format(BROWSER_CHROME),
                        icon='icons/chrome.png')
            wf.add_item('Safari',
                        'Hit ENTER to use Safari.',
                        valid=True,
                        arg='--browser {!s}'.format(BROWSER_SAFARI),
                        icon='icons/safari.png')

            wf.send_feedback()
            return 0
        elif command == 'list-lastpass-settings':
            if wf.settings['lastpass']['username'] == '':
                wf.add_item('No LastPass username in settings!',
                            'Hit ENTER to add one.',
                            autocomplete='username {} '.format(DELIMITER),
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
                            autocomplete='username {} '.format(DELIMITER),
                            icon='icons/user.png')
                wf.add_item('Set Cache Timeout',
                            'Enter the number of seconds to keep the cache.',
                            autocomplete='cache {} '.format(DELIMITER),
                            icon='icons/clock.png')
                wf.add_item('Set `lpass` Filepath',
                            'Enter the absolute path to `lpass`.',
                            autocomplete='lpass-path {} '.format(DELIMITER),
                            icon='icons/filepath.png')

            wf.send_feedback()
            return 0
        elif command == 'list-password-settings':
            wf.add_item('Set Number of Passwords',
                        'Enter the number of passwords that `lppg` creates.',
                        autocomplete='password-number {} '.format(DELIMITER),
                        icon='icons/password-number.png')
            wf.add_item('Set Password Length',
                        'Enter the length of a generated password.',
                        autocomplete='password-length {} '.format(DELIMITER),
                        icon='icons/password-length.png')

            wf.send_feedback()
            return 0
        elif command == 'list-settings':
            wf.add_item('Set Default Browser',
                        'Set the browser used by `lpbrowser`.',
                        autocomplete='list-browsers',
                        icon='icons/browser.png')
            wf.add_item('Modify LastPass Settings',
                        'Username, cache settings, etc.',
                        autocomplete='list-lastpass-settings',
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
                        arg='open-repo',
                        icon='icons/github.png')

            wf.send_feedback()
            return 0
        elif command == 'open-repo':
            subprocess.call(['open', GITHUB_URL])
            return 0

    ####################################################################
    # 3. Actions with a command and a query
    ####################################################################
    else:
        if args.query.endswith(DELIMITER):
            subprocess.call(['osascript', '-e', ALFRED_AS_SETTINGS])
            return 0

        if command == 'cache':
            if query:
                if query.isdigit():
                    wf.add_item('Set timeout to {!s} seconds.'.format(query),
                                'Hit ENTER to confirm.',
                                valid=True,
                                arg='--timeout {!s}'.format(query),
                                icon='icons/confirm.png')
                else:
                    wf.add_item('{!s} is not an integer.'.format(query),
                                'Please ensure you enter an integer.',
                                icon='icons/warning.png')
            else:
                wf.add_item('Input a cache timeout in seconds.',
                            'Current timeout: '
                            + str(wf.settings['general']['cache_bust']),
                            icon='icons/clock.png')

            wf.send_feedback()
            return 0
        elif command == 'lpass-path':
            if query:
                if os.path.exists(query):
                    wf.add_item('Set filepath to {}'.format(query),
                                'Hit ENTER to confirm.',
                                valid=True,
                                arg='--lpass_path {}'.format(query),
                                icon='icons/confirm.png')
                else:
                    wf.add_item('{!s} is not a valid filepath.'.format(query),
                                'Please ensure the path actually exists.',
                                icon='icons/warning.png')
            else:
                wf.add_item('Input the path to your instance of `lpass`.',
                            'Current filepath: '
                            + str(wf.settings['lastpass']['path']),
                            icon='icons/filepath.png')

            wf.send_feedback()
            return 0
        elif command == 'password-number':
            if query:
                if query.isdigit():
                    wf.add_item('Create {!s} passwords.'.format(query),
                                'Hit ENTER to confirm.',
                                valid=True,
                                arg='--password_number {!s}'.format(query),
                                icon='icons/confirm.png')
                else:
                    wf.add_item('{!s} is not an integer.'.format(query),
                                'Please ensure you enter an integer.',
                                icon='icons/warning.png')
            else:
                wf.add_item('Input the number of passwords created by `lppg`.',
                            'Current number: '
                            + str(wf.settings['passwords']['number']),
                            icon='icons/password-number.png')

            wf.send_feedback()
            return 0
        elif command == 'password-length':
            if query:
                if query.isdigit():
                    wf.add_item('Set password length to {!s}.'.format(query),
                                'Hit ENTER to confirm.',
                                valid=True,
                                arg='--password_length {!s}'.format(query),
                                icon='icons/confirm.png')
                else:
                    wf.add_item('{!s} is not an integer.'.format(query),
                                'Please ensure you enter an integer.',
                                icon='icons/warning.png')
            else:
                wf.add_item('Input the length of passwords created by `lppg`.',
                            'Current length: '
                            + str(wf.settings['passwords']['length']),
                            icon='icons/password-length.png')

            wf.send_feedback()
            return 0
        elif command == 'username':
            if query:
                wf.add_item('Set username to {}'.format(query),
                            'Hit ENTER to confirm.',
                            valid=True,
                            arg='--username {}'.format(query),
                            icon='icons/confirm.png')
            else:
                wf.add_item('Input your LastPass username.',
                            'Current username: '
                            + str(wf.settings['lastpass']['username']),
                            icon='icons/user.png')

            wf.send_feedback()
            return 0

if __name__ == '__main__':
    wf = Workflow(libraries=['./lib'])
    log = wf.logger

    # Initialize setting categories (unless they
    # already exist):
    wf.settings.setdefault(
        'general',
        {
            'cache_bust': 300,
            'browser': BROWSER_CHROME
        }
    )

    wf.settings.setdefault(
        'lastpass',
        {
            'path': '/usr/local/bin/lpass',
            'username': ''
        }
    )

    wf.settings.setdefault(
        'passwords',
        {
            'number': 10,
            'length': 20
        }
    )
    wf.settings.save()

    sys.exit(wf.run(main))
