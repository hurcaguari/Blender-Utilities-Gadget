@echo off
REM filepath: /c:/Users/Hurca/OneDrive/GitCode/Blender-Utilities-Gadget/zip.cmd

REM ����Ҫѹ�����ļ��к����ѹ������·��
set SOURCE_FOLDER=C:\Users\Hurca\OneDrive\GitCode\Blender-Utilities-Gadget/source
set OUTPUT_ZIP=C:\Users\Hurca\OneDrive\GitCode\Blender-Utilities-Gadget.zip

REM ʹ�� PowerShell ����ѹ����
powershell -command "Get-ChildItem -Path '%SOURCE_FOLDER%' | Compress-Archive -DestinationPath '%OUTPUT_ZIP%' -Force"

echo ѹ�����: %OUTPUT_ZIP%