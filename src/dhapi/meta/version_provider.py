from importlib.metadata import version


class VersionProvider:
    def __init__(self, version_endpoint):
        self._version_endpoint = version_endpoint
        self._package_name = "dhapi"

    def show_version(self):
        package_version = version(self._package_name)
        self._version_endpoint.print_version(package_version)
