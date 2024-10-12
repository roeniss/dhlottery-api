@echo off
echo Building dhapi package into shared library
pip install cython
python setup.py build_ext --inplace

@REM echo Renaming .pyd to .dll
@REM ren src\dhapi\main.cp*.pyd main.dll

echo Build complete!
pause