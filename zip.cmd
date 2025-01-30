@echo off
REM filepath: /c:/Users/Hurca/OneDrive/GitCode/Blender-Utilities-Gadget/zip.cmd

REM 定义要压缩的文件夹和输出压缩包的路径
set SOURCE_FOLDER=C:\Users\Hurca\OneDrive\GitCode\Blender-Utilities-Gadget/source
set OUTPUT_ZIP=C:\Users\Hurca\OneDrive\GitCode\Blender-Utilities-Gadget.zip

REM 使用 PowerShell 创建压缩包
powershell -command "Get-ChildItem -Path '%SOURCE_FOLDER%' | Compress-Archive -DestinationPath '%OUTPUT_ZIP%' -Force"

echo 压缩完成: %OUTPUT_ZIP%