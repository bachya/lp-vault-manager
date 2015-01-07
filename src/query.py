# encoding: utf-8

from __future__ import unicode_literals
from workflow import Workflow

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
    command = wf.args[0]
    query = None
    try:
        query = wf.args[1]
    except IndexError:
        log.error('Query not provided.')
        sys.exit()

    # Search the vault and return the necessary Script Filter XML:
    if command == 'search-vault':
        results = util.search_vault(query)
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

    else:
        log.error('Unknown command: {}'.format(command))

if __name__ == '__main__':
    # Configure a Workflow class and a logger:
    wf = Workflow()
    log = wf.logger

    # Configure a LpvmUtilities class:
    util = utilities.LpvmUtilities(wf)

    # Initialize setting categories (unless they already exist):
    util.set_config_defaults()

    # Run!
    sys.exit(wf.run(main))
