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
            # Email error to the concerned authority
            print 'Error sending file to %s' % self._hostname
            print 'Check the credentials/remotepath/localpath/Server URI'
            email_transactions().send_mail('please-do-not-reply@ufl.edu', contact_email, str(e))
            print str(e)

    def get_file_from_uri(self, remotepath, localpath, contact_email):
        try:
            self.get(remotepath, localpath)
        except Exception, e:
            # Email error to the concerned authority
            email_transactions().send_mail('please-do-not-reply@ufl.edu', contact_email, str(e))
            print str(e)

    def put(self, local_path, remote_path):
        connection_info = self._connection_info()

        with pysftp.Connection(**connection_info) as sftp:
            print('Connected as {0}@{1}:{2}'
                  .format(connection_info['username'], connection_info['host'],
                          connection_info['port']))

            remotedir = os.path.dirname(remote_path)
            if remotedir:
                sftp.makedirs(remotedir)
                sftp.chdir(remotedir)

            filename = os.path.basename(remote_path)
            sftp.put(local_path, filename)

    def get(self, remote_path, local_path):
        connection_info = self._connection_info()

        with pysftp.Connection(**connection_info) as sftp:
            print('Connected as {0}@{1}:{2}'
                  .format(connection_info['username'], connection_info['host'],
                          connection_info['port']))

            sftp.get(remote_path, local_path)

    def _connection_info(self):
        """Helper method to build a dict with connection information"""
        return {
            'host': self._hostname,
            'port': self._port,
            'username': self._username,
            'password': self._password,
            'private_key': self._private_key,
            'private_key_pass': self._private_key_pass,
        }
