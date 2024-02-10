import unittest

from dhapi.client.mailjet_email_client import MailjetEmailClient


class TestMailjetEmailClient(unittest.TestCase):

    @unittest.skip("sending real email is not needed after checking success")
    def test_send_email(self):
        sut = MailjetEmailClient("EMAIL", "API_KEY", "SECRET_KEY")

        sut.send_email("hello", "world")
