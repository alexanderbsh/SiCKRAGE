# Author: Idan Gutman
# URL: http://github.com/SiCKRAGETV/SickRage/
#
# This file is part of SickRage.
#
# SickRage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickRage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import re
import traceback
import urllib

import sickrage
from sickrage.core.caches import tv_cache
from sickrage.core.helpers import bs4_parser
from sickrage.providers import TorrentProvider


class TorrentLeechProvider(TorrentProvider):
    def __init__(self):

        super(TorrentLeechProvider, self).__init__("TorrentLeech",'torrentleech.org')

        self.supportsBacklog = True

        self.username = None
        self.password = None
        self.ratio = None
        self.minseed = None
        self.minleech = None

        self.urls.update({
            'login': '{base_url}/user/account/login/'.format(base_url=self.urls['base_url']),
            'detail': '{base_url}/torrent/%s'.format(base_url=self.urls['base_url']),
            'search': '{base_url}/torrents/browse/index/query/%s/categories/%s'.format(base_url=self.urls['base_url']),
            'download': '{base_url}/%s'.format(base_url=self.urls['base_url']),
            'index': '{base_url}/torrents/browse/index/categories/%s'.format(base_url=self.urls['base_url'])
        })

        self.categories = "2,7,26,27,32,34,35"

        self.proper_strings = ['PROPER', 'REPACK']

        self.cache = TorrentLeechCache(self)

    def _doLogin(self):

        login_params = {'username': self.username,
                        'password': self.password,
                        'remember_me': 'on',
                        'login': 'submit'}

        try:
            response = self.session.post(self.urls['login'], data=login_params, timeout=30).content
        except Exception:
            sickrage.srLogger.warning("[{}]: Unable to connect to provider".format(self.name))
            return False

        if re.search('Invalid Username/password', response) or re.search('<title>Login :: TorrentLeech.org</title>',
                                                                         response):
            sickrage.srLogger.warning("[{}]: Invalid username or password. Check your settings".format(self.name))
            return False

        return True

    def search(self, search_params, search_mode='eponly', epcount=0, age=0, epObj=None):

        results = []
        items = {'Season': [], 'Episode': [], 'RSS': []}

        if not self._doLogin():
            return results

        for mode in search_params.keys():
            sickrage.srLogger.debug("Search Mode: %s" % mode)
            for search_string in search_params[mode]:

                if mode is 'RSS':
                    searchURL = self.urls['index'] % self.categories
                else:
                    searchURL = self.urls['search'] % (
                        urllib.quote_plus(search_string.encode('utf-8')), self.categories)
                    sickrage.srLogger.debug("Search string: %s " % search_string)

                sickrage.srLogger.debug("Search URL: %s" % searchURL)

                try:
                    data = self.session.get(searchURL).content
                except Exception:
                    continue

                try:
                    with bs4_parser(data) as html:
                        torrent_table = html.find('table', attrs={'id': 'torrenttable'})
                        torrent_rows = torrent_table.find_all('tr') if torrent_table else []

                        # Continue only if one Release is found
                        if len(torrent_rows) < 2:
                            sickrage.srLogger.debug("Data returned from provider does not contain any torrents")
                            continue

                        for result in torrent_table.find_all('tr')[1:]:

                            try:
                                link = result.find('td', attrs={'class': 'name'}).find('a')
                                url = result.find('td', attrs={'class': 'quickdownload'}).find('a')
                                title = link.string
                                download_url = self.urls['download'] % url['href']
                                seeders = int(result.find('td', attrs={'class': 'seeders'}).string)
                                leechers = int(result.find('td', attrs={'class': 'leechers'}).string)
                                # FIXME
                                size = -1
                            except (AttributeError, TypeError):
                                continue

                            if not all([title, download_url]):
                                continue

                            # Filter unseeded torrent
                            if seeders < self.minseed or leechers < self.minleech:
                                if mode is not 'RSS':
                                    sickrage.srLogger.debug(
                                        "Discarding torrent because it doesn't meet the minimum seeders or leechers: {0} (S:{1} L:{2})".format(
                                            title, seeders, leechers))
                                continue

                            item = title, download_url, size, seeders, leechers
                            if mode is not 'RSS':
                                sickrage.srLogger.debug("Found result: %s " % title)

                            items[mode].append(item)

                except Exception:
                    sickrage.srLogger.error("Failed parsing provider. Traceback: {}".format(traceback.format_exc()))

            # For each search mode sort all the items by seeders if available
            items[mode].sort(key=lambda tup: tup[3], reverse=True)

            results += items[mode]

        return results

    def seedRatio(self):
        return self.ratio


class TorrentLeechCache(tv_cache.TVCache):
    def __init__(self, provider_obj):
        tv_cache.TVCache.__init__(self, provider_obj)

        # only poll TorrentLeech every 20 minutes max
        self.minTime = 20

    def _getRSSData(self):
        search_params = {'RSS': ['']}
        return {'entries': self.provider.search(search_params)}
