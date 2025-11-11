# 内部包
from public import *
# 外部包
from pathlib import Path
import re

def create_plugin(plugin_dir: Path, plugin_name: str, feat_name: str):
    if not plugin_dir.exists():
        ERROR(f"插件目录 {plugin_dir} 不存在")
        return
    # 判断plugin_name与feat_name是否是蛇形小写
    snake_pattern = re.compile(r'^[a-z]+(_[a-z]+)*$')
    if not snake_pattern.match(plugin_name):
        ERROR(f"插件名 {plugin_name} 不是蛇形小写")
        return
    if not snake_pattern.match(feat_name):
        ERROR(f"特性名 {feat_name} 不是蛇形小写")
        return
    PluginName = ''.join([word.capitalize() for word in plugin_name.split("_")])
    FeatName = ''.join([word.capitalize() for word in feat_name.split("_")])
    context = {
        "plugin_name": plugin_name,
        "PluginName": PluginName,
        "feat_name": plugin_name,
        "FeatName": FeatName,
    }
    INFO(f"基于context: {context}创建插件")

if __name__ == "__main__":
    plugin_dir = Path(r"C:\Users\user1\Desktop\Code\zengnui-manage\GUI\plugins")
    plugin_name = "test_demo"
    feat_name = "feat_demo"
    create_plugin(plugin_dir, plugin_name, feat_name)