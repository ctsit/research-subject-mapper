__author__ = 'Taeber Rapczak <taeber@ufl.edu>'

import os
import contextlib
import tempfile
from unittest import TestCase
from bin.utils.sftp_transactions import sftp_transactions


class sftp_transactionsTests(TestCase):
    def test_put_with_password(self):
        server = 'localhost'
        port = 2222
        username = 'vagrant'
        password = 'vagrant'

        sftp = sftp_transactions(server, port, username, password)
        local_path = os.path.realpath(__file__)
        remote_path = os.path.basename(__file__)
        sftp.put(local_path, remote_path)

    def test_put_into_nested_directories(self):
        server = 'localhost'
        port = 2222
        username = 'vagrant'
        password = 'vagrant'

        sftp = sftp_transactions(server, port, username, password)
        local_path = os.path.realpath(__file__)
        remote_path = './tmp/subtmp/' + os.path.basename(__file__)
        sftp.put(local_path, remote_path)

    def test_get(self):
        with temporary_file() as temp_filename:
            sftp = sftp_transactions('localhost', port=2222,
                                     username='vagrant', password='vagrant')
            sftp.get_file_from_uri(remotepath='/vagrant/Vagrantfile',
                                   localpath=temp_filename,
                                   contact_email=None)
            self.assertFalse(os.stat(temp_filename)[6] == 0)

    def test_key_based_auth(self):
        server = 'localhost'
        port = 2222
        username = 'vagrant'
        key_path = 'id_rsa'

        with temporary_key(filename=key_path):
            sftp = sftp_transactions(server, port, username, private_key=key_path)
            sftp.put(os.path.realpath(__file__), os.path.basename(__file__))

@contextlib.contextmanager
def temporary_file():
    filename = tempfile.NamedTemporaryFile(delete=False).name
    yield filename
    os.remove(filename)

@contextlib.contextmanager
def temporary_key(filename):
    vagrant_insecure_private_key = """\
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzI
w+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoP
kcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2
hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NO
Td0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcW
yLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQIBIwKCAQEA4iqWPJXtzZA68mKd
ELs4jJsdyky+ewdZeNds5tjcnHU5zUYE25K+ffJED9qUWICcLZDc81TGWjHyAqD1
Bw7XpgUwFgeUJwUlzQurAv+/ySnxiwuaGJfhFM1CaQHzfXphgVml+fZUvnJUTvzf
TK2Lg6EdbUE9TarUlBf/xPfuEhMSlIE5keb/Zz3/LUlRg8yDqz5w+QWVJ4utnKnK
iqwZN0mwpwU7YSyJhlT4YV1F3n4YjLswM5wJs2oqm0jssQu/BT0tyEXNDYBLEF4A
sClaWuSJ2kjq7KhrrYXzagqhnSei9ODYFShJu8UWVec3Ihb5ZXlzO6vdNQ1J9Xsf
4m+2ywKBgQD6qFxx/Rv9CNN96l/4rb14HKirC2o/orApiHmHDsURs5rUKDx0f9iP
cXN7S1uePXuJRK/5hsubaOCx3Owd2u9gD6Oq0CsMkE4CUSiJcYrMANtx54cGH7Rk
EjFZxK8xAv1ldELEyxrFqkbE4BKd8QOt414qjvTGyAK+OLD3M2QdCQKBgQDtx8pN
CAxR7yhHbIWT1AH66+XWN8bXq7l3RO/ukeaci98JfkbkxURZhtxV/HHuvUhnPLdX
3TwygPBYZFNo4pzVEhzWoTtnEtrFueKxyc3+LjZpuo+mBlQ6ORtfgkr9gBVphXZG
YEzkCD3lVdl8L4cw9BVpKrJCs1c5taGjDgdInQKBgHm/fVvv96bJxc9x1tffXAcj
3OVdUN0UgXNCSaf/3A/phbeBQe9xS+3mpc4r6qvx+iy69mNBeNZ0xOitIjpjBo2+
dBEjSBwLk5q5tJqHmy/jKMJL4n9ROlx93XS+njxgibTvU6Fp9w+NOFD/HvxB3Tcz
6+jJF85D5BNAG3DBMKBjAoGBAOAxZvgsKN+JuENXsST7F89Tck2iTcQIT8g5rwWC
P9Vt74yboe2kDT531w8+egz7nAmRBKNM751U/95P9t88EDacDI/Z2OwnuFQHCPDF
llYOUI+SpLJ6/vURRbHSnnn8a/XG+nzedGH5JGqEJNQsz+xT2axM0/W/CRknmGaJ
kda/AoGANWrLCz708y7VYgAtW2Uf1DPOIYMdvo6fxIB5i9ZfISgcJ/bbCUkFrhoH
+vq/5CIWxCPp0f85R4qxxQ5ihxJ0YDQT9Jpx4TMss4PSavPaBH3RXow5Ohe+bYoQ
NE5OgEXk2wVfZczCZpigBKbKZHNYcelXtTt/nP3rsCuGcM4h53s=
-----END RSA PRIVATE KEY-----
"""
    with open(filename, mode='w+b') as fp:
        fp.write(vagrant_insecure_private_key)

    yield
    os.remove(filename)
