@echo off && setlocal enabledelayedexpansion

set pyexe=python
set mainfile=main.py
set buildfile=build.py
set pii=

for /f "tokens=1,2 delims==" %%i in (../test.env) do (
    if "%%i"=="pyexe" set pyexe=%%j
    if "%%i"=="mainfile" set mainfile=%%j
    if "%%i"=="buildfile" set buildfile=%%j
    if "%%i"=="pii" set pii=%%j
)
echo %pyexe% %mainfile% %buildfile% %pii%
echo %mainfile%
echo %pii%
echo %buildfile%