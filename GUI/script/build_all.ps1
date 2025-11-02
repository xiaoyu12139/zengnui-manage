# 获取当前脚本所在目录
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
# 调用python执行compile_ui.py
python $scriptDir\compile_ui.py
# 调用python执行compile_img_qrc.py
python $scriptDir\compile_img_qrc.py
