@echo off
chcp 65001 >nul
setlocal

set "ROOT=%~dp0.."
set "CACHE_DIR=%USERPROFILE%\.zengnui_manage\python_cache"

echo [1/3] Create cache directory: "%CACHE_DIR%"
if not exist "%CACHE_DIR%" (
    mkdir "%CACHE_DIR%"
    echo Cache directory created successfully.
) else (
    echo Cache directory already exists.
)

echo.
echo [2/3] Set PYTHONPYCACHEPREFIX environment variable
setx PYTHONPYCACHEPREFIX "%CACHE_DIR%" >nul
if %errorlevel% equ 0 (
    echo Environment variable set successfully.
    echo Note: Please restart your terminal for the change to take effect.
) else (
    echo Failed to set environment variable.
    exit /b 1
)

echo.
echo [3/3] Install dependencies

if exist "%ROOT%GUI\requirement.txt" (
  echo  - Installing GUI requirements
  pip install -r "%ROOT%GUI\requirement.txt"
)
if exist "%ROOT%server\requirements.txt" (
  echo  - Installing server requirements
  pip install -r "%ROOT%server\requirements.txt"
)
if exist "%ROOT%terminal\requirement.txt" (
  echo  - Installing terminal requirements
  pip install -r "%ROOT%terminal\requirement.txt"
)

echo.
echo [DONE] Environment configured.
echo  - Please reopen your terminal for PYTHONPYCACHEPREFIX to take effect globally.
echo  - To run GUI:
echo      "%ROOT%.venv\Scripts\python.exe" GUI\launcher.py
echo  - Or (without reopening terminal), run with explicit prefix:
echo      python -X pycache_prefix="%CACHE_DIR%" GUI\launcher.py

:done
endlocal
exit /b 0