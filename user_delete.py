#!/usr/bin/env python
from argparse import ArgumentParser
import os
import pycurl
import base64
import json

from Common import getConfig
from CurlCallback import Test


###########################################################################################
# TODO: the user deletion method is not supported yet in the restful interface. This script
#       for the moment is just a place holder.
###########################################################################################
if __name__ == "__main__":
    cfg = getConfig( os.path.dirname(os.path.abspath(__file__)) + '/etc/config.ini' )

    parg = ArgumentParser(description='delete iRODS accounts')

    ## positional arguments
    parg.add_argument('account',
                      metavar = 'account',
                      nargs   = '+',
                      help    = 'iRODS user account')

    args = parg.parse_args()

    for a in args.account:
        accept_frsp      = 'application/json'
        auth             = 'Authorization: Basic %s' % base64.b64encode("%s:%s" % (cfg.get('iRODS','username'), cfg.get('iRODS','password')))
        base_url         = cfg.get('RESTFUL','http_endpt')
        resource         = 'user/%s' % a
        http_request     = 'DELETE'

        ## several listing options
        params = []
        dest_url = '?'.join([os.path.join(base_url, resource), '&'.join(params)])

        print 'deleting user %s' % resource.split('/')[-1]
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