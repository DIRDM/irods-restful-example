#!/usr/bin/env python
from argparse import ArgumentParser
import os
import pycurl
import base64
import json

from Common import getConfig
from CurlCallback import Test


###########################################################################################
# Note this script is created via reverse-engineering the following java codes in iRODS-rest
#  - src/test/java/org/irods/jargon/rest/commands/user/UserServiceTest.java
#  - src/main/java/org/irods/jargon/rest/commands/user/UserAddByAdminRequest.java
#
# as the documentation is missing for this part of operation. The interface may be changed
# in the future.  Always consult the latest documentation for an update
###########################################################################################
if __name__ == "__main__":
    cfg = getConfig( os.path.dirname(os.path.abspath(__file__)) + '/etc/config.ini' )

    parg = ArgumentParser(description='get iRODS account information')

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
        http_request     = 'GET'

        ## several listing options
        params = []
        dest_url = '?'.join([os.path.join(base_url, resource), '&'.join(params)])

        print 'getting account info: %s' % a
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
