@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

cd /d "%~dp0..\..\.."
echo Go to the project root directory %cd%
echo.

set "Dir_dist=%cd%\dist"
set "Type_gz=*.gz"
set "Type_whl=*.whl"

set "LatestGz="
set "LatestWhl="
set "GzTicks=0"
set "WhlTicks=0"

for /f "delims=" %%f in ('dir /b /a-d /o-d "%Dir_dist%\%Type_gz%" 2^>nul') do (
    set "LatestGz=%%f"
    goto :break_gz
)
:break_gz
for /f "delims=" %%f in ('dir /b /a-d /o-d "%Dir_dist%\%Type_whl%" 2^>nul') do (
    set "LatestWhl=%%f"
    goto :break_whl
)
:break_whl

echo Latest Package Found:
echo    %LatestGz%
echo    %LatestWhl%
echo.

:ask
set /p answer=Whether to upload the distribution package(yes/no):
if /i "!answer!"=="yes" goto confirm
if /i "!answer!"=="no" goto cancel

echo Please enter valid options (yes/no)
echo.
goto ask

:confirm
echo Start uploading the distribution package...
echo.
poetry publish
goto end

:cancel
echo Cancel uploading the distribution package...
echo.
goto end

:end
pause
endlocal