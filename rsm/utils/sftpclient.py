import os
import pysftp
import logging

from emailsender import EmailSender


class SFTPClient:
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


    def send_file_to_uri(self, remote_path, file_name, local_path, props = None):
        '''
        To email exceptions the caller must pass
        the object `props` of type EmailProps
        '''
        try:
            self.put(local_path, os.path.join(remote_path, file_name))
        except Exception, e:
            error = 'There was an error sending file %s to %s: %s\n' % (file_name, self._hostname, str(e))
            error = error + "SFTP file location: " + remote_path
            logging.error(error)
            logging.error('Please check the credentials/remotepath/localpath/Server URI')

            if props:
                # include the exception in the email body
                props.msg_body = error
                EmailSender().send(props)


    def get_file_from_uri(self, remote_path, local_path, props = None):
        '''
        To email exceptions the caller must pass
        the object `props` of type EmailProps
        '''
        try:
            self.get(remote_path, local_path)
        except Exception, e:
            error = 'There was an error getting file %s from %s: %s' % (remote_path, self._hostname, str(e))
            logging.error(error)

            if props:
                # include the exception in the email body
                props.msg_body = error
                EmailSender().send(props)

        return


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
