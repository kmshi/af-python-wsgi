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

from bottle import route, run, debug, template, request, validate, static_file, error,redirect

#will default to follow_redirects
def fetch(url, payload=None):
    return urllib2.urlopen(url,payload)
  


class YoukuVideoID2DownloadUrl:
    def get(self,vid):
            v = "http://v.youku.com/player/getPlayList/VideoIDS/%s/version/5/source/video/password/?ran=%d&n=%d"  % (vid,random.randint(9000,10000), 3)
            resp = fetch(v)            
            jsonobj = json.loads(resp.read())
            
            seed = jsonobj['data'][0]['seed']
            streamtype = ''
            key = ''
            streamfileids = ''
            if jsonobj['data'][0]['segs']['mp4']:
                streamtype = 'mp4'
                key = jsonobj['data'][0]['segs']['mp4'][0]['k'] #only get the first segment
                streamfileids = jsonobj['data'][0]['streamfileids']['mp4']
            elif jsonobj['data'][0]['segs']['flv']:
                streamtype = 'flv'
                key = jsonobj['data'][0]['segs']['flv'][0]['k'] #only get the first segment
                streamfileids = jsonobj['data'][0]['streamfileids']['flv']
            else:
                streamtype = 'flvhd'
                key = jsonobj['data'][0]['segs']['flvhd'][0]['k'] #only get the first segment
                streamfileids = jsonobj['data'][0]['streamfileids']['flvhd']
                
            #title = jsonobj['data'][0]['title']

            file_id = self.get_file_id(streamfileids, seed)
            temp = file_id[0:8]+"00"+file_id[10:] #the first segment 16x
            url = "http://f.youku.com/player/getFlvPath/sid/00_00/st/%s/fileid/%s?K=%s" % (streamtype,temp,key)
            return url


    def get_file_id(self, file_id, seed):
        mixed = self.get_file_id_mix_string(seed)
        #logging.info('fileid:'+ file_id)
        ids = file_id.split('*')
        #logging.info(ids)
        real_id = ""
        for myid in ids:
            if myid:
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


@route('/download/:name')
def download(name='XMjU3MzIxOTk2'): #name to be videoid, like XMjU3MzIxOTk2
    youku = YoukuVideoID2DownloadUrl()    
    return template('<a href="{{name}}">Download</a>', name=youku.get(name))

@route('/redirect/:name')
def convert(name='XMjU3MzIxOTk2'): #name to be videoid, like XMjU3MzIxOTk2
    youku = YoukuVideoID2DownloadUrl()    
    redirect(youku.get(name))

@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'

@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'

# only needed when you run Bottle on mod_wsgi
from bottle import default_app
application = default_app()

