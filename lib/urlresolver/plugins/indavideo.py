'''
    indavideo urlresolver plugin
    Copyright (C) 2013 Bagira

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

from t0mm0.common.net import Net
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay.interfaces import PluginSettings
from urlresolver.plugnplay import Plugin
import re
import urlparse
import urllib2
from urlresolver import common
import os

class IndavideoResolver(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "indavideo"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()

    def get_media_url(self, host, media_id):
        plugin = 'plugin://plugin.video.indavideo/?action=play_video&videoid=' +\
                 media_id
        return plugin

    def get_url(self, host, media_id):
        return 'http://indavideo.hu/video/%s' % media_id 

    def get_host_and_id(self, url):
        r = re.search('http://(.+?)/video/([\w]+)', url)
        if r:
            return r.groups()
        else:
            r = re.search('//(.+?)/([\w]+)', url)
            if r:
                return r.groups()
            else:
                return False

    def valid_url(self, url, host):
        return (re.match('http://(www.)?indavideo.hu/' +
                         '[0-9A-Za-z]+', url) or
                         'indavideo' in host)
