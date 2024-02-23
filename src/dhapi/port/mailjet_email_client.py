import logging

from mailjet_rest import Client

logger = logging.getLogger(__name__)


class MailjetEmailClient:
    def __init__(self, api_key, api_secret):
        self._mailjet = Client(auth=(api_key, api_secret), version="v3.1")

    def send_email(self, sender_email, sender_name, recipient_email, recipient_name, subject, body):
        data = {
            "Messages": [
                {
                    "From": {"Email": sender_email, "Name": sender_name},
                    "To": [{"Email": recipient_email, "Name": recipient_name}],
                    "Subject": subject,
                    "TextPart": body,
                    "HTMLPart": "",
                }
            ]
        }

        result = self._mailjet.send.create(data=data)
        logger.debug(f"status_code: {result.status_code}")

        json = result.json()
        logger.debug(f"result.json: {json}")

        if result.status_code == 200:
            print("✉️ 메일 전송에 성공했습니다.")
        else:
            raise RuntimeError(f"❗ 메일 전송에 실패했습니다. (result.json: {json})")
