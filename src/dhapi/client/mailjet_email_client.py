import logging

from mailjet_rest import Client

logger = logging.getLogger(__name__)


class MailjetEmailClient:
    def __init__(self, recipient_email, sender_email, api_key, api_secret):
        self._recipient_email = recipient_email
        self._sender_email = sender_email
        self._mailjet = Client(auth=(api_key, api_secret), version="v3.1")

    def send_email(self, subject, body):
        data = {
            "Messages": [
                {
                    "From": {"Email": self._sender_email, "Name": "동행복권 API"},
                    "To": [{"Email": self._recipient_email, "Name": self._recipient_email}],
                    "Subject": subject,
                    "TextPart": body,
                    "HTMLPart": "",
                }
            ]
        }

        result = self._mailjet.send.create(data=data)

        logging.debug(result.json())

        if result.status_code == 200:
            logger.info("✉️ 메일 전송에 성공했습니다.")
        else:
            logger.error(f"❗ 메일 전송에 실패했습니다. (result: {result.json()})")
