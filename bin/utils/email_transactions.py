class email_transactions():
    """docstring for email_transactions"""
    def __init__(self):
        self.data = []

    def send_report(self, sender, receiver, body):
        '''
        Function to email the report of the get_data_from_redcap to site contact.
        mohan
        '''
        import smtplib
        from email.MIMEMultipart import MIMEMultipart
        from email.MIMEText import MIMEText
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = "Email from Research Subject Mapper"
        msg.attach(MIMEText(body, 'html'))
        
        """
        Sending email

        """
        
        try:
           smtpObj = smtplib.SMTP('smtp.ufl.edu',25)
           smtpObj.sendmail(sender, receiver, msg.as_string())
           print "Successfully sent email to "+receiver
        except Exception:
            print "Error: unable to send email to "+receiver