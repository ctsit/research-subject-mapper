#/usr/bin/env python
"""

generate_subject_map_input.py -  Tool to generate patient-to-research
subject mapping files based on inputs from REDCap projects

"""
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

import pprint
import os
import sys
import datetime
from datetime import date, timedelta
import argparse
import gsm_lib

# This addresses the issues with relative paths
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'

from utils.sftpclient import SFTPClient
from utils.redcap_transactions import redcap_transactions
from utils.GSMLogger import GSMLogger
import SimpleConfigParser

# Command line default argument values
default_configuration_directory = proj_root + "config/"
default_do_keep_gen_files = None

# Defaults for optional settings.ini parameters
DEFAULT_LOG_FILE = "gsmi_log/gsmi.log"

def main():
    global configuration_directory
    global do_keep_gen_files
    global tmp_folder

    # obtaining command line arguments for path to config directory
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', dest='configuration_directory_path',
        default=default_configuration_directory,
        required=False,
        help='Specify the path to the configuration directory')

    # read the optional argument `-k` for keeping the generated files
    parser.add_argument(
        '-k', '--keep',
        default=default_do_keep_gen_files,
        required=False,
        help = 'Specify `yes` to preserve the files generated during execution')


    args = vars(parser.parse_args())
    configuration_directory = args['configuration_directory_path'] + '/'
    do_keep_gen_files       = False if args['keep'] is None else True

    settings = SimpleConfigParser.SimpleConfigParser()
    settings.read(configuration_directory + 'settings.ini')
    settings.set_attributes()
    gsm_lib.read_config(configuration_directory, 'settings.ini', settings)
    site_catalog_file = configuration_directory+settings.site_catalog

    if not settings.hasoption('system_log_file') or \
    settings.system_log_file == "":
        system_log_file = DEFAULT_LOG_FILE
    else:
        system_log_file = settings.system_log_file

    # Configure logging
    global gsmlogger
    gsmlogger = GSMLogger()
    gsmlogger.configure_logging(system_log_file)

    # Check if xml_formatting_transform.xsl file is present/properly set in
    # setting.ini
    message2 = "Please set it with appropriate value and restart execution. \
For assistance refer config-example-gsm-input/settings.ini.\
 \nProgram will now terminate..."
    if not settings.hasoption('xml_formatting_tranform_xsl'):
        message = "Required parameter xml_formatting_tranform_xsl is missing \
in settings.ini. " + message2
        print message
        gsmlogger.LogException(message)
        sys.exit()
    elif settings.xml_formatting_tranform_xsl == "":
        message = "Required parameter xml_formatting_tranform_xsl does not \
have a value in settings.ini. " + message2
        print message
        gsmlogger.LogException(message)
        sys.exit()
    elif not os.path.exists(configuration_directory + \
        settings.xml_formatting_tranform_xsl):
        message = "Required file xml_formatting_tranform.xsl does not exist \
in " + configuration_directory + ". Please make sure this file is included in \
the configuration directory and restart execution. For assistance refer \
config-example-gsm-input/xml_formatting_tranform.xsl.\
 \nProgram will now terminate..."
        print message
        gsmlogger.LogException(message)
        sys.exit()

    # Initialize Redcap Interface
    rt = redcap_transactions()
    rt.configuration_directory = configuration_directory

    properties = rt.init_redcap_interface(settings, gsmlogger.logger)
    transform_xsl = configuration_directory + settings.xml_formatting_tranform_xsl
    #get data from the redcap for the fields listed in the source_data_schema.xml
    response = rt.get_data_from_redcap(properties, gsmlogger.logger)

    #XSL Transformation 1: This transformation removes junk data, rename elements and extracts site_id and adds new tag site_id
    xml_tree = etree.fromstring(response)
    xslt = etree.parse(transform_xsl)
    transform = etree.XSLT(xslt)
    xml_transformed = transform(xml_tree)
    xml_str = etree.tostring(xml_transformed, method='xml', pretty_print=True)

    #XSL Transformation 2: This transformation groups the data based on site_id
    transform2_xsl = proj_root + 'bin/utils/groupby_siteid_transform.xsl'
    xslt = etree.parse(transform2_xsl)
    transform = etree.XSLT(xslt)
    xml_transformed2 = transform(xml_transformed)

    #XSL Transformation 3: This transformation removes all the nodes which are not set
    transform3_xsl = proj_root + 'bin/utils/remove_junktags_transform.xsl'
    xslt = etree.parse(transform3_xsl)
    transform = etree.XSLT(xslt)
    xml_transformed3 = transform(xml_transformed2)

    #Prettifying the output generated by XSL Transformation
    xml_str2 = etree.tostring(xml_transformed3, method='xml', pretty_print=True)
    tree = etree.fromstring(xml_str2, etree.XMLParser(remove_blank_text=True))

    # Loop through the start_date elements and update theur values
    for k in tree.iter('start_date'):
        d = datetime.datetime.strptime(k.text, "%Y-%m-%d").date()-timedelta(days=180)
        k.text = str(d)

    #writing data to smi+site_id.xml. This xml will be saved to sftp of the site as smi.xml
    smi_filenames = []
    smi_ids = []
    tmp_folder = gsm_lib.get_temp_path(do_keep_gen_files)

    for k in tree:
        file_name = tmp_folder + 'smi' + k.attrib['id']+'.xml'
        gsm_lib.write_element_tree_to_file(ET.ElementTree(k), file_name)
        smi_filenames.append(file_name)
        smi_ids.append(k.attrib['id'])

    print 'Using smi_filenames: '
    pprint.pprint(smi_filenames)
    parse_site_details_and_send(site_catalog_file, smi_filenames, smi_ids, gsmlogger, settings)


'''
Parses the site details from site catalog

Note: uses files generated by `write_element_tree_to_file`
in the main function.
'''
def parse_site_details_and_send(site_catalog_file, smi_filenames, smi_ids, gsmlogger, settings):
    for smi_file_name in smi_filenames:
        if not os.path.exists(smi_file_name):
            raise GSMLogger().LogException("Error: smi file "+smi_file_name+" not found")

    if not os.path.exists(site_catalog_file):
        raise GSMLogger().LogException("Error: site_catalog xml file not found at "
                + site_catalog_file)
        r2
    else:
        catalog = open(site_catalog_file, 'r')

    site_data = etree.parse(site_catalog_file)
    site_num = len(site_data.findall(".//site"))
    gsmlogger.logger.info(str(site_num) + " total subject site entries read into tree.")

    for site in site_data.iter('site'):
        site_code = site.findtext('site_code')
        if site_code in smi_ids:
            host, port = gsm_lib.parse_host_and_port(site.findtext('site_URI'))
            site_uname = site.findtext('site_uname')
            site_key_path = site.findtext('site_key_path')
            site_password = site.findtext('site_password')
            site_contact_email = site.findtext('site_contact_email')
            sender_email = settings.sender_email

            '''Pick up the correct smi file with the code and place in the destination
            as smi.xml at the specified remote path
            '''
            file_name = 'smi'+site_code+'.xml'
            site_remotepath = site.findtext('site_remotepath')

            site_localpath = tmp_folder + file_name

            info = '\nSending '+site_localpath+' to '+host+':'+site_remotepath
            print info
            gsmlogger.logger.info(info)

            info = 'Any error will be reported to '+site_contact_email
            print info
            gsmlogger.logger.info(info)

            sftp_instance = SFTPClient(host, sender_email, port, site_uname, site_password,
                                       private_key=site_key_path)
            sftp_instance.send_file_to_uri(site_remotepath, 'smi.xml',
                                           site_localpath, site_contact_email)

            if do_keep_gen_files:
                print ' * Keeping the temporary file: ' + site_localpath
            else :
                # remove the smi.xml from the folder
                try:
                    print ' * Removing the temporary file: ' + site_localpath
                    os.remove(site_localpath)
                except OSError:
                    pass
        else:
            print 'Site code '+site_code+' does not exist'
            gsmlogger.logger.info('Site code does not exist')
    catalog.close()
    gsmlogger.logger.info("site catalog XML file closed.")
    pass


if __name__ == "__main__":
    main()
