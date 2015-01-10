# encoding: utf-8

from __future__ import unicode_literals
from workflow import Workflow

import lpvaultmanager as lpvm


def download_data(lpass_path):
    lpv = lpvm.LastPassVaultManager(lpass_path)
    data = lpv.download_data()
    return [{k: wf.decode(v) for k, v in i.iteritems()} for i in data]


def main(wf):
    try:
        def wrapper():
            return download_data(wf.settings['lastpass']['path'])

        results = wf.cached_data(
            'vault_items',
            wrapper,
            max_age=int(wf.settings['general']['cache_bust'])
        )

        wf.logger.debug('{} vault items cached.'.format(len(results)))
    except lpvm.LastPassVaultManagerError, e:
        wf.logger.error(
            'There was an issue downloading LastPass data: {}'.format(e)
        )
        return []

if __name__ == '__main__':
    wf = Workflow()
    wf.run(main)
