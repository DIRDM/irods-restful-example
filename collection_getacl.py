#!/usr/bin/env python
from argparse import ArgumentParser
import os
import pycurl
import base64
import json

from Common import getConfig, getTemporaryPassword
from CurlCallback import Test


if __name__ == "__main__":
    cfg = getConfig( os.path.dirname(os.path.abspath(__file__)) + '/etc/config.ini' )

    parg = ArgumentParser(description='get ACL of iRODS collections')

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
                      choices = ['di'],
                      default = 'di',
                      help    = 'specify the institute')

    parg.add_argument('-u','--user',
                      action  = 'store',
                      dest    = 'user',
                      default = '',
                      help    = 'connect with specified iRODS account')

    args = parg.parse_args()

    accept_frsp  = 'application/json'
    base_url     = cfg.get('RESTFUL','http_endpt')
    http_request = 'GET'

    for c in args.collection:

        if args.user:
            passwd = getTemporaryPassword(args.user)
            auth = 'Authorization: Basic %s' % base64.b64encode("%s:%s" % (args.user, passwd))
        else:
            auth = 'Authorization: Basic %s' % base64.b64encode("%s:%s" % (cfg.get('iRODS','username'), cfg.get('iRODS','password')))

        resource = 'collection/rdm-tst/%s/%s/%s/acl' % (args.institute, args.centre, c)

        ## several listing options
        params = []

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
