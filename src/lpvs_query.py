# encoding: utf-8

from __future__ import unicode_literals
from argparser import ArgParser, ArgParserError
from urlparse import urlparse
from workflow import Workflow
from workflow.background import is_running

import re
import subprocess
import sys
import utilities

####################################################################
# Miscellaneous
####################################################################
DEFAULT_COMMAND = 'search-vault-for-query'

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

    # COMMAND: Search Vault For Query
    if ap.command == 'search-vault-for-query':
        # In this case, the user is requesting a "details view" for a particular
        # hostname.
        if ap.arg and ap.arg.startswith('view-details'):
            log.debug('Executing command: view-details')
            output_details_results(ap)
        # In this case, the user is requesting all vault items that match the
        # provided query.
        else:
            log.debug('Executing command: search-vault-for-query')
            ap.command = 'get-password'
            output_query_vault_results(ap)

        sys.exit(0)

    # COMMAND: Search Vault For URL
    elif ap.command == 'search-vault-for-url':
        # Figure out the URL of the current tab of the
        # default browser:
        url = wf.decode(subprocess.check_output(
            ['osascript',
             'get-url-from-browser.scpt',
             str(wf.settings['general']['browser'])]
        )).rstrip()
        uri = str('{uri.netloc}'.format(uri=urlparse(url)))

        log.debug('Decoded URI from browser: {!s}'.format(uri))

        # In this case, the user is requesting a "details view" for a particular
        # hostname.
        if ap.arg and ap.arg.startswith('view-details'):
            log.debug('Executing command: view-details')
            output_details_results(ap)
        # In this case, the user is requesting all vault items that match the
        # provided query.
        else:
            log.debug('Executing command: search-vault-for-url')
            log.debug('Searching vault for URL: {!s}'.format(uri))
            ap.command = 'get-password'
            ap.arg = uri
            output_query_vault_results(ap)

        sys.exit(0)
    else:
        log.error('Unknown command: {}'.format(ap.command))
        sys.exit(1)


def output_details_results(ap):
    hostname = re.sub('view-details ', '', ap.arg.split('***')[0])

    log.debug('Getting details for "{}"...'.format(hostname))
    item_details = util.get_item_details(hostname)
    if item_details:
        wf.add_item(
            'Exploring: {}'.format(hostname),
            'Hit ENTER on any option below to copy its value.',
            valid=False,
            icon='icons/info.png'
        )

        log.debug('Detail results: {}'.format(item_details))

        for i in item_details:
            pieces = i.partition(': ')
            field = pieces[0]
            value = pieces[2]

            if field and value:
                wf.add_item(
                    field,
                    value,
                    valid=True,
                    arg='get-raw-value {}***{}***{}'.format(
                        field,
                        value,
                        hostname)
                )
    else:
        wf.add_item(
            'No items matching "{}".'.format(ap.arg),
            'View the `lpvs` debug log for more information.',
            valid=False,
            icon='icons/warning.png'
        )

    wf.send_feedback()
    return


def output_query_vault_results(ap):
    """
    A simple helper function to manage outputting LastPass vault items to an
    Alfred Script Filter. Uses an ArgParser instance to figure out which
    command and argument to use.
    """
    # Notify the user if the cache is being updated:
    if is_running('update'):
        log.debug('Currenly running update; notifying user...')
        wf.add_item(
            'Getting new data from LastPass.',
            'This should only take a few moments, so hang tight.',
            valid=False,
            icon='icons/loading.png',
            uid='1'
        )

    results = util.search_vault_for_query(ap.arg)
    if results:
        for result in results:
            wf.add_item(
                result['hostname'],
                'TAB to explore; ' +
                'ENTER to copy password; ' +
                '\u2318-Click to copy username; ' +
                'Shift-Click to open URL',
                modifier_subtitles={
                    'cmd': '\u2318-Click to copy username.',
                    'shift': 'Shift-Click to open the URL.'
                },
                valid=True,
                arg='{} {}***{}'.format(ap.command,
                                        result['hostname'],
                                        result['url']),
                autocomplete='view-details {}'.format(result['hostname']),
            )
    else:
        wf.add_item(
            'No items matching "{}".'.format(ap.arg),
            'View the `lpvs` debug log for more information.',
            valid=False,
            icon='icons/warning.png'
        )

    wf.send_feedback()
    return

if __name__ == '__main__':
    # Configure a Workflow class and a logger:
    wf = Workflow(libraries=['./lib'])
    log = wf.logger

    # Configure a LpvmUtilities class:
    util = utilities.LpvmUtilities(wf)

    # Notify the user if they are not logged in:
    if not util.is_logged_in():
        log.warning('Not logged into LastPass.')
        wf.add_item(
            'Not logged in to LastPass.',
            'Hit ENTER to open an Alfred command to login to LastPass.',
            valid=True,
            arg="login",
            icon='icons/warning.png'
        )

        wf.send_feedback()
        sys.exit(1)

    # Run!
    sys.exit(wf.run(main))
