import smtplib, os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

class email_transactions():
    """docstring for email_transactions
    This class deals with the email transactions as a shared library"""
    def __init__(self):
        self.data = []

    def send_mail(self,send_from, send_to, body, files=[]):
        '''
        Function to email the report of the get_data_from_redcap to site contact.
        mohan
        '''
        assert type(files)==list

        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = send_to
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = "Email from Research Subject Mapper"

        msg.attach( MIMEText(body) )

        for f in files:
            part = MIMEBase('application', "octet-stream")
            part.set_payload( open(f,"rb").read() )
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
            msg.attach(part)

        """
        Sending email

        """
        
        try:
           smtpObj = smtplib.SMTP('smtp.ufl.edu',25)
           smtpObj.sendmail(send_from, send_to, msg.as_string())
           smtpObj.close()
           print "Successfully sent email to "+send_to
        except Exception:
            print "Error: unable to send email to "+send_to