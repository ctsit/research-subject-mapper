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
    site_catalog_file = proj_root+setup['site_catalog_gsm']
    
    # Initialize Redcap Interface

    properties = redcap_transactions().init_redcap_interface(setup,setup['person_index_uri'], gsmlogger.logger)
    response = redcap_transactions().get_data_from_redcap(properties,setup['gsm_token'], gsmlogger.logger,'Person_Index')
    xml_tree = etree.fromstring(response)

    #XSL Transformation 2: This transformation groups the data based on site_id
    transform_xsl = setup['person_index_transforma_xsl']
    xslt = etree.parse(proj_root+transform_xsl)
    transform = etree.XSLT(xslt)
    person_index_data = transform(xml_tree)

    # # # retrieve smi.xml from the sftp server
    get_smi_and_parse(site_catalog_file)
    smi_path = proj_root+"smi.xml"
    if not os.path.exists(smi_path):
        raise GSMLogger().LogException("Error: smi.xml file not found at\
             "+ proj_root)
    else:
        smi = open(smi_path, 'r')
    smi_data = etree.parse(smi_path)
    sort_element_tree(smi_data)
    sort_element_tree(person_index_data)

    person_index_dict = {}
    for item in person_index_data.iter('item'):
         person_index_dict[item.findtext('research_subject_id')]=[item.findtext('yob'),item.findtext('mrn'),item.findtext('facility_code')]


    subjectmap_root = etree.Element("subject_map_records")
    subjectmap_exceptions_root = etree.Element("subject_map_exception_records")
    for item in smi_data.iter('item'):
        if item.findtext('research_subject_id') in person_index_dict.keys():
            if(person_index_dict[item.findtext('research_subject_id')][0]==item.findtext('yob')):
                mrn = etree.SubElement(item, "mrn")
                mrn.text = person_index_dict[item.findtext('research_subject_id')][1]
                facility_code = etree.SubElement(item, "facility_code")
                facility_code.text = person_index_dict[item.findtext('research_subject_id')][2]
                subjectmap_root.append(item)
            else:
                subjectmap_exceptions_root.append(etree.Element("item"))
                exception_item = subjectmap_exceptions_root[0]
                research_subject_id = etree.SubElement(exception_item, "research_subject_id")
                research_subject_id.text = item.findtext('research_subject_id')
                pi_yob = etree.SubElement(exception_item, "Person_Index_YOB")
                pi_yob.text = person_index_dict[item.findtext('research_subject_id')][0]
                hcvt_yob = etree.SubElement(exception_item, "HCVTarget_YOB")
                hcvt_yob.text = item.findtext('yob')

    transform_xsl = setup['xml2csv_xsl']
    xslt = etree.parse(proj_root+transform_xsl)
    transform = etree.XSLT(xslt)
    subject_map_csv = open("subject_map.csv", "w")
    subject_map_csv.write("%s"%transform(subjectmap_root))
    subject_map_csv.close()
    subject_map_exception_csv = open("subject_map_exceptions.csv", "w")
    subject_map_exception_csv.write("%s"%transform(subjectmap_exceptions_root))
    subject_map_exception_csv.close()
    
 
def sort_element_tree(data):
    """Sort element tree based on three given indices.

    Keyword argument: data
    sorting is based on study_id, form name, then timestamp, ascending order

    """

    # this element holds the subjects that are being sorted
    container = data.getroot()
    container[:] = sorted(container, key=getkey)

def getkey(elem):
    """Helper function for sorting. Returns keys to sort on.

    Keyword argument: elem
    returns the corresponding tuple study_id, form_name, timestamp

    Nicholas

    """
    research_subject_id = elem.findtext("research_subject_id")
    yob = elem.findtext("yob")
    return (research_subject_id,yob)



def get_smi_and_parse(site_catalog_file):
    '''Function to get the smi files from sftp server
    The smi files are picked up according to the details in the site-catalog.xml
    '''
    if not os.path.exists(site_catalog_file):
        raise GSMLogger().LogException("Error: site_catalog xml file not found at \
            file not found at "+ site_catalog_file)
    else:
        catalog = open(site_catalog_file, 'r')
    site_data = etree.parse(site_catalog_file)
    site_num = len(site_data.findall(".//site"))
    gsmlogger.logger.info(str(site_num) + " total subject site entries read into tree.")
    sftp_instance = sftp_transactions()
    '''The reference site code is the current site on which generate_subject_map.py is running
    As we need to get the only smi from the sftp to this site.
    '''
    reference_site_code = setup['current_site_code']
    for site in site_data.iter('site'):
        site_code = site.findtext('site_code')
        if reference_site_code == site_code:
            site_URI = site.findtext('smi_URI')
            site_uname = site.findtext('smi_uname')
            site_password = site.findtext('smi_password')
            site_contact_email = site.findtext('smi_contact_email')
            '''Pick up the smi file from the server and place it in the proj_root
            
            '''
            file_name = 'smi.xml'
            site_remotepath = site.findtext('smi_remotepath')+file_name
            site_localpath = proj_root+file_name
            print 'Retrieving '+site_remotepath+' from '+site_URI
            gsmlogger.logger.info('Retrieving %s from %s', site_remotepath, site_URI)
            print 'Any error will be reported to '+site_contact_email
            gsmlogger.logger.info('Any error will be reported to %s',site_contact_email)
            sftp_instance.get_file_from_uri(site_URI, site_uname, site_password, site_remotepath, site_localpath, site_contact_email)
    catalog.close()
    gsmlogger.logger.info("site catalog XML file closed.")
    pass   
    
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
    required_parameters = ['source_data_schema_file', 'site_catalog_gsm',
                    'system_log_file', 'redcap_uri', 'gsm_token']
    for parameter in required_parameters:
        if not parameter in setup:
            raise GSMLogger().LogException("read_config: required parameter, "
                + parameter  + "', is not set in " + setup_json)

    # test for required files but only for the parameters that are set
    files = ['source_data_schema_file', 'site_catalog_gsm', 'system_log_file']
    for item in files:
        if item in setup:
            if not os.path.exists(proj_root + setup[item]):
                raise GSMLogger().LogException("read_config: " + item + " file, '"
                        + setup[item] + "', specified in "
                        + setup_json + " does not exist")
    return setup
    

if __name__ == "__main__":
    main()