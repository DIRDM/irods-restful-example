#!/usr/bin/env python
from argparse import ArgumentParser
import os
import pycurl
import base64
import json
import re

from Common import getConfig, getTemporaryPassword
from CurlCallback import Test


if __name__ == "__main__":
    cfg = getConfig( os.path.dirname(os.path.abspath(__file__)) + '/etc/config.ini' )

    parg = ArgumentParser(description='delete AVU metadata from iRODS collections')

    ## positional arguments
    parg.add_argument('collection',
                      metavar = 'collection',
                      nargs   = '+',
                      help    = 'list of collections')

    ## optional arguments
    parg.add_argument('-c','--centre',
                      action  = 'store',
                      dest    = 'centre',
                      choices = ['dccn','dcc','dcn'],
                      default = 'dccn',
                      help    = 'specify the centre')

    parg.add_argument('-i','--institute',
                      action  = 'store',
                      dest    = 'institute',
                      choices = ['donders'],
                      default = 'donders',
                      help    = 'specify the institute')

    parg.add_argument('-m','--metadata',
                      action  = 'store',
                      dest    = 'metadata',
                      default = '',
                      help    = 'specify the metadata AVU in comma-separated sets of "key|val|unit"')

    parg.add_argument('-u','--user',
                      action  = 'store',
                      dest    = 'user',
                      default = '',
                      help    = 'connect with specified iRODS account')

    args = parg.parse_args()

    accept_frsp  = 'application/json'
    base_url     = cfg.get('RESTFUL','http_endpt')
    http_request = 'POST'

    for c in args.collection:

        if args.user:
            passwd = getTemporaryPassword(args.user)
            auth = 'Authorization: Basic %s' % base64.b64encode("%s:%s" % (args.user, passwd))
        else:
            auth = 'Authorization: Basic %s' % base64.b64encode("%s:%s" % (cfg.get('iRODS','username'), cfg.get('iRODS','password')))

        resource = 'collection/rdm-tst/%s/%s/%s/metadata' % (args.institute, args.centre, c)

        ## several listing options
        params = []

        dest_url = '?'.join([os.path.join(base_url, resource), '&'.join(params)])

        ## compose the request body
        content_type = 'application/json'
        avu_data = {'metadataEntries': []}
        for avu in re.split(',\s?', args.metadata):
            md = avu.split('|')

            if len(md) < 2:
                print 'ignore set: %s' % avu

            elif len(md) == 2:
                avu_data['metadataEntries'].append({'attribute':md[0], 'value':md[1], 'unit':''})
            else:
                avu_data['metadataEntries'].append({'attribute':md[0], 'value':md[1], 'unit':md[2]})

        print json.dumps(avu_data)

        print 'sending %s to %s' % (http_request, dest_url)

        t = Test()
        c = pycurl.Curl()
        c.setopt(c.URL, dest_url)
        c.setopt(c.HEADERFUNCTION, t.header_callback)
        c.setopt(c.WRITEFUNCTION , t.body_callback)
        c.setopt(c.CUSTOMREQUEST , http_request)
        c.setopt(c.HTTPHEADER    , ['ACCEPT: %s' % accept_frsp, 'Content-Type: %s' % content_type, auth])
        c.setopt(c.POSTFIELDS    , json.dumps(avu_data))
        c.perform()
        c.close()

        print t.header

        print json.dumps( json.loads(t.contents), indent=4, sort_keys=True, separators=(',',':') )
