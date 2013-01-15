"""
    muchshare urlresolver plugin
    Copyright (C) 2013 Bagira

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from t0mm0.common.net import Net
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay.interfaces import PluginSettings
from urlresolver.plugnplay import Plugin
import urllib2
from urlresolver import common

# Custom imports
import re
from lib import jsunpack

class MuchshareResolver(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "muchshare"

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()
        self.resolver_host = "muchshare.net"

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)


        """ Human Verification """
        html = self.net.http_GET(web_url + "?play=1", headers = {'Referer': web_url}).content

        """ Parsing HTML """
        sPattern = "<div id=\"player_code\">.*?<script type='text/javascript'>eval.*?return p}\((.*?)</script>"
        r = re.search(sPattern, html, re.DOTALL + re.IGNORECASE)
        if r:
            sJavascript = r.group(1)
            sUnpacked = jsunpack.unpack(sJavascript)
            #sPattern = '\'file\',\'([^\']+?)\''
            sPattern = '<param name="src"0="(.*?)"'
            r = re.search(sPattern, sUnpacked)
            if r:
                return r.group(1)
            else:
                common.addon.log_error(self.name + ": no video url found in %s" % sUnpacked)
        else:
            common.addon.log_error(self.name + ': no javascript pattern found')
        return False


    def get_url(self, host, media_id):
        return 'http://' + self.resolver_host + '/embed-%s.html' % media_id

    def get_host_and_id(self, url):
        r = re.search('//(.+?)/embed-([0-9a-z]+)\.html', url)
        if r:
            return r.groups()
        else:
            return False

    def valid_url(self, url, host):
        return re.match('http://(www.)?muchshare.net/embed-([0-9a-z]+)', url, re.IGNORECASE) or self.name in host

