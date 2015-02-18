#!/usr/bin/env python
from argparse import ArgumentParser
import os
import pycurl
import base64
import json

from Common import getConfig, getPassword, getTemporaryPassword
from CurlCallback import FileContent
#from CurlCallback import Test

if __name__ == "__main__":

    cfg = getConfig( os.path.dirname(os.path.abspath(__file__)) + '/etc/config.ini' )

    parg = ArgumentParser(description='upload file to iRODS')

    ## positional arguments
    parg.add_argument('fpath',
                      metavar = 'fpath',
                      nargs   = 1,
                      help    = 'the local file path')

    parg.add_argument('collection',
                      metavar = 'collection',
                      nargs   = 1,
                      help    = 'the collection')

    ## required arguments
    parg.add_argument('-p', '--path',
                      action  = 'store',
                      dest    = 'path',
                      default = '',
                      help    = 'specify the remote file path within the collection')

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

    parg.add_argument('-u','--user',
                      action  = 'store',
                      dest    = 'user',
                      default = '',
                      help    = 'connect with specified iRODS account')

    args = parg.parse_args()

    if args.user:
        passwd = getTemporaryPassword(args.user)
        auth = 'Authorization: Basic %s' % base64.b64encode("%s:%s" % (args.user, passwd))
    else:
        auth = 'Authorization: Basic %s' % base64.b64encode("%s:%s" % (cfg.get('iRODS','username'), cfg.get('iRODS','password')))

    accept_frsp = 'application/json'
    base_url = cfg.get('RESTFUL','http_endpt')
    remote_fpath = 'rdm-tst/%s/%s/%s' % (args.institute, args.centre, args.collection[0])

    if args.path:
        remote_fpath = '%s/%s' % (remote_fpath, args.path)
    else:
        remote_fpath = '%s/%s' % (remote_fpath, os.path.basename(args.fpath[0]))

    resource         = 'fileContents/%s' % remote_fpath
    http_request     = 'POST'

    dest_url = os.path.join(base_url, resource)

    # start uploading
    print 'uploading %s to %s ...' % (args.fpath[0], dest_url)

    t = FileContent(mode='upload', fpath_local=args.fpath[0])
    #t = Test()

    c = pycurl.Curl()
    c.setopt(c.URL, dest_url)
    c.setopt(c.CUSTOMREQUEST , http_request)
    c.setopt(c.HEADERFUNCTION, t.header_callback)
    c.setopt(c.WRITEFUNCTION , t.body_callback)
    #c.setopt(c.READFUNCTION, t.read_callback)
    c.setopt(c.NOPROGRESS, 0)
    c.setopt(c.PROGRESSFUNCTION, t.progress_callback)
    c.setopt(c.HTTPHEADER, ['ACCEPT: %s' % accept_frsp, auth])

    # preparing form data
    data = [('uploadFile',
            (c.FORM_FILE, args.fpath[0], 
             c.FORM_CONTENTTYPE, 'application/octet-stream'))]

    c.setopt(c.HTTPPOST, data)
    c.perform()
    c.close()

    t.close()

    print t.header

    print json.dumps( json.loads(t.contents), indent=4, sort_keys=True, separators=(',',':') )
