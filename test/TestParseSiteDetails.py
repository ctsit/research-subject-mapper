import unittest
import os, sys
import tempfile
import pprint

sys.path.append('bin/')
import gsm_lib

"""
TestParseSiteDetails.py

   Unit test for  gsm_lib#get_site_details_as_dic()
"""

__author__      = "CTS-IT team"
__copyright__   = "Copyright 2014, University of Florida"
__license__     = "BSD 3-Clause"
__version__     = "0.1"


class TestParseSiteDetails(unittest.TestCase):

    def test_get_site_details_as_dict(self):
        xml = """<?xml version='1.0' encoding='UTF-8'?>
<sites_list>
    <site type="data_source">
        <site_URI>          source_sftp             </site_URI>
        <site_uname>        source_tester           </site_uname>
        <site_password>     source_pass             </site_password>
        <site_remotepath>   smi.xml                 </site_remotepath>
        <site_contact_email>jdoe@example.com        </site_contact_email>
        <site_key_path>                             </site_key_path>
    </site>

    <site type="data_destination">
        <site_URI>          dest_sftp               </site_URI>
        <site_uname>        dest_tester             </site_uname>
        <site_password>     dest_pass               </site_password>
        <site_remotepath>   smi.xml                 </site_remotepath>
        <site_contact_email>jdoe@example.com        </site_contact_email>
        <site_key_path>     path                    </site_key_path>
    </site>
</sites_list>
        """

        try :
            pair = tempfile.mkstemp()
            file_path = pair[1]
            f = open(file_path, 'r+')
            f.write(xml)
            f.close()
        except :
            print('Unable to create temp_file: ' + file_path)


        good_dikt_source = {
            'site_URI'              : 'source_sftp',
            'site_uname'            : 'source_tester',
            'site_password'         : 'source_pass',
            'site_remotepath'       : 'smi.xml',
            'site_contact_email'    : 'jdoe@example.com',
            'site_key_path'         : '',
        }

        good_dikt_dest = {
            'site_URI'              : 'dest_sftp',
            'site_uname'            : 'dest_tester',
            'site_password'         : 'dest_pass',
            'site_remotepath'       : 'smi.xml',
            'site_contact_email'    : 'jdoe@example.com',
            'site_key_path'         : 'path',
        }


        # Test the actual function
        dikt_source = gsm_lib.get_site_details_as_dict(file_path, 'data_source')
        dikt_dest   = gsm_lib.get_site_details_as_dict(file_path, 'data_destination')

        #pprint.pprint(dikt)
        self.assertEqual(good_dikt_source, dikt_source)
        self.assertEqual(good_dikt_dest, dikt_dest)

        try :
            os.unlink(file_path)
        except :
            print('Unable to remove temp_file: ' + file_path)

if __name__ == '__main__':
    unittest.main()
