#/usr/bin/env python
"""

generate_subject_map.py -  Tool to generate patient-to-research subject mapping files based on inputs from REDCap projects 

"""
# Version 0.1 2013-11-18
__authors__ = "Mohan Das Katragadda"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause"
__version__ = "0.1"
__email__ = "mohan88@ufl.edu"
__status__ = "Development"
from lxml import etree
import xml.etree.ElementTree as ET
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
from redcap_transactions import redcap_transactions
from GSMLogger import GSMLogger

def main():
    
    # Configure logging
    global gsmlogger
    gsmlogger = GSMLogger()
    gsmlogger.configure_logging()
    
    setup_json = proj_root+'config/setup.json'
    global setup
    setup = read_config(setup_json)
    site_catalog_file = proj_root+setup['site_catalog_file']
    # Initialize Redcap Interface

    properties = redcap_transactions().init_redcap_interface(setup,setup['person_index_uri'], gsmlogger.logger)
    transform_xsl = setup['xml_formatting_tranform_xsl']
    response = redcap_transactions().get_data_from_redcap(properties,setup['token'], gsmlogger.logger,'Person_Index')
    
    
    
def write_element_tree_to_file(element_tree, file_name):
    '''function to write ElementTree to a file
        takes file_name as input
        Radha

    '''
    gsmlogger.logger.debug('Writing ElementTree to %s', file_name)
    element_tree.write(file_name, encoding="us-ascii", xml_declaration=True,
            method="xml")

        
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
            raise GSMLogger().LogException("read_config: required parameter, '"
            + parameter  + "', is not set in " + setup_json)

    # test for required files but only for the parameters that are set
    files = ['source_data_schema_file', 'site_catalog_file', 'system_log_file']
    for item in files:
        if item in setup:
            if not os.path.exists(proj_root + setup[item]):
                raise GSMLogger().LogException("read_config: " + item + " file, '"
                        + setup[item] + "', specified in "
                        + setup_json + " does not exist")
    return setup
    

if __name__ == "__main__":
    main()