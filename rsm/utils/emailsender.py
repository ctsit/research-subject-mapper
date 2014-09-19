import smtplib, os, logging
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

class EmailProps():
    """
    Plain Old Data Storage class used for passing email properties
    """
    def __init__(self,
            host,
            port,
            sender,
            to_addr_list,
            cc_addr_list    = [],
            subject         = '',
            msg_body        = '',
            attach_files    = []):
        self.host           = host
        self.port           = port
        self.sender         = sender
        self.to_addr_list   = to_addr_list
        self.cc_addr_list   = cc_addr_list
        self.subject        = subject
        self.msg_body       = msg_body
        self.attach_files   = attach_files


class EmailSender():
    '''
    This class is a helper for sending emails
    '''
    def __init__(self):
        pass


    def send(self, props):
        '''
        Function to email the report of the get_data_from_redcap to site contact.
        '''

        assert type(props.to_addr_list) == list
        recipients = ",".join(props.to_addr_list)
        msg = MIMEMultipart()
        msg['From']     = props.sender
        msg['To']       = recipients
        msg['Cc']       = ",".join(props.cc_addr_list)
        msg['Date']     = formatdate(localtime=True)
        msg['Subject']  = props.subject

        logging.info("Message body: " + props.msg_body)
        msg.attach( MIMEText(props.msg_body) )

        try :
            for f in props.attach_files :
                logging.info("Adding email attachment: %s" % f)
                part = MIMEBase('application', "octet-stream")
                fh = open(f, "rb")
                part.set_payload( fh.read() )
                fh.close()
                Encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
                msg.attach(part)
        except:
            logging.error('Unable to open file: %s' % f)
            raise

        try:
           smtpObj = smtplib.SMTP(props.host, props.port)
           smtpObj.sendmail(props.sender, recipients, msg.as_string())
           smtpObj.close()
           logging.info("Success sending email to: %s " % recipients)

        except Exception, e:
            logging.error("Error sending email to: %s - %s" % (recipients, str(e)))
            return False
        return True

