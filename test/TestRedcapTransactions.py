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
import tempfile

class TestRedcapTransactions(unittest.TestCase):

    def setUp(self):
        # create test setup
        self.configuration_directory = tempfile.mkdtemp()
        self.setup = {'source_data_schema_file': 'test_source_data_schema.xml'}
        # create test source data schema
        source_data_schema_content = '''<?xml version='1.0' encoding='US-ASCII'?>
        <source>
          <redcap_uri>http://localhost:8051/</redcap_uri>
          <apitoken>TOKENTOKENTOKENTOKENTOKENTOKEN</apitoken>
          <fields>
            <field>test_field1</field>
            <field>test_field2</field>
            <field>test_field3</field>
          </fields>
        </source>'''
        self.f = open(self.configuration_directory + '/test_source_data_schema.xml', 'w')
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
        global gsmlogger
        gsmlogger = GSMLogger()
        self.logFile = tempfile.mkstemp()[1]
        print self.logFile
        gsmlogger.configure_logging(self.logFile)
        logger = gsmlogger.logger
        redcap_obj = redcap_transactions()
        redcap_obj.configuration_directory = self.configuration_directory
        # init redcap interface
        properties = redcap_obj.init_redcap_interface(self.setup, logger)
        self.assertEqual(properties['path'],'/' )
        self.assertEqual(properties['host'],'localhost:8051' )
        self.assertEqual(properties['token'],'TOKENTOKENTOKENTOKENTOKENTOKEN' )
        self.assertEqual(properties['fields'],'test_field1,test_field2,test_field3' )
        self.assertEqual(properties['is_secure'],False )
        generate_subject_map_input.parse_site_details_and_send(self.setup['source_data_schema_file'], self.smi_filenames,logger)
        
        returned = redcap_obj.get_data_from_redcap(properties,logger)
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
        
    #@all_requests
    def response_content(self, environ, start_response):
        response_body = 'OK'
        status = '200 OK'
        response_headers = [('Content-Type', 'text/plain'),
            ('Content-Length', str(len(response_body)))]
        start_response(status, response_headers)
        body= ''  # b'' for consistency on Python 3.0
        try:
            length= int(environ.get('CONTENT_LENGTH', '0'))
        except ValueError:
            length= 0
        if length!=0:
            # got the body of the response
            body = environ['wsgi.input'].read(length)
            required_params = {
                            'format':'xml',
                            'returnFormat':'xml',
                            'content':'record',
                            'fields':'test_field1,test_field2,test_field3',
                            'token':'TOKENTOKENTOKENTOKENTOKENTOKEN',
                            'type':'flat'}
        import re
        if re.search(r'format\=xml',body).group() != 'format=xml' or \
        re.search(r'returnFormat\=xml',body).group() != 'returnFormat=xml' or \
        re.search(r'content\=record',body).group() != 'content=record' or \
        re.search(r'token\=TOKENTOKENTOKENTOKENTOKENTOKEN',body).group() != 'token=TOKENTOKENTOKENTOKENTOKENTOKEN' or \
        re.search(r'type\=flat',body).group() != 'type=flat':
            response_body = 'NOT OK'
        return [response_body]

        '''This function runs as a seperate thread.
            used to start the server at localhost:8051
        '''
    def server_setup(self):
        httpd = make_server('localhost', 8051, self.response_content)
        httpd.handle_request()

if __name__ == "__main__":
    unittest.main()
