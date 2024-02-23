import logging

logger = logging.getLogger(__name__)


class LotteryEmailSender:
    def __init__(self, email_client, sender_email, recipient_email):
        self._email_client = email_client
        self._sender_email = sender_email
        self._recipient_email = recipient_email

    def send_email(self, subject, body):
        self._email_client.send_email(self._sender_email, "동행복권 API", self._recipient_email, self._recipient_email, subject, body)
