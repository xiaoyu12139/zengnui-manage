from pathlib import Path

def test_create_plugin():
    import py_plugin_tools.ops_create_plugin as test
    plugin_dir = Path(r"C:\Users\user1\Desktop\Code\test")
    plugin_name = "test_demo"
    feat_name = "feat_demo"
    test.create_plugin(plugin_dir, plugin_name, feat_name)

def test_add_feat():
    import py_plugin_tools.ops_add_feat as test
    plugin_dir = Path(r"C:\Users\user1\Desktop\Code\test")
    plugin_name = "test_demo"
    feat_name = "feat_demo1"
    test.add_plugin_feat(plugin_dir, plugin_name, feat_name)

if __name__ == "__main__":
    test_create_plugin()
    test_add_feat()