#!/usr/bin/env python
from argparse import ArgumentParser
import os
import pycurl
import base64

from Common import getConfig
from CurlCallback import Test


if __name__ == "__main__":
    cfg = getConfig( os.path.dirname(os.path.abspath(__file__)) + '/etc/config.ini' )

    parg = ArgumentParser(description='set ACL of iRODS collections')

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

    args = parg.parse_args()


    roleMap = {'manager':'OWN', 'contributor':'WRITE', 'user':'READ'}

    for coll in args.collection:
        for r, acl in roleMap.iteritems():

            accept_frsp      = 'application/json'
            auth             = 'Authorization: Basic %s' % base64.b64encode("%s:%s" % (cfg.get('iRODS','username'), cfg.get('iRODS','password')))
            base_url         = cfg.get('RESTFUL','http_endpt')
            resource         = 'collection/rdm-tst/%s/%s/%s/acl/%s_%s' % (args.institute, args.centre, coll, coll, r)
            http_request     = 'PUT'

            permission       = acl
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