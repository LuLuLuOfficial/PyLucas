@echo off
chcp 65001

cd ..\..\
echo 工作路径为: %cd%
echo 开始尝试 build
poetry build

pause