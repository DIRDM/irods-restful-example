import ConfigParser
import base64
import getpass
import json
import os
import sys
import pycurl
from CurlCallback import Test

def getConfig(config_file='config.ini'):
    '''
    read and parse the config.ini file
    '''

    default_cfg = {
        'irods_username' : 'irods',
        'irods_password' : '',
    }

    config = ConfigParser.SafeConfigParser(default_cfg)
    config.read(config_file)

    return config

def getPassword():

    ## try ask for password from the interactive shell
    if sys.stdin.isatty(): ## for interactive password typing
        passwd = getpass.getpass('password: ')
    else: ## for pipeing-in password
        print 'password: '
        passwd = sys.stdin.readline().rstrip()

    return passwd

def getTemporaryPassword(username):
    '''
    gets one-time temporary password for the iRODS user
    :param username: the iRODS username
    :return: the temporary password
    '''

    cfg = getConfig( os.path.dirname(os.path.abspath(__file__)) + '/etc/config.ini' )

    accept_frsp  = 'application/json'
    auth         = 'Authorization: Basic %s' % base64.b64encode("%s:%s" % (cfg.get('iRODS','username'), cfg.get('iRODS','password')))
    base_url     = cfg.get('RESTFUL','http_endpt')
    resource     = 'user/%s/temppassword' % (username)
    http_request = 'PUT'

    params = ['admin=True']
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

    return json.loads(t.contents)['temporaryPassword']['password']