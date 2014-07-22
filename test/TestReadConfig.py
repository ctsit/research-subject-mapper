import os, sys
import unittest
import tempfile

import gsm_lib

class TestReadConfig(unittest.TestCase):

    def setUp(self):
        self.setupFolder = tempfile.mkdtemp() + "/"
        self.input = """
system_log_file = log/rsm.log
source_data_schema_file = source_data_schema.xml
site_catalog = site-catalog.xml
sender_email = please-do-not-reply@ufl.edu
"""
        self.setupFileFullPath = self.setupFolder + 'settings.ini'
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
        settings = gsm_lib.get_settings(self.setupFileFullPath)
        gsm_lib.read_config(self.setupFolder, self.setupFileFullPath, settings)
        self.assertEqual(settings.system_log_file, "log/rsm.log")
        self.assertEqual(settings.source_data_schema_file,
            "source_data_schema.xml")
        self.assertEqual(settings.site_catalog, "site-catalog.xml")        

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
