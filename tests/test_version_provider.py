import unittest
from unittest.mock import patch

from dhapi.meta.version_provider import get_installed_version


class TestVersionProvider(unittest.TestCase):

    @patch("dhapi.meta.version_provider.version", side_effect=Exception("Failed to get version"))
    def test_no_error_on_failed_to_get_version(self, _version):
        self.assertIsNotNone(get_installed_version())
