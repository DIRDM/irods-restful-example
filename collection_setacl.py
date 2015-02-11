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
resource         = 'collection/rdm-tst/donders/dccn/dac_00002/acl/dac_00002_manager'
http_request     = 'PUT'

permission       = 'OWN'  ## one of 'READ', 'WRITE' and 'OWN', default is 'READ'
recursive        = True   ## default is False

## several listing options
params = []

if permission:
    params.append('permission=%s' % permission)
if recursive:
    params.append('recursive=true')

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

#print json.dumps( json.loads(t.contents), indent=4, sort_keys=True, separators=(',',':') )

# unfortunately, this function returns nothing, one should check explicitly
# if the new role is implemented
