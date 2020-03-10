@REM @Author: JDreamHeart
@REM @Date:   2020-03-10 15:18:46
@REM @Last Modified by:   JinZhang
@REM Modified time: 2020-03-10 17:12:32

@echo off && setlocal enabledelayedexpansion

rem 获取参数
set Program=%1
set LnkName=%2
set Desc=%3
set WorkDir=%~dp1
set WorkDir=%WorkDir:~,-1%

rem 生成vbs脚本
(echo Set WshShell=CreateObject("WScript.Shell"^)
echo strDesKtop=WshShell.SpecialFolders("Desktop"^)
echo Set oShellLink=WshShell.CreateShortcut(strDesKtop^&"\%LnkName%.lnk"^)
echo oShellLink.TargetPath="%Program%"
echo oShellLink.WorkingDirectory="%WorkDir%"
echo oShellLink.WindowStyle=1
echo oShellLink.Description="%Desc%"
echo oShellLink.Save)>makelnk.vbs

rem 运行vbs脚本并删除
makelnk.vbs
del /f /q makelnk.vbs