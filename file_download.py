#!/usr/bin/env python
from argparse import ArgumentParser
import os
import pycurl
import base64
import json

from Common import getConfig, getPassword, getTemporaryPassword
from CurlCallback import FileContent

if __name__ == "__main__":

    cfg = getConfig( os.path.dirname(os.path.abspath(__file__)) + '/etc/config.ini' )

    parg = ArgumentParser(description='upload file to iRODS')

    ## positional arguments
    parg.add_argument('collection',
                      metavar = 'collection',
                      nargs   = 1,
                      help    = 'the collection')

    ## required arguments
    parg.add_argument('-p', '--path',
                      action  = 'store',
                      dest    = 'path',
                      required= True,
                      help    = 'specify the path of the file within the collection to download')

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

    accept_frsp      = 'application/json'
    base_url         = cfg.get('RESTFUL','http_endpt')
    remote_fpath     = 'rdm-tst/%s/%s/%s/%s' % (args.institute, args.centre, args.collection[0], args.path)
    resource         = 'fileContents/%s' % remote_fpath
    http_request     = 'GET'

    dest_url = os.path.join(base_url, resource)

    # start downloading
    fpath_local = os.path.basename(remote_fpath)

    print 'downloading %s to %s ...' % (dest_url, fpath_local)

    t = FileContent(mode='download', fpath_local=fpath_local)

    c = pycurl.Curl()
    c.setopt(c.URL, dest_url)
    c.setopt(c.CUSTOMREQUEST , http_request)
    c.setopt(c.HEADERFUNCTION, t.header_callback)
    c.setopt(c.WRITEFUNCTION, t.write_callback)
    c.setopt(c.NOPROGRESS, 0)
    c.setopt(c.PROGRESSFUNCTION, t.progress_callback)
    c.setopt(c.HTTPHEADER, [auth])
    c.perform()
    http_code = c.getinfo(c.HTTP_CODE)
    c.close()

    # close the downloading, this is essentially close the file descriptor
    t.close()

    # check the http code 
    if http_code not in ['200']:
        if os.path.exists(fpath_local):
            os.unlink(fpath_local)
            print t.header
    else:
        # check if local file size is the same as the content-length
        if t.content_length != os.path.getsize(fpath_local):
            print 'download file %s not OK' % fpath_local
        else:
            print 'download file %s OK' % fpath_local
