from pathlib import Path

def test_create_plugin():
    import pyside_plugin_maker.ops_create_plugin as test
    plugin_dir = Path(r"C:\Users\user1\Desktop\Code\test")
    plugin_name = "test_demo"
    feat_name = "feat_demo"
    test.create_plugin(plugin_dir, plugin_name, feat_name)

def test_add_feat():
    import pyside_plugin_maker.ops_add_plugin_feat as test
    plugin_dir = Path(r"C:\Users\user1\Desktop\Code\test")
    plugin_name = "test"
    feat_name = "demo5"
    test.add_plugin_feat(plugin_dir, plugin_name, feat_name)

def test_del_feat():
    import pyside_plugin_maker.ops_del_plugin_feat as test
    plugin_dir = Path(r"C:\Users\user1\Desktop\Code\test")
    plugin_name = "test"
    feat_name = "demo1"
    test.del_plugin_feat(plugin_dir, plugin_name, feat_name)

if __name__ == "__main__":
    # test_create_plugin()
    test_add_feat()
    # test_del_feat()