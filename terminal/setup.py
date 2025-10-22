# 执行 pip install -e . 后在任意终端都能执行mycli命令
# setup.py
# pip install -e .
from setuptools import setup,find_packages

# blue 为提示信息，green 为成功信息，red 为error信息，yellow 为警告信息

setup(
    name="zengnui-cli",
    version="0.1",
    packages=find_packages(include=["change_dir", "public"]),
    install_requires=["click", "questionary"],
    entry_points={
        "console_scripts": [
            "update-change-dir=change_dir.main:main",
            "clash-proxy=clash.terminal_proxy:cli_proxy",
        ],
    },
)
