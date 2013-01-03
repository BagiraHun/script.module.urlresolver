'''
indavideo urlresolver plugin
Copyright (C) 2012 Bagira

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

# Custom import
import httplib
from pyamf import remoting

class IndavideoResolver(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "indavideo"


    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()

    def get_media_url(self, host, media_id):
        print 'indavideo: in get_media_url %s %s' % (host, media_id)
        web_url = self.get_url(host, media_id)
        html = self.net.http_GET(web_url).content

        match = re.search('vID=([^&]+?)&', html,re.DOTALL)
        if not match:
            print 'could not find video'
            return False
        vID = match.group(1)

        env = remoting.Envelope(amfVersion=3)
        env.bodies.append(
           (  "/1",
              remoting.Request(
                 target="player.playerHandler.getVideoData",
                 body=[vID],
                 envelope=env
              )
           )
        )
        conn = httplib.HTTPConnection("amfphp.indavideo.hu")
        conn.request("POST", "/gateway.php", str(remoting.encode(env).read()),{'content-type': 'application/x-amf'})
        response = conn.getresponse().read()
        response = remoting.decode(response).bodies[0][1].body
        conn.close()
        return response['data']['video_file']


    def get_url(self, host, media_id):
        print 'indavideo: in get_url %s %s' % (host, media_id)
        return 'http://indavideo.hu/video/%s' % media_id 
        
        
    def get_host_and_id(self, url):
        print 'indavideo: in get_host_and_id %s' % (url)

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
