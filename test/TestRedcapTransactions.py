'''

This file is to test the function redcap_transactions of bin/utils/redcap_transactions.py
This file should be run from the project level folder (one level up from /bin)

'''
import unittest
import os
import sys
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'
sys.path.append(proj_root+'test')
sys.path.append(proj_root+'bin')
sys.path.append(proj_root+'bin/utils')

from wsgiref.simple_server import make_server
import requests
import thread
from GSMLogger import GSMLogger
from redcap_transactions import redcap_transactions
import generate_subject_map_input

class TestRedcapTransactions(unittest.TestCase):

    def setUp(self):
        # create test setup
        self.setup = {'source_data_schema_file': 'test_source_data_schema.xml'}
        # create test source data schema
        source_data_schema_content = '''<?xml version='1.0' encoding='US-ASCII'?>
        <source>
          <redcap_uri>http://localhost/</redcap_uri>
          <apitoken>TOKENTOKENTOKENTOKENTOKENTOKEN</apitoken>
          <fields>
            <field>test_field1</field>
            <field>test_field2</field>
            <field>test_field3</field>
          </fields>
        </source>'''
        self.f = open('test_source_data_schema.xml', 'w')
        self.f.write(source_data_schema_content)
        self.f.close()

        # create smi files
        self.smi_filenames = ['555', '666']
        f1 = open(proj_root+'smi555.xml', 'w')
        f1.write('Test file 1')
        f1.close()
        f2 = open(proj_root+'smi666.xml', 'w')
        f2.write('Test file 2')
        f2.close()
        # start a server in seperate thread
        thread.start_new_thread(self.server_setup,())

    def testRedcapTransactions(self):
        # Configure logging
        gsmlogger = GSMLogger()
        gsmlogger.configure_logging()
        logger = gsmlogger.logger
        redcap_obj = redcap_transactions()

        # init redcap interface
        properties = redcap_obj.init_redcap_interface(self.setup, logger)

        generate_subject_map_input.parse_site_details_and_send(self.setup['source_data_schema_file'], self.smi_filenames)

        # checking for the response from the server started with the expected
        # data from user side
        assert returned == 'OK'

    def tearDown(self):
        #try:
          #os.remove(proj_root+'test_source_data_schema.xml')
          #os.remove(self.smi_filenames[0])
          #os.remove(self.smi_filenames[1])
        #except OSError:
        #  pass
        return()

if __name__ == "__main__":
    unittest.main()
