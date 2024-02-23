from pytest_mock import MockerFixture

from dhapi.endpoint.lottery_email_sender import LotteryEmailSender


def test_send_email_call_email_client_with_expected_arguments(mocker: MockerFixture):
    mock_client = mocker.patch('dhapi.port.mailjet_email_client.MailjetEmailClient')
    sut = LotteryEmailSender(mock_client, "sender@email.com", "recipient@email.com")

    sut.send_email("subject", "body")

    mock_client.send_email.assert_called_once_with("sender@email.com", "동행복권 API", "recipient@email.com", "recipient@email.com", "subject", "body")
