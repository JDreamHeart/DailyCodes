@REM @Author: JinZhang
@REM @Date:   2020-03-10 15:31:00
@REM @Last Modified by:   JinZhang
@REM Modified time: 2020-03-10 15:35:49

@echo off && setlocal enabledelayedexpansion

REM set WorkDir=%~dp1
REM set WorkDir=%WorkDir:~,-1%

REM echo %WorkDir%

REM echo %cd%

REM echo %~dp0
REM echo %~dp1

set pyexe=python

for /f "tokens=1,2 delims==" %%i in (tst.env) do (
    if "%%i"=="pyexe" set pyexe=%%j
)
echo !pyexe!
