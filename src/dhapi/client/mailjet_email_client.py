import logging

from mailjet_rest import Client

logger = logging.getLogger(__name__)


class MailjetEmailClient:
    def __init__(self, to_email, api_key, api_secret, _sender_email):
        self._to_email = to_email
        self._mailjet = Client(auth=(api_key, api_secret), version="v3.1")
        self._sender_email = _sender_email

    def send_email(self, subject, body):
        data = {
            "Messages": [
                {
                    "From": {"Email": self._sender_email, "Name": "동행복권 API"},
                    "To": [{"Email": self._to_email, "Name": self._to_email}],
                    "Subject": subject,
                    "TextPart": body,
                    "HTMLPart": "",
                }
            ]
        }

        result = self._mailjet.send.create(data=data)
        logging.debug(result.json())

        if result.status_code == 200:
            logger.info("메일 전송에 성공했습니다.")
        else:
            logger.error(f"메일 전송에 실패했습니다. (result: {result.json()})")
            raise RuntimeError(f"메일 전송에 실패했습니다. (status_code: {result.status_code})")
