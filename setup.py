import pathlib

from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent.resolve()


def _get_dependencies():
    with open(HERE + "/requirements.txt") as f:
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

    entry_points={
        "console_scripts": [
            "dhapi=dhapi.main:main",
        ],
    },

    install_requires=_get_dependencies(),
)
