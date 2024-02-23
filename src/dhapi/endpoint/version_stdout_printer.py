from rich.console import Console
from rich.table import Table


class VersionStdoutPrinter:

    def print_version(self, version):
        console = Console()

        table = Table("현재버전")
        table.add_row(version)

        console.print(table)
