# encoding: utf-8

from __future__ import unicode_literals
from workflow import MATCH_ALL, MATCH_ALLCHARS

import LastPassVaultManager as lpvm

####################################################################
# Constants
####################################################################
BROWSER_CHROME = 1
BROWSER_FIREFOX = 2
BROWSER_SAFARI = 3


class LpvmUtilities:

    def __init__(self, wf):
        """
        Initialize an instance of the class (primarily so that we can use the
        same Workflow() and pass it aroud once).
        """
        self.wf = wf
        self.log = self.wf.logger

    def download_data(self):
        """
        Download data from LastPass and coerce it to Unicode:
        """
        data = lpvm.download_data()

        self.log.debug('Downloaded data: {}'.format(data))

        return [{k: self.wf.decode(v) for k, v in i.iteritems()} for i in data]

    def print_utf8(self, string):
        print(string.encode('utf-8'))

    def search_item_fields(self, item):
        """
        The function used to search individual lastpass vault items.
        """
        elements = []
        elements.append(item['hostname'])
        elements.append(item['url'])
        return ' '.join(elements)

    def search_vault(self, query):
        """
        Search the LastPass vault for an optional passed query.
        """
        results = self.wf.cached_data(
            'vault_items',
            self.download_data,
            max_age=int(self.wf.settings['general']['cache_bust'])
        )

        # If a query is passed, filter the results:
        if query:
            results = self.wf.filter(
                query,
                results,
                self.search_item_fields,
                match_on=MATCH_ALL ^ MATCH_ALLCHARS
            )

        self.log.debug('Search results: {}'.format(results))

        return results

    def set_config_defaults(self):
        """
        Configure some default options (unless they already exist).
        """
        self.wf.settings.setdefault(
            'general',
            {
                'cache_bust': 300,
                'browser': BROWSER_CHROME
            }
        )
        self.wf.settings.setdefault(
            'passwords',
            {
                'number': 10,
                'length': 20
            }
        )
