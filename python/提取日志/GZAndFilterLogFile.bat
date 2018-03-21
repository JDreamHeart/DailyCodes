@REM @Author: JinZhang
@REM @Date:   2018-03-21 12:58:19
@REM @Last Modified by:   JinZhang
@REM Modified time: 2018-03-21 20:00:31

@echo off && setlocal enabledelayedexpansion

rem 获取该bat文件的路径
set batFilePath=%~dp0

for %%i in (%*) do (
	rem 获取文件名
	set fileName=%%i

	rem 判断是gz文件才进行解压
	if "!fileName:~-3!"==".gz" (
		rem 解压文件
		7z x !fileName! -aoa

		rem 获取文件名的后缀
		set fileSuffix="!fileName:~-6!"

		if !fileSuffix!=="tar.gz" (
			rem 解压，然后删除
			7z x !fileName:~0,-3! -aoa
			del !fileName:~0,-3!
		)
		if !fileSuffix!=="log.gz" (
			rem 运行bat文件路径中的filterLog.py文件，并把文件名作为参数传入
			python !batFilePath!python\filterLog.py !fileName:~0,-3!
		)
	) else (
		msg !username! /time:5 !fileName!" is not a .gz file!"
	)
)

pause