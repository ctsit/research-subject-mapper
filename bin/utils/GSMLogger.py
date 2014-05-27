import logging
import os
import sys
# This addresses the issues with relative paths
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../..")
proj_root = os.path.abspath(goal_dir)+'/'
sys.path.insert(0, proj_root+'bin')


class GSMLogger:
    """A class for handling logging"""
    # create logger
    logger = logging.getLogger('research_subject_mapper')

    def __init__(self):
        self.data = []


    '''Configure log level to: DEBUG'''
    def configure_logging(self, log_file_path):
        logging.basicConfig(filename=log_file_path,
                                format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                                datefmt='%m/%d/%Y %H:%M:%S',
                                filemode='w',
                                level=logging.DEBUG)

    class LogException(Exception):
        '''Class to log the exception
        logs the exception at an error level
        '''
        def __init__(self, *val):
            self.val = val

        def __str__(self):
            # print self.val
            GSMLogger().logger.error(self.val)
            return repr(self.val)
