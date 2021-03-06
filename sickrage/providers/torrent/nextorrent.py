# Author: echel0n <echel0n@sickrage.ca>
# URL: https://sickrage.ca
# Git: https://git.sickrage.ca/SiCKRAGE/sickrage
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
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import unicodedata
from urlparse import urljoin

import sickrage
from sickrage.core.caches.tv_cache import TVCache
from sickrage.core.helpers import bs4_parser, convert_size, tryInt
from sickrage.providers import TorrentProvider


class NextorrentProvider(TorrentProvider):
    def __init__(self):

        super(NextorrentProvider, self).__init__("Nextorrent", 'http://nextorrent.pw', False)

        self.supports_backlog = True
        self.confirmed = True
        self.ratio = None
        self.minseed = None
        self.minleech = None

        self.cache = TVCache(self, min_time=15)

        self.urls.update({
            'series': '{base_url}/torrents/series'.format(base_url=self.urls['base_url'])
        })

    def seed_ratio(self):
        return self.ratio

    def get_download_url(self, url):
        try:
            data = sickrage.srCore.srWebSession.get(urljoin(self.urls['base_url'], url)).text
            with bs4_parser(data) as html:
                return html.find('div', class_="btn-magnet").find('a').get('href')
        except Exception:
            pass

    def search(self, search_strings, search_mode='eponly', epcount=0, age=0, epObj=None):
        results = []

        for mode in search_strings:
            items = []
            sickrage.srCore.srLogger.debug('Search Mode: {}'.format(mode))
            for search_string in search_strings[mode]:
                if mode != 'RSS':
                    sickrage.srCore.srLogger.debug('Search string: {}'.format(search_string))

                if mode == 'RSS':
                    search_url = self.urls['series']
                else:
                    search_url = urljoin(self.urls['base_url'], search_string)

                try:
                    data = sickrage.srCore.srWebSession.get(search_url, cache=False).text
                except Exception:
                    sickrage.srCore.srLogger.debug('No data returned from provider')
                    continue

                with bs4_parser(data) as html:
                    torrent_rows = html.find_all('tr')
                    for row in torrent_rows:
                        for torrent in row.find_all('td'):
                            for link in torrent.find_all('a'):
                                fileType = ''.join(link.find_previous('i')["class"])
                                fileType = unicodedata.normalize('NFKD', fileType). \
                                    encode(sickrage.SYS_ENCODING, 'ignore')

                                if fileType == "Series":
                                    title = link.get_text(strip=True)
                                    download_url = self.get_download_url(link.get('href'))

                                    if not all([title, download_url]):
                                        continue

                                    # size
                                    size = convert_size(link.findNext('td').text) or -1

                                    # Filter unseeded torrent
                                    seeders = tryInt(link.find_next('img', alt='seeders').parent.text, 0)
                                    leechers = tryInt(link.find_next('img', alt='leechers').parent.text, 0)

                                    if seeders < self.minseed or leechers < self.minleech:
                                        if mode != 'RSS':
                                            sickrage.srCore.srLogger.debug(
                                                "Discarding torrent because it doesn't meet the minimum seeders or leechers: {} (S:{} L:{})".format(
                                                    title, seeders, leechers))
                                        continue

                                    items += [{
                                        'title': title,
                                        'link': download_url,
                                        'size': size,
                                        'seeders': seeders,
                                        'leechers': leechers,
                                    }]

                                    if mode != 'RSS':
                                        sickrage.srCore.srLogger.debug("Found result: {}".format(title))

            # For each search mode sort all the items by seeders if available
            items.sort(key=lambda d: int(d.get('seeders', 0)), reverse=True)
            results += items

        return results
