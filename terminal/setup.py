# 执行 pip install -e . 后在任意终端都能执行mycli命令
# setup.py
# pip install -e .
# python -m pip install -e . --config-settings editable_mode=compat
from setuptools import setup,find_packages

# blue 为提示信息，green 为成功信息，red 为error信息，yellow 为警告信息

setup(
    name="zengnui-cli",
    version="0.1",
    packages=find_packages(include=["change_dir", "public"]),
    install_requires=["click", "questionary"],
    entry_points={
        "console_scripts": [
            # command_alias 中的命令
            "alias=command_alias.main:cli",
            "clear-all-alias=command_alias.main:reset_all",
            # change_dir 中的命令
            "update-change-dir=change_dir.main:main",
            # clash中的命令
            "update-clash-proxy=clash.terminal_proxy:cli_proxy_config",
            "proxy=clash.terminal_proxy:cli_proxy",
            # update_config 中的命令
            "update-all-config=update_config.main:update_all_configurations",
            # py_plugin_tools 中的命令
            "py-plugin-tools=py_plugin_tools.main:main",
        ],
    },
)
