@echo off
chcp 65001
echo ====================================
echo     文件监控服务管理工具
echo ====================================
echo.
echo 请选择操作:
echo 1. 安装服务
echo 2. 启动服务
echo 3. 停止服务
echo 4. 卸载服务
echo 5. 查看服务状态
echo 6. 以调试模式运行
echo 0. 退出
echo.
set /p choice=请输入选项 (0-6): 

if "%choice%"=="1" goto install
if "%choice%"=="2" goto start
if "%choice%"=="3" goto stop
if "%choice%"=="4" goto uninstall
if "%choice%"=="5" goto status
if "%choice%"=="6" goto debug
if "%choice%"=="0" goto exit
goto menu

:install
echo.
echo 正在安装文件监控服务...
python main.py install
if %errorlevel% equ 0 (
    echo 服务安装成功！
) else (
    echo 服务安装失败！请检查是否以管理员身份运行。
)
pause
goto menu

:start
echo.
echo 正在启动文件监控服务...
python main.py start
if %errorlevel% equ 0 (
    echo 服务启动成功！
) else (
    echo 服务启动失败！
)
pause
goto menu

:stop
echo.
echo 正在停止文件监控服务...
python main.py stop
if %errorlevel% equ 0 (
    echo 服务停止成功！
) else (
    echo 服务停止失败！
)
pause
goto menu

:uninstall
echo.
echo 正在卸载文件监控服务...
python main.py remove
if %errorlevel% equ 0 (
    echo 服务卸载成功！
) else (
    echo 服务卸载失败！
)
pause
goto menu

:status
echo.
echo 查看服务状态...
sc query FileMonitorService
pause
goto menu

:debug
echo.
echo 以调试模式运行文件监控服务...
echo 按 Ctrl+C 停止服务
python main.py
pause
goto menu

:menu
cls
goto start_menu

:start_menu
echo ====================================
echo     文件监控服务管理工具
echo ====================================
echo.
echo 请选择操作:
echo 1. 安装服务
echo 2. 启动服务
echo 3. 停止服务
echo 4. 卸载服务
echo 5. 查看服务状态
echo 6. 以调试模式运行
echo 0. 退出
echo.
set /p choice=请输入选项 (0-6): 

if "%choice%"=="1" goto install
if "%choice%"=="2" goto start
if "%choice%"=="3" goto stop
if "%choice%"=="4" goto uninstall
if "%choice%"=="5" goto status
if "%choice%"=="6" goto debug
if "%choice%"=="0" goto exit
goto start_menu

:exit
echo 再见！
exit