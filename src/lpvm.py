# encoding: utf-8

from __future__ import unicode_literals

from urlparse import urlparse
from workflow import Workflow, MATCH_ALL, MATCH_ALLCHARS

import argparse
import subprocess
import sys

####################################################################
# Browsers
####################################################################
BROWSER_CHROME = 1
BROWSER_FIREFOX = 2
BROWSER_SAFARI = 3


####################################################################
# Helper Functions
####################################################################
def _search_vault(wf, vault, query):
    """
    Searches the LastPass vault for any items
    that match a certain query (based on the
    fields specified in `search_item_fields`).
    """
    results = wf.cached_data(
        'vault_items',
        vault.download_data,
        max_age=int(wf.settings['general']['cache_bust'])
    )

    if query:
        results = wf.filter(
            query,
            results,
            search_item_fields,
            match_on=MATCH_ALL ^ MATCH_ALLCHARS
        )

    return results


def download_data(wf, vault):
    """
    Blows away the cached LastPass vault data
    and re-downloads a copy.
    """
    data = vault.download_data()
    if data:
        wf.cache_data('vault_items', data)
        print('Metadata successfully downloaded!')
    else:
        print('Metadata download failed!')


def generate_passwords(wf, vault):
    """
    Generates a series of random passwords and
    outputs the results as Script Filter-friendly
    XML.
    """
    n = wf.settings['passwords']['number']
    l = wf.settings['passwords']['length']
    passwords = vault.generate_passwords(n, l)
    for password in passwords:
        wf.add_item(
            password,
            'Click to copy to clipboard.',
            arg=password,
            valid=True,
            uid=password
        )

    wf.send_feedback()


def search_item_fields(item):
    """
    The function used to search individual lastpass
    vault items.
    """
    elements = []
    elements.append(item['hostname'])
    elements.append(item['url'])
    return ' '.join(elements)


def search_url(wf, vault):
    """
    Searches for the user's default browser's current tab
    in their vault and returns Script Filter-friendly
    XML.
    """
    browser = wf.settings['general']['browser']
    url = subprocess.check_output(
        ['osascript',
         'get-url-from-browser.scpt',
         str(browser)]
    ).rstrip()

    uri = '{uri.netloc}'.format(uri=urlparse(url))
    results = _search_vault(
        wf,
        vault,
        uri
    )
    if results:
        for result in results:
            wf.add_item(
                result['hostname'],
                'Click to launch; ' +
                '\u2318-Click to copy password; ' +
                'Shift-Click to copy username.',
                modifier_subtitles={
                    'cmd': '\u2318-Click to copy password',
                    'shift': 'Shift-Click to copy username'
                },
                arg='{}***{}'.format(result['hostname'], result['url']),
                autocomplete=result['hostname'],
                valid=True,
                uid=result['hostname']
            )
    else:
        wf.add_item(
            'No items matching the {}.'.format(uri),
            valid=False,
            icon='icons/warning.png'
        )

    wf.send_feedback()


def search_vault(wf, vault, query):
    """
    Searches a LastPass vault for a specific query and
    outputs the results as Script Filter-friendly XML.
    """
    results = _search_vault(wf, vault, query)
    if results:
        for result in results:
            wf.add_item(
                result['hostname'],
                'Click to launch; ' +
                '\u2318-Click to copy password; ' +
                'Shift-Click to copy username.',
                modifier_subtitles={
                    'cmd': '\u2318-Click to copy password',
                    'shift': 'Shift-Click to copy username'
                },
                arg='{}***{}'.format(result['hostname'], result['url']),
                autocomplete=result['hostname'],
                valid=True,
                uid=result['hostname']
            )
    else:
        wf.add_item(
            'No items matching ' + query,
            valid=False,
            icon='icons/warning.png'
        )

    wf.send_feedback()


def set_password_length(wf, vault, query):
    """
    Sets a default length for generated passwords.
    """
    try:
        length = int(query)
        if length <= 0:
            length = vault.DEFAULT_PASSWORD_LENGTH
    except ValueError:
        length = vault.DEFAULT_PASSWORD_LENGTH
    wf.settings['passwords']['length'] = length
    wf.settings.save()
    print(str(length) + ' characters')


####################################################################
# Main Script
####################################################################
def main(wf):
    # Create an argument parser to handle the arguments coming in
    # from Alfred:
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("query", nargs='?', default=None)
    args = parser.parse_args(wf.args)

    # Create an instance of LastPassVaultManager:
    from LastPassVaultManager import LastPassVaultManager
    vault = LastPassVaultManager()

    # Try a simple `lpass` command; if it returns a non-zero
    # exit status, we can safely assume that the user isn't
    # logged into LastPass.
    try:
        subprocess.check_output(['/usr/local/bin/lpass', 'ls'])
    except subprocess.CalledProcessError:
        wf.add_item(
            'Not logged in to LastPass!',
            'Log in by running `lpsettings` and following along.',
            valid=False,
            icon='icons/warning.png'
        )

        wf.send_feedback()
        return 0

    # Download Data:
    if args.command == 'download-data':
        download_data(wf, vault)
        return 0

    # Generate Password:
    elif args.command == 'generate-passwords':
        generate_passwords(wf, vault)
        return 0

    # Get Password:
    elif args.command == 'get-password':
        hostname = args.query.split('***')[0]
        password = vault.get_field_value(hostname, 'Password')
        print(password)
        return 0

    # Get Username:
    elif args.command == 'get-username':
        hostname = args.query.split('***')[0]
        username = vault.get_field_value(hostname, 'Username')
        print(username)
        return 0

    # Open URL:
    elif args.command == 'open-url':
        url = args.query.split('***')[1]
        subprocess.call(['open', url])
        return 0

    # Search Vault:
    elif args.command == 'search-vault':
        search_vault(wf, vault, args.query)
        return 0

    # Search URL:
    elif args.command == 'search-url':
        search_url(wf, vault)
        return 0

    # Set Length of Passwords
    elif args.command == 'set-password-length':
        set_password_length(wf, vault, args.query)
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
        'passwords',
        {
            'number': 10,
            'length': 20
        }
    )

    sys.exit(wf.run(main))
