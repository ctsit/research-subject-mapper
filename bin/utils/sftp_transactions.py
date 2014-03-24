class sftp_transactions:
    """A class for handling the sftp transactions. This class contains
    functions for getting a file from sftp server and putting a file
    to a sftp server"""

    def __init__(self):
        super(sftp_transactions, self).__init__()
        
    def send_file_to_uri(site_URI, uname, password, remotepath, localpath, contact_email):
        '''This function puts the specified file to the given uri.
        Authentication is done using the uname and password
        remotepath - the path where the file needs to be put
        localpath - the path where the file is picked from
        contact_email - the email of the concerned authority to mail to incase of failed
        transaction
        
        '''
        try:
        	# make a connection with uri and credentials
            s = sftp.Connection(host=site_URI, username=uname, password=password)
            # put the file at the designated location in the server
            s.put(localpath, remotepath)
            # close the connection
            s.close()

        except Exception, e:
        	# closing the connection incase there is any exception
        	s.close()
        	''' TODO
        	Report should be sent to the concerned authority with the error
        	message
        	'''
            print str(e)
        pass