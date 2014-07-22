
import os, sys
import unittest

sys.path.append('bin/utils')

import gsm_lib
from emailsender import EmailProps
from emailsender import EmailSender

class TestEmailSender(unittest.TestCase):
    def test_send(self):
        conf_file = 'gsm-devconfig/settings.ini'
        settings = gsm_lib.get_settings(conf_file)

        props = EmailProps(
            settings.smtp_host,
            settings.smtp_port,
            settings.sender_email,
            [settings.test_recipient],
            [],
            'Research Subject Mapper Notification',
            'This is a test')
 
        success = EmailSender().send(props)
        self.assertEqual(True, success)


if __name__ == '__main__':
    unittest.main()
