'''
@author : Radha
email : rkandula@ufl.edu

This file creates a test suite for all the test classes.

'''

import unittest


'''
    IMPORTANT: the imports should be updated in order to add the test to
    the test suite.
    note: No error will be thrown if the import is not done, at the same
    time test also will not be run even we addTest(<test_class>)
'''
from lxml import etree
# from TestLog import TestLog
from TestReadConfig import TestReadConfig

class rsm_suite(unittest.TestSuite):

    def suite(self):
        # create a test suite
        rsm_test_suite = unittest.TestSuite()
        
        # add the test to the suite in the order to be tested
        # rsm_test_suite.addTest(TestLog)
        redi_test_suite.addTest(TestReadConfig)
        
        # return the suite
        return unittest.TestSuite([rsm_test_suite])

def main():
    unittest.main(buffer=True)
    

if __name__ == '__main__':
    main()

