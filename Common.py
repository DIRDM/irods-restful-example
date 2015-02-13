import ConfigParser

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