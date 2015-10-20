import logging
import httplib
from urllib import urlencode
import os
import sys
from lxml import etree
# This addresses the issues with relative paths
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../../")
proj_root = os.path.abspath(goal_dir)+'/'
sys.path.insert(0, proj_root+'rsm')


class redcap_transactions:
    """A class for getting data from redcap instace"""
    def __init__(self):
        self.data = []
        self.configuration_directory = ''

    def init_redcap_interface(self,settings,logger):
        '''This function initializes the variables requrired to get data from redcap
        interface. This reads the data from the settings.ini and fills the dict
        with required properties.
        Mohan'''
        logger.info('Initializing redcap interface')
        host = ''
        path = ''
        source_data_schema_file = ''
        source_data_schema_file = self.configuration_directory + '/' + settings.source_data_schema_file

        if not os.path.exists(source_data_schema_file):
            raise Exception("Error: source_data_schema.xml file not found at\
             "+ source_data_schema_file)
        else:
            source = open(source_data_schema_file, 'r')

        source_data = etree.parse(source_data_schema_file)
        redcap_uri = source_data.find('redcap_uri').text
        token = source_data.find('apitoken').text
        fields = ','.join(field.text for field in source_data.iter('field'))
        if redcap_uri is None:
            host = '127.0.0.1:8998'
            path = '/redcap/api/'
        if token is None:
            token = '4CE405878D219CFA5D3ADF7F9AB4E8ED'

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
                                'token': token, "fields" : fields}

        logger.info("redcap interface initialzed")
        return properties

    def get_data_from_redcap(self, properties,logger, format_param='xml',
            type_param='flat', return_format='xml'):
        '''This function gets data from redcap using POST method
        for getting person index data formtype='Person_Index' must be passed as argument
        for getting redcap data formtype='RedCap' must be passed as argument

        '''
        logger.info('getting data from redcap')
        params = {}
        params['token'] = properties['token']
        params['content'] = 'record'
        params['format'] = format_param
        params['type'] = type_param
        params['returnFormat'] = return_format
        params['fields'] = properties['fields']

        if properties['is_secure'] is True:
            redcap_connection = httplib.HTTPSConnection(properties['host'])
        else:
            redcap_connection = httplib.HTTPConnection(properties['host'])
        redcap_connection.request('POST', properties['path'], urlencode(params),
            {'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain'})
        response_buffer = redcap_connection.getresponse()
        returned = response_buffer.read()
        logger.info('***********RESPONSE RECEIVED FROM REDCAP***********')
        redcap_connection.close()
        return returned
