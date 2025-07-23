from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


def _read_version_file() -> str:
    version_path = Path(__file__).resolve().parents[1].parent / "VERSION"
    return version_path.read_text(encoding="utf-8").strip()


try:
    __version__ = version("dhapi")
except PackageNotFoundError:
    __version__ = _read_version_file()

