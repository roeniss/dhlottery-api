import os
import pathlib
from setuptools import find_packages, setup, Extension
from Cython.Build import cythonize
from distutils.sysconfig import get_config_vars

HERE = pathlib.Path(__file__).parent.resolve()

# Set paths for Android NDK and build tools
NDK_ROOT = "/home/southglory/android_sdk/ndk/28.0.12433566/toolchains/llvm/prebuilt/linux-x86_64"
SYSROOT = f"{NDK_ROOT}/sysroot"
LIBGCC_PATH = "/usr/lib/gcc/x86_64-linux-gnu/13" 

# List of API levels you want to build for
api_levels = ["28"] ##, "29", "30", "31", "32", "33", "34", "35"]

# Set the compilers from NDK toolchain
os.environ["CC"] = f"{NDK_ROOT}/bin/clang"
os.environ["CXX"] = f"{NDK_ROOT}/bin/clang++"

# Disable flags that are not compatible with NDK
cfg_vars = get_config_vars()
for key in ["CFLAGS", "OPT", "BASECFLAGS"]:
    if key in cfg_vars:
        cfg_vars[key] = cfg_vars[key].replace("-Wstrict-prototypes", "")

def _get_dependencies():
    with open(HERE / "requirements.txt") as f:
        return f.read().splitlines()


# Function to create the extension for each API level
def create_extension(api_level):
    arch_lib = f"{NDK_ROOT}/sysroot/usr/lib/aarch64-linux-android/{api_level}"

    # Check if crtbegin_so.o and crtend_so.o exist for the API level
    crtbegin = os.path.abspath(f"{arch_lib}/crtbegin_so.o")
    crtend = os.path.abspath(f"{arch_lib}/crtend_so.o")


    print("사용", crtbegin)
    print("사용", crtend)

    
    if not os.path.exists(crtbegin) or not os.path.exists(crtend):
        raise FileNotFoundError(f"crtbegin_so.o or crtend_so.o not found for API level {api_level}")

    return Extension(
        f"dhapi.main_{api_level}",
        sources=["src/dhapi/main.py"],
        extra_compile_args=[
            "-march=armv8-a",
            "--target=aarch64-linux-android",
            f"--sysroot={SYSROOT}"
        ],
        extra_link_args=[
            "--target=aarch64-linux-android",
            f"--sysroot={SYSROOT}",
            f"-L{arch_lib}",
            f"-L{LIBGCC_PATH}",
            "-lc", "-lgcc",
            f"--ld-path={NDK_ROOT}/bin/ld.lld",
            "-Wl,-verbose",
        ]
    )


    
    
# Generate a list of extensions for each API level and filter out None values
extensions = [create_extension(api_level) for api_level in api_levels]

# Print extensions to ensure it's a valid list of Extension objects
print("Extensions:", extensions)

# Setup call
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
    
    ext_modules=cythonize(extensions, language_level=3, nthreads=1),  # Use language_level=3 for Python 3 support
    install_requires=_get_dependencies(),
)
