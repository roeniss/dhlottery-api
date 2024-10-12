import os
import pathlib
from setuptools import find_packages, setup
from Cython.Build import cythonize
from distutils.sysconfig import get_config_var, get_config_vars

HERE = pathlib.Path(__file__).parent.resolve()

# Set NDK toolchain path
os.environ["CC"] = "/path/to/ndk/toolchain/bin/clang"  # Update with your Android NDK Clang path
os.environ["CXX"] = "/path/to/ndk/toolchain/bin/clang++"

# Disable flags that are not compatible with NDK
cfg_vars = get_config_vars()
for key in ["CFLAGS", "OPT", "BASECFLAGS"]:
    if key in cfg_vars:
        cfg_vars[key] = cfg_vars[key].replace("-Wstrict-prototypes", "")

def _get_dependencies():
    with open(HERE / "requirements.txt") as f:
        return f.read().splitlines()

setup(
    name="dhapi",
    description="동행복권 비공식 API",
    version=(HERE / "VERSION").read_text(encoding="utf-8"),
    long_description=(HERE / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/roeniss/dhlottery-api",
    project_urls={
        "Bug Reports": "https://github.com/roeniss/dhlottery-api/issues",
        "Source": "https://github.com/roeniss/dhlottery-api/",
    },
    author="Roeniss Moon",
    author_email="roeniss2@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
    ],
    keywords="donghaeng,lottery,lotto645,api,korean",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8, <4",
    ext_modules=cythonize("src/dhapi/main.py", language_level=3),
    install_requires=_get_dependencies(),
)
