ECHO OFF

CD /D %~dp0

SET gim_path=F:\project\svn\trunk\client\res\model\zhucheng
SET fbx_path=E:\private\project\DailyCodes\python\test\output
SET exe_path=test_params.py

C:\Python27\python.exe gim_to_fbx.py %gim_path% %fbx_path% %exe_path%

PAUSE