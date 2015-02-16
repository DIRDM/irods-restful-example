import ConfigParser
import getpass 
import sys

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
