import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="dhapi",
    version="1.3.1",
    description="DongHaeng Lottery Unofficial API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/roeniss/dhlottery-api",
    author="Roeniss Moon",
    author_email="roeniss2@gmail.com",
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: MacOS X",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="api,korean,donghaeng,lottery",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6, <4",
    entry_points={
        "console_scripts": [
            "dhapi=dhapi.main:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/roeniss/dhlottery-api/issues",
        "Source": "https://github.com/roeniss/dhlottery-api/",
    },
)
