@echo off
REM filepath: /c:/Users/Hurca/OneDrive/GitCode/Blender-Utilities-Gadget/zip.cmd

REM ����Ҫѹ�����ļ��к����ѹ������·��
set SOURCE_FOLDER=C:\Users\Hurca\OneDrive\GitCode\Blender-Utilities-Gadget
set OUTPUT_ZIP=C:\Users\Hurca\OneDrive\GitCode\Blender-Utilities-Gadget.zip

REM ʹ�� PowerShell ����ѹ����
powershell -command "Compress-Archive -Path '%SOURCE_FOLDER%' -DestinationPath '%OUTPUT_ZIP%' -Force"

echo ѹ�����: %OUTPUT_ZIP%