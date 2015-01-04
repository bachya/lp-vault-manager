# encoding: utf-8

from __future__ import unicode_literals
from ArgParser import ArgParser
from workflow import Workflow

import sys

####################################################################
# Constants
####################################################################
BROWSER_CHROME = 1
BROWSER_FIREFOX = 2
BROWSER_SAFARI = 3

####################################################################
# Logger Instance
####################################################################
log = None


def main(wf):
    ap = ArgParser(' '.join(wf.args))
    ap.import_script()
    ap.run_command_with_args()

if __name__ == '__main__':
    wf = Workflow()
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

    log.debug('Setting default settings: {}'.format(wf.settings))

    sys.exit(wf.run(main))
