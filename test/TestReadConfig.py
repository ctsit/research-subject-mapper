import json
import unittest
import tempfile
import os
import sys
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'
sys.path.append(proj_root + 'bin/')
import gsm_lib
import utils.SimpleConfigParser as SimpleConfigParser

class TestReadConfig(unittest.TestCase):

    def setUp(self):
        self.setupFolder = tempfile.mkdtemp() + "/"
        self.setupFile = "settings.ini"
        self.input = """smtp_host_for_outbound_mail = smtp.example.org
system_log_file = log/rsm.log
source_data_schema_file = source_data_schema.xml
site_catalog = site-catalog.xml
redcap_uri = https://example.org/redcap/api/
token = ABCDEF878D219CFA5D3ADF7F9AB12345"""
        self.setupFileFullPath = self.setupFolder + self.setupFile
        f = open(self.setupFileFullPath, 'w')
        f.write(self.input)
        
        f.close()
        self.files = ['source_data_schema.xml', 'site-catalog.xml']
        for file in self.files:
            try:
                f = open(self.setupFolder+file, "w+")
            except:
                print("setUp failed to create file '" + file + "'")

    def test_readConfig(self):
        settings = SimpleConfigParser.SimpleConfigParser()
        settings.read(self.setupFileFullPath)
        settings.set_attributes()
        gsm_lib.read_config(self.setupFolder,self.setupFile, settings)
        self.assertEqual(settings.system_log_file, "log/rsm.log")
        self.assertEqual(settings.source_data_schema_file,
            "source_data_schema.xml")
        self.assertEqual(settings.site_catalog, "site-catalog.xml")
        self.assertEqual(settings.redcap_uri,
            "https://example.org/redcap/api/")
        self.assertEqual(settings.token,
            "ABCDEF878D219CFA5D3ADF7F9AB12345")
        self.assertEqual(settings.smtp_host_for_outbound_mail,
            "smtp.example.org")

    def tearDown(self):
        os.unlink(self.setupFileFullPath)
        for file in self.files:
            try:
                os.unlink(self.setupFolder+file)
            except:
                print("setUp failed to unlink file '" + file + "'")

        return()

if __name__ == '__main__':
    unittest.main()
