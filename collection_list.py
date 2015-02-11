#!/usr/bin/env python
import os
import sys
import pycurl
import base64
import pprint
import json
from Common import getConfig
from CurlCallback import Test

cfg = getConfig( os.path.dirname(os.path.abspath(__file__)) + '/etc/config.ini' )

#sys.stderr.write("Testing %s\n" % pycurl.version)
accept_frsp      = 'application/json'
auth             = 'Authorization: Basic %s' % base64.b64encode("%s:%s" % (cfg.get('iRODS','username'), cfg.get('iRODS','password')))
base_url         = cfg.get('RESTFUL','http_endpt')
resource         = 'collection/rdm-tst/donders/dccn'
http_request     = 'GET'

## several listing options
list_child       = True
list_type        = 'both'  ## 'collection', 'data' or 'both' (default: 'both')
params = []
if list_child:
   params.append('listing=True')
if list_type:
   params.append('listType=%s' % list_type)

dest_url = '?'.join([os.path.join(base_url, resource), '&'.join(params)])

print 'sending %s to %s' % (http_request, dest_url)

t = Test()
c = pycurl.Curl()
c.setopt(c.URL, dest_url)
c.setopt(c.HEADERFUNCTION, t.header_callback)
c.setopt(c.WRITEFUNCTION , t.body_callback)
c.setopt(c.CUSTOMREQUEST , http_request)
c.setopt(c.HTTPHEADER    , ['ACCEPT: %s' % accept_frsp, auth])
c.perform()
c.close()

print t.header

print json.dumps( json.loads(t.contents), indent=4, sort_keys=True, separators=(',',':') )
