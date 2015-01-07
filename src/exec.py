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
        pass

    # Do the proper thing based on the command:
    if command == 'download-data':
        data = util.download_data()
        if data:
            wf.cache_data('vault_items', data)
            util.print_utf8('LastPass metadata successfully downloaded.')
        else:
            util.print_utf8('LastPass metadata download failed.')

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
