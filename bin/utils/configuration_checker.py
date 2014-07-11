#!/usr/bin/env python
"""

configuration_checker.py - Standalone python script to check for configuration settings for Research_Subject_mapper and REDI Projects

This script serves as a tool to validate the settings made in the settings.ini for the above projects. 

User of this script can run this script to provide configuration settings in an interactive way.

For details on how to use this tool run 'python configuration_checker.py --help' from the command line.


TODO:
Required fields and files for gsm, gsmi and redi are set in lists below import statements. If you stumble upon any required field or file, which isn't 
in the lists, please add them to the list before using this script.

"""
__author__ = "Mohan Katragadda"
__copyright__ = "Copyright 2013, University of Florida"
__license__ = "BSD 2-Clause"
__version__ = "0.1"
__email__ = "mohan88@ufl.edu"
__status__ = "Development"

import argparse
import SimpleConfigParser as SimpleConfigParser
from redcap import Project, RedcapError
import os
import re
import logging
import sys
logging.getLogger().setLevel(logging.getLevelName('INFO'))
    
GSM_REQ_FIELDS = ['smtp_host_for_outbound_mail','system_log_file','send_email','receiver_email','redcap_uri','token']
GSM_REQ_FILES = ['source_data_schema_file', 'site_catalog']

GSMI_REQ_FIELDS = ['system_log_file']
GSMI_REQ_FILES = ['source_data_schema_file', 'site_catalog','xml_formatting_tranform_xsl']

REDI_REQ_FIELDS = ['smtp_host_for_outbound_mail','system_log_file','send_email','receiver_email','redcap_uri','token']
REDI_REQ_FILES = ['translation_table_file', 'form_events_file','research_id_to_redcap_id','component_to_loinc_code_xml','replace_fields_in_raw_data_xml','raw_xml_file']

EMAIL_REGEX = re.compile('^[-+.\w]{1,64}@[-.\w]{1,64}\.[-.\w]{2,6}$')
URI_REGEX = re.compile('(?:http.*:\/\/)?(?P<host>[^:\/ ]+).?(?P<port>[0-9]*).*')

def get_proj_root():
    file_dir = os.path.dirname(os.path.realpath(__file__))
    proj_root = os.path.abspath(os.path.join(file_dir, "../../")) + '/'
    return proj_root

proj_root = get_proj_root()
default_configuration_directory = proj_root + "config.gsm/"


def main():
    """ script can be executed with filename as parameter, otherwise the
        script itself will be checked """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', dest='configuration_directory_path',
        default=default_configuration_directory,
        required=False,
        help='Specify the path to the configuration directory')

    parser.add_argument(
        '-i', '--interactive_mode',
        default=False,
        action='store_true',
        required=False,
        help='run in interactive mode ')

    parser.add_argument(
        '-r', dest='check_project',
        default='gsm',
        required=False,
        help='Specify the project name to run configuration checker against that project. For redi project provide \'redi\'.\
                For generate_subject_mapper provide \'gsm\' and For generate_subject_mapper_input provide \'gsmi\'. By default this value is taken as \'gsm\'')

    args = vars(parser.parse_args())

    global REQ_FIELDS
    global REQ_FILES
    if args['check_project'] == 'gsm':
        REQ_FIELDS = list(GSM_REQ_FIELDS)
        REQ_FILES = list(GSM_REQ_FILES)
    elif args['check_project'] == 'gsmi':
        REQ_FIELDS = list(GSMI_REQ_FIELDS)
        REQ_FILES = list(GSMI_REQ_FILES)
    elif args['check_project'] == 'redi':
        REQ_FIELDS = list(REDI_REQ_FIELDS)
        REQ_FILES = list(REDI_REQ_FILES)

    if args['configuration_directory_path'] == default_configuration_directory and not args['interactive_mode']:
        print """Running configuration checker against default configuration directory config"""

    settings_dictionary = None
    
    global configuration_directory
    configuration_directory = args['configuration_directory_path'] + '/'

    settings_dictionary = read_settings()

    if args['interactive_mode']:
        settings_dictionary = get_settings_interactively(settings_dictionary)
    else:
        settings_dictionary = validate_settings(settings_dictionary)
    if 'redcap_uri' in settings_dictionary and 'token' in settings_dictionary:
        check_redcap_connection(settings_dictionary['redcap_uri'],settings_dictionary['token'])

def check_redcap_connection(redcap_uri,redcap_token):
    try:
        project = Project(redcap_uri,redcap_token)
        logging.info("Successfully established connection with REDCap instance")
    except RedcapError as e:
        logging.info(e.message)

def read_settings():
    #Reading settings file
    settings = SimpleConfigParser.SimpleConfigParser()
    config_file = configuration_directory + 'settings.ini'
    try:
        settings.read(config_file)
        settings.set_attributes()
    except:
        logging.warning("Unable to read settings.ini at the location provided")
    settings_dictionary = {}
    settings_dict = vars(settings).iteritems()
    for key, value in settings_dict:
        if not key.startswith('_'):
            settings_dictionary[key] = value
    logging.info('Settings.ini file read successfull.')
    return settings_dictionary

#checking for required fields and required files in the settings.ini
def validate_settings(settings_dict):
    config_checker = ConfigurationChecker()
    logging.info("Validating configurations set in settings.ini")
    for key, value in settings_dict.iteritems():
        if key in REQ_FIELDS and key not in REQ_FILES:
            if config_checker.add_required_setting(key,value,required=True):
                logging.info("Found valid value \'"+value+"\' for "+key)
            continue
        if key in REQ_FILES:
            if config_checker.add_req_file_settings(key,value):
                logging.info("Found file \'"+key+"\' at location "+key)
            continue
        config_checker.add_required_setting(key,value)
        logging.info("Setting value "+value+" for \'"+key+"\' ...")
    settings_dictionary = config_checker.settings
    return settings_dictionary

def validate_xmls(xmlfilename, xsdfilename):
    if not os.path.exists(xsdfilename):
        raise LogException("Error: " + xsdfilename + " xsd file not found at "
                           + xsdfilename)
    else:
        xsdfilehandle = open(xsdfilename, 'r')
        logging.info(xmlfilename + " Xsd file read in. ")

    xsd_tree = etree.parse(xsdfilename)
    xsd = etree.XMLSchema(xsd_tree)

    if not os.path.exists(xmlfilename):
        raise LogException("Error: " + xmlfilename + " xml file not found at "
                           + xmlfilename)
    else:
        xmlfilehandle = open(xmlfilename, 'r')
        logging.info(xmlfilename +
                    " XML file read in. " +
                    str(sum(1 for line in xmlfilehandle)) +
                    " total lines in file.")
    if not xsd.validate(xml):
        raise LogException(
            "XSD Validation Failed for xml file %s and xsd file %s",
            xmlfilename,
            xsdfilename)

def get_settings_interactively(settings_dict):
    config_checker = ConfigurationChecker()
    logging.info("Default values are displayed in [] if available. Press Enter to proceed with default values")
    for key in REQ_FIELDS:
        is_valid_value = False
        try:
            value_on_file = settings_dict[key]
            while not is_valid_value:
                value = raw_input("Please enter valid value for "+key+"["+value_on_file+"]:")
                if not value:
                    value = value_on_file
                is_valid_value = config_checker.add_required_setting(key,value,required=True)
                if is_valid_value:
                    logging.info("Value \'"+value+"\' entered for "+key+" is valid")
        except KeyError:
            while not is_valid_value:
                value = raw_input("Please enter valid value for "+key+":")
                is_valid_value = config_checker.add_required_setting(key,value,required=True)
                if is_valid_value:
                    logging.info("Value \'"+value+"\' entered for "+key+" is valid")
    for key in REQ_FILES:
        is_file_found = False
        try:
            value_on_file = settings_dict[key]
            while not is_file_found:
                value = raw_input("Please provide name of the file for "+key+"["+value_on_file+"]:")
                if not value:
                    value = value_on_file
                is_file_found = config_checker.add_req_file_settings(key,value)
                if is_file_found:
                    logging.info("File "+key+" found at \'"+value+"\'")
        except KeyError:
            while not is_file_found:
                value = raw_input("Please provide either Fully-Qualified path or Relative path to the file "+key+":")
                is_file_found = config_checker.add_req_file_settings(key,value,is_full_path=True)
                if is_file_found:
                    logging.info("File "+key+" found at \'"+value+"\'")
    return config_checker.settings

class ConfigurationChecker:
    def __init__(self):
        self.settings = {}
        self.REQ_FIELDS = []
        self.REQ_FILES = [] 

    def add_required_setting(self,setting_key,setting_value,required=False,uri=False):
        #check for value
        if required:
            self.REQ_FIELDS.append(setting_key)
            if not setting_value or setting_value == '':
                logging.warning("Please provide value for "+setting_key+" in settings.ini") 
                return False
        if 'email' in setting_key and setting_key!='send_email' and not EMAIL_REGEX.match(setting_value):
            logging.warning("Please provide a valid email Address for "+ setting_key)
            return False
        if setting_key == 'send_email':
            if setting_value=='Y' or setting_value=='N':
                return True
            else:
                logging.warning("Please provide a Y or N for "+ setting_key)
                return False
        if 'uri' in setting_key and not URI_REGEX.match(setting_value):
            logging.warning("Please provide a valid URI")
            return False
        self.settings[setting_key] = setting_value
        return True

    def add_req_file_settings(self,setting_key,setting_value,is_full_path=False):
        self.REQ_FILES = setting_key
        file_path = setting_value
        if not is_full_path:
            file_path = configuration_directory + setting_value
        if not os.path.exists(file_path):
            logging.warning('File ' + setting_key + ' not found at '+file_path)
            return False
        self.settings[setting_key] = setting_value
        return True

if __name__ == "__main__":
    main()