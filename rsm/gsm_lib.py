#/usr/bin/env python

"""
gsm_lib.py

    Stores a collection of utility functions used by
        generate_subject_map.py and generate_subject_map_input.py
"""

__author__      = "CTS-IT team"
__copyright__   = "Copyright 2014, University of Florida"
__license__     = "BSD 3-Clause"
__version__     = "0.1"

import datetime
import tempfile
import logging
import os
from lxml import etree
from rsm.utils import SimpleConfigParser

# This addresses the issues with relative paths
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'

# Initialize a Logger for this module
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


'''
Sort element tree based on three given indices.

Keyword argument: data
sorting is based on study_id, form name, then timestamp, ascending order
'''
def sort_element_tree(data):
    # this element holds the subjects that are being sorted
    container = data.getroot()
    container[:] = sorted(container, key=getkey)


'''
Helper function for sorting. Returns keys to sort on.

Keyword argument: elem
returns the corresponding tuple study_id, form_name, timestamp
'''
def getkey(elem):
    research_subject_id = elem.findtext("research_subject_id")
    yob = elem.findtext("yob")
    return (research_subject_id,yob)


'''
Write ElementTree to a file
    takes file_name as input
'''
def write_element_tree_to_file(element_tree, file_name):
    #gsmlogger.logger.debug('Writing ElementTree to %s', file_name)
    element_tree.write(file_name, encoding="us-ascii", xml_declaration=True,method="xml")


class ConfigurationError(Exception):
    pass


def get_settings(config_file):
    '''
    TODO: call validate_settings
    '''
    settings = SimpleConfigParser.SimpleConfigParser()
    settings.read(config_file)
    settings.set_attributes()
    return settings

def read_config(configuration_directory, conf_file, settings):
    '''
    Read the config data from settings.ini
    @TODO: Rename to `validate_settings` and make more generic.
        Currently the function needs the settings file name to validate the settings
    '''

    # check if the path is valid
    if not os.path.exists(conf_file):
        message = "Cannot find settings file: " + conf_file
        logger.error(message)
        raise ConfigurationError(message)

    # test for required parameters
    required_parameters = ['source_data_schema_file', 'site_catalog']

    for parameter in required_parameters:
        if not settings.hasoption(parameter):
            message = "read_config: required parameter, \'{0}\', is missing " \
                      "in {1}. Please set it with appropriate value. For " \
                      "assistance refer settings.ini in config-example folder." \
                      "\nProgram will now \nterminate...".format(parameter, conf_file)
            logger.error(message)
            raise ConfigurationError(message)
        elif settings.getoption(parameter) == "":
            message = "read_config: required parameter, \'{0}\', is not set " \
                      "in {1}. Please set it with appropriate value. For " \
                      "assistance refer settings.ini in config-example folder." \
                      "\nProgram will now terminate...".format(parameter, conf_file)
            logger.error(message)
            raise ConfigurationError(message)

    # test for required files but only for the parameters that are set
    files = ['source_data_schema_file', 'site_catalog']
    for item in files:
        if settings.hasoption(item) and not os.path.exists(
                os.path.join(configuration_directory, settings.getoption(item))):
            message = "read_config: {0} file, '{1}', specified in {2} does not " \
                      "exist. Please make sure this file is included in {3}. " \
                      "For assistance refer settings.ini in config-example folder." \
                      "\nProgram will now terminate..."\
                .format(item, settings.getoption(item), conf_file, configuration_directory)
            logger.error(message)
            raise ConfigurationError(message)


'''
Helper function for parsing undefined strings
'''
def handle_blanks(s):
    return '' if s is None else s.strip()


'''
Create a folder name with the following format:
    ./out/out_YYYY_mm_dd:00:11:22
'''
def create_temp_dir_debug(existing_folder = './out') :
    prefix = 'out_' + datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
    mydir = existing_folder + '/' + prefix
    os.mkdir(mydir)
    return mydir

'''
If do_keep_gen_files = True
    create a path like './out/out_YYYY_mm_dd:00:11:22'
else
    create a path using system provided location for a file
'''
def get_temp_path(do_keep_gen_files) :
    if do_keep_gen_files :
        return create_temp_dir_debug('.') + '/'
    else :
        return tempfile.mkdtemp('/')


"""
    Returns a tuple comprising hostname and port number from raw text
    Example:
        From raw: sftp.example.com:1234
        Return  : [sftp.example.com, 1234]
"""
def parse_host_and_port(raw) :
    import re
    parse_uri = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
    m = re.search(parse_uri,raw)
    port = m.group('port')
    if not port:
        port = 22
    return [m.group('host'),port]


def get_site_details_as_dict(file_path, site_type):
    """
    Parse and return the details from a site catalog
        file_path: string - path to site catalog XML
        site_type: string - valid values "data_source" or "data_destination"

        return: dictionary - the representation of a site from xml tree
    """
    valid_site_types = ['data_source', 'data_destination']
    assert site_type in valid_site_types

    data = {}
    try:
        sites_list = etree.parse(file_path)
    except IOError:
        logger.exception("Could not open XML file at: " + file_path)
        raise

    site = sites_list.xpath("(/sites_list/site[@type='" + site_type + "'])[1]")[0]
    data['site_URI']            = handle_blanks( site.findtext('site_URI') )
    data['site_uname']          = handle_blanks( site.findtext('site_uname') )
    data['site_password']       = site.findtext('site_password').strip()
    data['site_remotepath']     = handle_blanks( site.findtext('site_remotepath') )
    data['site_contact_email']  = handle_blanks( site.findtext('site_contact_email') )
    data['site_key_path']       = handle_blanks( site.findtext('site_key_path') )

    return data


def makedirs(path):
    """Like os.makedirs() but suppresses error if path already exists."""
    try:
        os.makedirs(path)
    except os.error:
        if not os.path.exists(path):
            raise


