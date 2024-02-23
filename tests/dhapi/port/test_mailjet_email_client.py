import pytest

from dhapi.port.mailjet_email_client import MailjetEmailClient


@pytest.mark.skip("sending real email is not needed after checking success")
def test_send_email():
    sut = MailjetEmailClient("TO_EMAIL", "FROM_EMAIL", "API_KEY", "SECRET_KEY")

    sut.send_email("hello", "world")
