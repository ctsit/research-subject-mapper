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
    
    def configure_logging(self,log_file_path):
        '''Function to configure logging.

            The log levels are defined below. Currently the log level is
            set to DEBUG. All the logs in this level and above this level
            are displayed. Depending on the maturity of the application
            and release version these levels will be further
            narrowed down to WARNING
        

            Level       Numeric value
            =========================
            CRITICAL        50
            ERROR           40
            WARNING         30
            INFO            20
            DEBUG           10
            NOTSET          0

        '''
        last_slash = log_file_path.rfind('/')
        path_without_file = log_file_path[:last_slash]
        if not os.path.exists(path_without_file):
            try:
                os.makedirs(path_without_file)
            except:
                raise LogException("Log file cannot be created at the path "+path_without_file)
        # configuring logger file and log format
        # setting default log level to Debug
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

