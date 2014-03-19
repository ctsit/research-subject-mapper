#/usr/bin/env python
'''
    generate_subject_map_input.py

'''
import os
import logging

# This addresses the issues with relative paths
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'

def main():
	# Configure logging
    configure_logging()
    logger.info('Logger configured')

    # read setup.json file
    setup_json = proj_root+'config-example/setup.json'

    # store the config data in 'setup'
    setup = read_config(setup_json)
    
    # initialize the properties
    properties = init_properties(setup)

    # send file to specified uri
    data_to_send = "some_sample_data"
    send_file_to_uri(properties, data_to_send)
    pass

def read_config(setup_json):
    import json
    logger.info('reading configuration file')
    try:
        json_data = open(setup_json)
    except IOError:
        #raise logger.error
        print "file " + setup_json + " could not be opened"
        raise

    setup = json.load(json_data)
    json_data.close()

    # test for required parameters
    required_parameters = ['redcap_uri', 'token']
    for parameter in required_parameters:
        if not parameter in setup:
            raise LogException("read_config: required parameter, '"
            + parameter  + "', is not set in " + setup_json)

    logger.info('configuration file reading done')
    return setup

def init_properties(setup):
    '''This function initializes the variables requrired to send data to redcap
        interface. This reads the data from the setup.json and fills the dict
        with required properties.
        
    '''
    logger.info('Initializing redcap interface')
    host = ''
    path = ''

    token = setup['token']
    redcap_uri = setup['redcap_uri']

    if redcap_uri is None:
        host = '127.0.0.1:8998'
        path = '/redcap/api/'
    if token is None:
        token = '4CE405878D219CFA5D3ADF7F9AB4E8ED'

    # parse URI to get host name only and path only
    uri_list = redcap_uri.split('//')
    
    http_str = ''
    if uri_list[0] == 'https:':
        is_secure = True
    else:
        is_secure = False
    after_httpstr_list = uri_list[1].split('/', 1)
    host = http_str + '//' + after_httpstr_list[0]
    host = after_httpstr_list[0]
    path = '/' + after_httpstr_list[1]
    properties = {'host' : host, 'path' : path, "is_secure" : is_secure,
                    'token': token}
    
    logger.info("redcap interface initialzed")
    return properties

def send_file_to_uri(properties, data_to_send, format_param='csv',
        type_param='eav', overwrite_behavior='normal',
        return_format='xml'):
    '''This function sends the file to the specified uri

    '''
    import httplib
    from urllib import urlencode

    logger.info('sending data to redcap')
    params = {}
    params['token'] = properties['token']
    params['content'] = 'record'
    params['format'] = format_param
    params['type'] = type_param
    params['overwriteBehavior'] = overwrite_behavior
    params['data'] = data_to_send
    params['returnFormat'] = return_format

    if properties['is_secure'] is True:
        redcap_connection = httplib.HTTPSConnection(properties['host'])
    else:
        redcap_connection = httplib.HTTPConnection(properties['host'])
    
    logger.debug('data sent to path : %s', properties['path'])
    redcap_connection.request('POST', properties['path'], urlencode(params),
        {'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/plain'})
    logger.info('data sent to redcap')
    response_buffer = redcap_connection.getresponse()
    returned = response_buffer.read()
    
    print '***********RESPONSE RECEIVED FROM REDCAP***********'
    print returned
    logger.info('Response from REDCap : '+returned)
    redcap_connection.close()
    pass

class LogException(Exception):
    '''Class to log the exception
        logs the exception at an error level

    '''
    def __init__(self, *val):
        self.val = val

    def __str__(self):
        logger.error(self.val)
        return repr(self.val)


def configure_logging():
    '''Function to configure logging.

        The log levels are defined below. Currently the log level is
        set to DEBUG. All the logs in this level and above this level
        are displayed. Depending on the maturity of the application
        and release version these levels will be further
        narrowed down to WARNING
        

        Level       Numeric value
        =========================
        CRITICAL        50
        ERROR           40
        WARNING         30
        INFO            20
        DEBUG           10
        NOTSET          0

    '''
    # create logger
    global logger
    logger = logging.getLogger('research_subject_mapper')
    # configuring logger file and log format
    # setting default log level to Debug
    logging.basicConfig(filename=proj_root+'log/rsm.log',
                		format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        filemode='w',
                        level=logging.DEBUG)

if __name__ == "__main__":
    main()