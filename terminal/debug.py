from pathlib import Path

import py_plugin_tools.ops_create_plugin as test

if __name__ == "__main__":
    plugin_dir = Path(r"C:\Users\user1\Desktop\Code\test")
    plugin_name = "test_demo"
    feat_name = "feat_demo"
    test.create_plugin(plugin_dir, plugin_name, feat_name)