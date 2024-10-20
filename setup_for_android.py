import os
import pathlib
from setuptools import find_packages, setup, Extension
from Cython.Build import cythonize
from distutils.sysconfig import get_config_vars

HERE = pathlib.Path(__file__).parent.resolve()

# Set NDK toolchain path
os.environ["CC"] = "/home/southglory/android_sdk/ndk/28.0.12433566/toolchains/llvm/prebuilt/linux-x86_64/bin/clang"
os.environ["CXX"] = "/home/southglory/android_sdk/ndk/28.0.12433566/toolchains/llvm/prebuilt/linux-x86_64/bin/clang++"

# Disable flags that are not compatible with NDK
cfg_vars = get_config_vars()
for key in ["CFLAGS", "OPT", "BASECFLAGS"]:
    if key in cfg_vars:
        cfg_vars[key] = cfg_vars[key].replace("-Wstrict-prototypes", "")

# Extension module for Cython
extensions = [
    Extension(
        "dhapi.main",
        ["src/dhapi/main.py"],
        extra_compile_args=[
            "--target=aarch64-linux-android",
            "--sysroot=/home/southglory/android_sdk/ndk/28.0.12433566/toolchains/llvm/prebuilt/linux-x86_64/sysroot"
        ],
        extra_link_args=[
            "--target=aarch64-linux-android",
            "--sysroot=/home/southglory/android_sdk/ndk/28.0.12433566/toolchains/llvm/prebuilt/linux-x86_64/sysroot",
            "-L/home/southglory/android_sdk/platforms/android-28/arch-arm64/usr/lib",  # Correct platform path
            "-lc", "-lgcc",
        ]
    )
]

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
    
    # Specify custom build directory here
    options={
        'build': {'build_lib': './build/android'},  # Custom build directory
    },
    
    ext_modules=cythonize(extensions, compiler_directives={'language_level': 3}),
    install_requires=_get_dependencies(),
)
