from unittest import TestCase
from unittest.mock import patch

from dhapi.client.lottery_client import LotteryClient


class TestLotteryClient(TestCase):
    @patch("requests.get")
    def cookies(self, _mock_get):
        with self.assertRaises(KeyError):
            LotteryClient()

    @patch("requests.get")
    def test__init__success_when_JSESSIONID_contained_in_response_headers(self, mock_get):
        mock_get.return_value.cookies = [{"name": "JSESSIONID", "value": "test_jession_id"}]
        self.client = LotteryClient()

    @patch("requests.get")
    @patch("requests.post")
    def test__login__success_with_JSESSIONID(self, mock_post, mock_get):
        mock_get.return_value.cookies = [{"name": "JSESSIONID", "value": "test_jession_id"}]
        self.client = LotteryClient()
        self.client.login("test_user_id", "test_password")

        mock_post.assert_called_once()
