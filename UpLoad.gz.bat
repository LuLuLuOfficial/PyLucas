@echo off
:: 设置代码页为 UTF-8
chcp 65001 >nul

setlocal enabledelayedexpansion

:: 设置目标路径和文件类型
set "target_path=dist"
set "file_type=*.gz"

:: 初始化变量
set "latest_file="
set "latest_time="

:: 遍历目标路径下的所有指定类型的文件
for %%F in ("%target_path%\%file_type%") do (
    :: 获取文件的最后修改时间
    for %%T in ("%%~tF") do (
        if not defined latest_time (
            set "latest_time=%%~T"
            set "latest_file=%%~fF"
        ) else (
            :: 比较时间，找到最新的文件
            if "%%~T" gtr "!latest_time!" (
                set "latest_time=%%~T"
                set "latest_file=%%~fF"
            )
        )
    )
)

:: 输出结果
if defined latest_file (
    echo 最新的构建是: !latest_file!
    echo 最后修改时间: !latest_time!
    .venv\Scripts\twine upload "%latest_file%" --config-file .pypirc
) else (
    echo 未找到任何构建。
    pause
)

