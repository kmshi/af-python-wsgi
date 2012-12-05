#import bottle
#import os

#def application(environ, start_response):
#    data = "Hello World! AppFog Python Support"
#    start_response("200 OK", [
#            ("Content-Type", "text/plain"),
#            ("Content-Length", str(len(data)))
#            ])
#    return iter([data])

from urlparse import urlparse,urlunparse
#import logging
import re
import random
import json
import urllib2

from bottle import route, run, debug, template, request, validate, static_file, error

#will default to follow_redirects
def fetch(url, payload=None):
    return urllib2.urlopen(url,payload)
  


class YoukuVideoID2DownloadUrl:
    def get(self,vid):
            v = "http://v.youku.com/player/getPlayList/VideoIDS/%s/version/5/source/video/password/?ran=%d&n=%d"  % (vid,random.randint(9000,10000), 3)
            resp = fetch(v)            
            jsonobj = json.loads(resp.read())
            
            seed = jsonobj['data'][0]['seed']
            key1 = jsonobj['data'][0]['key1']
            key2 = jsonobj['data'][0]['key2']
            #title = jsonobj['data'][0]['title']
            streamfileids = jsonobj['data'][0]['streamfileids']['flv']
            #flv_segs = jsonobj['data'][0]['segs']['flv']
            streamtype = jsonobj['data'][0]['streamtypes'][0]
            if streamtype == 'flvhd':
                streamtype = 'flv'

            sid = self.get_sid()
            print('key1:'+ key1 + '  key2:'+key2)
            file_id = self.get_file_id(streamfileids, seed)
            key = self.gen_key(key1, key2)
            print('key:'+ key)
            url = "http://f.youku.com/player/getFlvPath/sid/%s/st/%s/fileid/%s?K=%s&myp=null" % (sid,streamtype,file_id,key)
            return url


    def get_sid(self):
        import time
        now = int(time.time())
        i1 = random.randint(1000,1999)
        i2 = random.randint(1000,9999)
        return str(now)+str(i1)+str(i2)
    
    def gen_key(self, key1, key2):
        key = int(key1,16)
        key ^= 0xA55AA5A5
        result = key2 + hex(key)[2:]
        if result.endswith('L'):result = result[0:-1]
        return result

    
    def get_file_id(self, file_id, seed):
        mixed = self.get_file_id_mix_string(seed)
        #logging.info('fileid:'+ file_id)
        ids = file_id.split('*')
        #logging.info(ids)
        real_id = ""
        for myid in ids:
            if myid:
                print(myid)
                real_id += mixed[int(myid)]
        return real_id
    
    def get_file_id_mix_string(self,seed):
        source = list(u"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\\:._-1234567890")
        length = len(source)
        #logging.info('length:'+str(length))
        mixed = []
        i = 0
        while i<length:
            seed = (seed * 211 + 30031) % 65536
            index = int(float(seed) / 65536 * len(source))
            mixed.append(source.pop(index))            
            i = i+1  
        return mixed


@route('/hello/:name')
def index(name='World'):
    youku = YoukuVideoID2DownloadUrl()
    print(youku.get("XMjU3MzIxOTk2"));
    return template('<b>Hello {{name}}</b>!', name=name)

@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'

@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'

# only needed when you run Bottle on mod_wsgi
from bottle import default_app
application = default_app()

