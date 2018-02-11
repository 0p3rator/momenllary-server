import httplib2 as httplib2

import shelve
import os
from xml.sax import make_parser, SAXParseException
from xml.sax.handler import ContentHandler
from time import sleep
import sys, traceback
import socket
import numpy as np
import conf.conf as config

httpCon = httplib2.Http()
httpCon.add_credentials(config.api_username, config.api_password)

# api_host='http://api.openstreetmap.org'
api_host = config.api_host
# api_host = "http://mapeditor.momenta.works"
retryDelays = [0, 10, 60, 300]

def doHttpRequest( message, url, method, data=None, headers=None):
    count = 0
    while count <= len(retryDelays):
        try:
            resp, content = httpCon.request(url, method, data, headers=headers)
            if resp.status == 500 and count < len(retryDelays):
                print '%sError 500, retrying in %u seconds' % (message, retryDelays[count])
                sleep(retryDelays[count])
                count += 1
                continue
            if resp.status != 200:
                print message + str(resp.status) + " " + str(content)
                # exit(-1)
            return (resp, content)
        except socket.error, e:
            if count < len(retryDelays):
                print '%s%s, retrying in %u seconds' % (message, e, retryDelays[count])
                sleep(retryDelays[count])
                count += 1
                continue
            else:
                print message + str(e)
                exit(-1)
#

if __name__ == "__main__":
    node = '''
    <osm>
    <node id="27686" changeset="199" timestamp="2018-01-27T09:19:07Z" version="1" visible="true" user="jingwei" uid="1" lat="39.9859812" lon="116.3691912">
<tag k="ele" v="41.9914326269"/>
<tag k="keypoints" v="(116.369194249 39.9859865238 43.2170695925,116.369188307 39.9859755132 43.228975328,116.369195654 39.9859862218 40.7236200049,116.369186496 39.9859764653 40.7960655823)"/>
<tag k="messageId" v="1517044487-6056"/>
<tag k="momenta" v="board"/>
<tag k="tableInfo" v="boards"/>
<tag k="type" v="RECT"/>
</node>
</osm>'''
    request = doHttpRequest("ada",config.api_host+ config.api_delete_element.format("node", "27686"),"DELETE", data=node)
