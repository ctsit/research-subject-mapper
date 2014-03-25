#/usr/bin/env python
"""

generate_subject_map_input.py -  Tool to generate patient-to-research subject mapping files based on inputs from REDCap projects 

"""
# Version 0.1 2013-11-18
__authors__ = "Mohan Das Katragadda"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause"
__version__ = "0.1"
__email__ = "mohan88@ufl.edu"
__status__ = "Development"
from lxml import etree
import logging
from lxml import etree
import httplib
from urllib import urlencode
import os
import sys

# This addresses the issues with relative paths
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'
sys.path.insert(0, proj_root+'bin/utils/')
from sftp_transactions import sftp_transactions

def main():
    # Configure logging
    configure_logging()
    
    setup_json = proj_root+'config/setup.json'
    global setup
    setup = read_config(setup_json)
    site_catalog_file = proj_root+setup['site_catalog_file']
    # Initialize Redcap Interface

    properties = init_redcap_interface(setup)
    transform_xsl = setup['transform_xsl']
    response = get_data_from_redcap(properties,setup['token'])
    xml_tree = etree.fromstring(response)
    xslt = etree.parse(transform_xsl)
    transform = etree.XSLT(xslt)
    xml_transformed = transform(xml_tree)
    xml_str = etree.tostring(xml_transformed, method='xml', pretty_print=True)
    # xml_str2 = etree.tostring(xml_tree, method='xml', pretty_print=True)
    print xml_str

    transform2_xsl = setup['transform2_xsl']
    xslt = etree.parse(transform2_xsl)
    transform = etree.XSLT(xslt)
    xml_transformed2 = transform(xml_transformed)
    xml_str2 = etree.tostring(xml_transformed2, method='xml', pretty_print=True)


    print xml_str2
    parse_site_details_and_send(site_catalog_file)
    #print response

def parse_site_details_and_send(site_catalog_file):
    '''Function to parse the site details from site catalog'''
    catalog_dict = {}
    if not os.path.exists(site_catalog_file):
        raise LogException("Error: site_catalog xml file not found at \
            file not found at "+ site_catalog_file)
    else:
        catalog = open(site_catalog_file, 'r')
    site_data = etree.parse(site_catalog_file)
    site_num = len(site_data.findall(".//site"))
    logger.info(str(site_num) + " total subject site entries read into tree.")
    sftp_instance = sftp_transactions()
    for site in site_data.iter('site'):
        site_URI = site.findtext('site_URI')
        site_uname = site.findtext('site_uname')
        site_password = site.findtext('site_password')
        site_remotepath = site.findtext('site_remotepath')
        site_contact_email = site.findtext('site_contact_email')
        '''TODO:
        currently sending a readme doc for testing purposes. replace it with the correct xml file.
        '''
        site_localpath = proj_root+'doc/README_DOC'
        sftp_instance.send_file_to_uri(site_URI, site_uname, site_password, site_remotepath, site_localpath, site_contact_email)
    catalog.close()
    logger.info("site catalog XML file closed.")
    pass

    
def init_redcap_interface(setup):
    '''This function initializes the variables requrired to get data from redcap
        interface. This reads the data from the setup.json and fills the dict
        with required properties.
        Mohan'''
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

def get_data_from_redcap(properties,token, format_param='xml',
        type_param='flat', return_format='xml'):
    '''This function gets data from redcap using POST method

    '''
    logger.info('getting data from redcap')
    params = {}
    if token != '':
        params['token'] = token
    else:
        params['token'] = properties['token']
    params['content'] = 'record'
    params['format'] = format_param
    params['type'] = type_param
    params['returnFormat'] = return_format
    params['fields'] = 'dm_usubjid,dm_rfstdtc,eot_dsstdtc,dm_brthyr'
    if properties['is_secure'] is True:
        redcap_connection = httplib.HTTPSConnection(properties['host'])
    else:
        redcap_connection = httplib.HTTPConnection(properties['host'])
    logger.debug('getting data from path : %s', properties['path'])
    redcap_connection.request('POST', properties['path'], urlencode(params),
        {'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/plain'})
    response_buffer = redcap_connection.getresponse()
    returned = response_buffer.read()
    logger.info('***********RESPONSE RECEIVED FROM REDCAP***********')
    logger.debug(returned)
    redcap_connection.close()
    return returned
    
def read_config(setup_json):
    """function to read the config data from setup.json
        Philip

    """
    import json

    try:
        json_data = open(setup_json)
    except IOError:
        #raise logger.error
        print "file " + setup_json + " could not be opened"
        raise

    setup = json.load(json_data)
    json_data.close()

    # test for required parameters
    required_parameters = ['source_data_schema_file', 'site_catalog_file',
                    'system_log_file', 'redcap_uri', 'token']
    for parameter in required_parameters:
        if not parameter in setup:
            raise LogException("read_config: required parameter, '"
            + parameter  + "', is not set in " + setup_json)

    # test for required files but only for the parameters that are set
    files = ['source_data_schema_file', 'site_catalog_file', 'system_log_file']
    for item in files:
        if item in setup:
            if not os.path.exists(proj_root + setup[item]):
                raise LogException("read_config: " + item + " file, '"
                        + setup[item] + "', specified in "
                        + setup_json + " does not exist")
    return setup
    
def send_report(sender,receiver,body):
    '''
    Function to email the report of the get_data_from_redcap to site contact.
    mohan
    '''
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "Email from Research Subject Mapper"
    msg.attach(MIMEText(body, 'html'))
    
    """
    Sending email

    """
    
    try:
       smtpObj = smtplib.SMTP('smtp.ufl.edu',25)
       smtpObj.sendmail(sender, receiver, msg.as_string())
       print "Successfully sent email"
    except Exception:
        print "Error: unable to send email"

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