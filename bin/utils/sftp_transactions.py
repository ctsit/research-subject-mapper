import os
import pysftp
from email_transactions import email_transactions


class sftp_transactions:
    """A class for handling the sftp transactions. This class contains
    functions for getting a file from sftp server and putting a file
    to a sftp server"""
    def __init__(self, hostname, port=22, username=None, password=None,
                 private_key=None, private_key_pass=None):
        self.data = []
        self._hostname = hostname
        self._port = int(port)
        self._username = username
        self._password = password
        self._private_key = private_key
        self._private_key_pass = private_key_pass

    def send_file_to_uri(self, remote_path, file_name, local_path, contact_email):
        try:
            self.put(local_path, remote_path+file_name)
        except Exception, e:
            #Report should be sent to the concerned authority with the error message
            print 'Error sending file to %s' % self._hostname
            print 'Check the credentials/remotepath/localpath/Server URI'
            email_transactions().send_mail('please-do-not-reply@ufl.edu', contact_email, str(e))
            print str(e)

    def put(self, local_path, remote_path):
        connection_info = {
            'host': self._hostname,
            'port': self._port,
            'username': self._username,
            'password': self._password,
            'private_key': self._private_key,
            'private_key_pass': self._private_key_pass,
        }

        with pysftp.Connection(**connection_info) as sftp:
            print ('Connected as {0}@{1}:{2}'
                   .format(self._username, self._hostname, self._port))

            remotedir = os.path.dirname(remote_path)
            if remotedir:
                sftp.makedirs(remotedir)
                sftp.chdir(remotedir)

            filename = os.path.basename(remote_path)
            sftp.put(local_path, filename)

    def get_file_from_uri(self, site_URI, uname, password, remotepath, localpath, contact_email):
        '''This function gets the specified file to the given uri.
        Authentication is done using the uname and password
        remotepath - the path where the file needs to be put
        localpath - the path where the file is picked from
        contact_email - the email of the concerned authority to mail to incase of failed
        transaction

        '''
        # make a connection with uri and credentials
        connect = pysftp.Connection(host=site_URI, username=uname, password=password)

        try:
            # get the file from the designated location in the server
            connect.get(remotepath, localpath)
            # close the connection
            connect.close()
        except Exception, e:
            # closing the connection incase there is any exception
            connect.close()
            '''Report should be sent to the concerned authority with the error
                message
            '''
            email_transactions().send_mail('please-do-not-reply@ufl.edu', contact_email, str(e))
            print str(e)
    pass
