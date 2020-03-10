@REM @Author: JinZhang
@REM @Date:   2020-03-10 15:31:00
@REM @Last Modified by:   JinZhang
@REM Modified time: 2020-03-10 15:35:49

@echo off && setlocal enabledelayedexpansion

set WorkDir=%~dp1
set WorkDir=%WorkDir:~,-1%

echo %WorkDir%

echo %cd%

echo %~dp0
echo %~dp1
