#/usr/bin/env python
"""

generate_subject_map.py -  Tool to generate patient-to-research
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
import httplib
from urllib import urlencode
import os
import sys
import argparse

import datetime
import gsm_lib

# This addresses the issues with relative paths
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'

from utils.sftpclient import SFTPClient
from sftp_transactions import sftp_transactions
from email_transactions import email_transactions
from redcap_transactions import redcap_transactions
from GSMLogger import GSMLogger
import SimpleConfigParser

# Command line default argument values
default_configuration_directory = proj_root + "config/"
default_do_keep_gen_files = None


'''
Application entry point
@TODO: extract logic into separate functions to reduce size
'''
def main():
    global configuration_directory
    global do_keep_gen_files

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

    # read settings options
    settings = SimpleConfigParser.SimpleConfigParser()
    settings.read(configuration_directory + 'settings.ini')
    settings.set_attributes()
    gsm_lib.read_config(configuration_directory, 'settings.ini', settings)
    site_catalog_file = configuration_directory + settings.site_catalog
    system_log_file = settings.system_log_file

    # Configure logging
    global gsmlogger
    gsmlogger = GSMLogger()
    gsmlogger.configure_logging(system_log_file)

    # Initialize Redcap Interface
    rt = redcap_transactions()
    rt.configuration_directory = configuration_directory

    properties = rt.init_redcap_interface(settings, gsmlogger.logger)
    #gets data from the person index for the fields listed in the source_data_schema.xml
    response = rt.get_data_from_redcap(properties, gsmlogger.logger)
    xml_tree = etree.fromstring(response)

    #XSL Transformation : transforms the person_index data
    transform_xsl = proj_root + "bin/utils/person_index_transform.xsl"
    xslt = etree.parse(transform_xsl)
    transform = etree.XSLT(xslt)
    person_index_data = transform(xml_tree)

    # # # retrieve smi.xml from the sftp server
    smi_path = get_smi_and_parse(site_catalog_file)
    if not os.path.exists(smi_path):
        raise GSMLogger().LogException("Error: file " + smi_path+ " not found")
    else:
        smi = open(smi_path, 'r')
    #Below code merges the 2 xmls
    smi_data = etree.parse(smi_path)
    #sorting both the xml files.
    gsm_lib.sort_element_tree(smi_data)
    gsm_lib.sort_element_tree(person_index_data)
    #generating the person index dictionary
    person_index_dict = {}
    for item in person_index_data.iter('item'):
         person_index_dict[item.findtext('research_subject_id')] = \
         [item.findtext('yob'),item.findtext('mrn'),\
                                       item.findtext('facility_code')]
    #iterate through the smi data and generate a
    # new merged xml's for subject_map and subject_map_exceptions
    subjectmap_root = etree.Element("subject_map_records")
    subjectmap_exceptions_root = etree.Element("subject_map_exception_records")
    exceptions = False
    for item in smi_data.iter('item'):
        if item.findtext('research_subject_id') in person_index_dict.keys():
            gsmlogger.logger.debug("Processing research_subject_id %s", item.findtext('research_subject_id'))
            if(person_index_dict[item.findtext('research_subject_id')][0]==item.findtext('yob')):
                gsmlogger.logger.debug("yob matched for research_subject_id %s", item.findtext('research_subject_id'))
                mrn = etree.SubElement(item, "mrn")
                mrn.text = person_index_dict[item.findtext('research_subject_id')][1]
                facility_code = etree.SubElement(item, "facility_code")
                facility_code.text = person_index_dict[item.findtext('research_subject_id')][2]
                item.remove(item.find('yob'))
                subjectmap_root.append(item)

            else:
                gsmlogger.logger.debug("yob not matched for research_subject_id %s", item.findtext('research_subject_id'))
                exception_item = etree.Element("item")
                research_subject_id = etree.SubElement(exception_item, "research_subject_id")
                research_subject_id.text = item.findtext('research_subject_id')
                if(research_subject_id.text is not None):
                    exceptions = True
                pi_yob = etree.SubElement(exception_item, "Person_Index_YOB")
                pi_yob.text = person_index_dict[item.findtext('research_subject_id')][0]
                hcvt_yob = etree.SubElement(exception_item, "HCVTarget_YOB")
                hcvt_yob.text = item.findtext('yob')
                subjectmap_exceptions_root.append(exception_item)

    #Below code transforms the xml files to csv files
    transform_xsl = proj_root + "bin/utils/xml2csv.xsl"
    xslt = etree.parse(transform_xsl)
    transform = etree.XSLT(xslt)

    tmp_folder = gsm_lib.get_temp_path(do_keep_gen_files)
    subject_map_file = tmp_folder + "subject_map.csv"
    gsmlogger.logger.info('Using path subject map file path: ' + subject_map_file)

    try:
        subject_map_csv = open(subject_map_file, "w")
        subject_map_csv.write("%s"%'"research_subject_id","start_date","end_date","mrn","facility_code"\n')

        for item in subjectmap_root.iter("item"):
            line = '"{0}","{1}","{2}","{3}","{4}"\n'.format(\
                gsm_lib.handle_blanks(item.findtext("research_subject_id")), \
                gsm_lib.handle_blanks(item.findtext("start_date")),\
                gsm_lib.handle_blanks(item.findtext("end_date")),\
                gsm_lib.handle_blanks(item.findtext("mrn")),\
                gsm_lib.handle_blanks(item.findtext("facility_code")))
            subject_map_csv.write("%s"%line)

        subject_map_csv.close()
    except IOError:
        raise GSMLogger().LogException("Could not open file %s for write", subject_map_file)


    # remove the smi.xml from the folder because the XSLT process
    # writes data to smi.xml
    try:
      os.remove(smi_path)
    except OSError:
        raise GSMLogger().LogException("Could not remove file %s ", smi_path)

    # send the subject_map.csv to EMR team (sftp server)
    parse_site_details_and_send(site_catalog_file, subject_map_file, 'sftp', settings)
    if do_keep_gen_files :
        print ' * Keeping the temporary file: ' + subject_map_file
    else :
        print ' * Removing the temporary file: ' + subject_map_file
        os.remove(subject_map_file)


    # send subject_map_exceptions.csv as email attachment
    if exceptions :
        subject_map_exceptions_file = tmp_folder + 'subject_map_exceptions.csv'
        try:
            subject_map_exceptions_csv = open(subject_map_exceptions_file, "w")
        except IOError:
            raise GSMLogger().LogException("Could not open file %s for write", subject_map_exceptions_file)

        subject_map_exceptions_csv.write("%s"%'"research_subject_id","person_index_yob","redcap_yob"\n')
        for item in subjectmap_exceptions_root.iter("item"):
            line = '"{0}","{1}","{2}"\n'.format(\
                    gsm_lib.handle_blanks(item.find("research_subject_id").text), \
                    gsm_lib.handle_blanks(item.find("Person_Index_YOB").text),\
                    gsm_lib.handle_blanks(item.find("HCVTarget_YOB").text))
            subject_map_exceptions_csv.write("%s"%line)
        subject_map_exceptions_csv.close()

        parse_site_details_and_send(site_catalog_file, subject_map_exceptions_file, 'email', settings)
        if do_keep_gen_files :
            print ' * Keeping the temporary file: ' + subject_map_exceptions_file
        else :
            print ' * Removing the temporary file: ' + subject_map_exceptions_file
            os.remove(subject_map_exceptions_file)


'''
Parse the site details from site catalog and
    send the subject map csv to the sftp server
    OR
    email the exceptions file
'''
def parse_site_details_and_send(site_catalog_file, local_file_path, action, settings):
    if not os.path.exists(local_file_path):
        raise GSMLogger().LogException("Error: subject map file "+local_file_path+" file not found")

    if not os.path.exists(site_catalog_file):
        raise GSMLogger().LogException("Error: site_catalog xml file not found at: " + site_catalog_file)

    dikt = gsm_lib.get_site_details_as_dict(site_catalog_file, 'data_destination')
    site_uri = dikt['site_URI']
    host, port = gsm_lib.parse_host_and_port(site_uri)

    site_uname          = dikt['site_uname']
    site_password       = dikt['site_password']
    site_remotepath     = dikt['site_remotepath']
    site_key_path       = dikt['site_key_path']
    site_contact_email  = dikt['site_contact_email']

    # is it a file transfer or attachment email?
    if action == 'sftp':
        # Pick up the subject_map.csv and put it in the specified sftp server's remote path
        info = '\nSending file: [ %s] to host %s:%s %s' % (local_file_path, host, port, site_remotepath)
        print info
        gsmlogger.logger.info(info)

        info = 'Errors will be reported to: ' + site_contact_email
        print info
        gsmlogger.logger.info(info)

        # put the subject map csv file
        remote_directory = site_remotepath.rsplit("/", 1)[0] + "/"
        remote_file_name = site_remotepath.split("/")[-1]

        sftp_instance = SFTPClient(host, port,
                                    site_uname,
                                    site_password,
                                    site_key_path)
        sftp_instance.send_file_to_uri(remote_directory,
                                        remote_file_name,
                                        local_file_path,
                                        site_contact_email)

    elif action == 'email':
        # Send the subject_map_exceptions.csv to the contact email address as an attachment
        info = '\nSending file: [ %s ] as email attachement to: %s' % (local_file_path, site_contact_email)
        gsmlogger.logger.info(info)

        # @TODO change the mail body as required
        mail_body = 'Hi, \n this mail contains attached exceptions.csv file.'
        email_transactions().send_mail(settings.sender_email,
                    site_contact_email, mail_body, [local_file_path])
    else :
        info = 'Invalid option. Either sftp/email should be used.'
        print info
        gsmlogger.logger.warn(info)

    return


def get_smi_and_parse(site_catalog_file):
    '''Function to get the smi files from sftp server
    The smi files are picked up according to the details in the site-catalog.xml
    '''
    if not os.path.exists(site_catalog_file):
        raise GSMLogger().LogException("Error: site_catalog xml file not found at \
            file not found at "+ site_catalog_file)

    dikt = gsm_lib.get_site_details_as_dict(site_catalog_file, 'data_source')
    site_uri = dikt['site_URI']
    host, port = gsm_lib.parse_host_and_port(site_uri)

    site_uname          = dikt['site_uname']
    site_password       = dikt['site_password']
    site_remotepath     = dikt['site_remotepath']
    site_key_path       = dikt['site_key_path']
    site_contact_email  = dikt['site_contact_email']


    file_name = site_remotepath.split("/")[-1]
    site_localpath = configuration_directory + file_name

    # Pick up the smi file from the server and place it in the proj_root
    info = 'Retrieving file: %s from %s:%s' % (site_remotepath, host, port)
    print info
    gsmlogger.logger.info(info)

    info = 'Errors will be reported to: ' + site_contact_email
    print info
    gsmlogger.logger.info(info)

    sftp_instance = SFTPClient(host, port, site_uname, site_password, site_key_path)
    sftp_instance.get_file_from_uri(site_remotepath, site_localpath, site_contact_email)
    return site_localpath



if __name__ == "__main__":
    main()
