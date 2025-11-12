# 内部包
# 外部包
placeholder_import_start = "######import_start######"
placeholder_import_end = "######import_end######"
placeholder_constructor_start = "######constructor_start######"
placeholder_constructor_end = "######constructor_end######"
placeholder_ui_start = "######ui_start######"
placeholder_ui_end = "######ui_end######"
placeholder_view_start = "######view_start######"
placeholder_view_end = "######view_end######"
placeholder_viewmodel_start = "######viewmodel_start######"
placeholder_viewmodel_end = "######viewmodel_end######"

placeholder_plugin_init_start = "######plugin_init_start######"
placeholder_plugin_init_end = "######plugin_init_end######"
placeholder_plugin_initialize_start = "######plugin_initialize_start######"
placeholder_plugin_initialize_end = "######plugin_initialize_end######"
placeholder_plugin_assembled_start = "######plugin_assembled_start######"
placeholder_plugin_assembled_end = "######plugin_assembled_end######"
placeholder_vmbuild_method_start = "######vmbuild_method_start######"
placeholder_vmbuild_method_end = "######vmbuild_method_end######"

context = {
    "plugin_main_feat": True,
    "plugin_name": "",
    "PluginName": "",
    "feat_name": "",
    "FeatName": "",
    # 导包占位符
    "placeholder_import_start": placeholder_import_start,
    "placeholder_import_end": placeholder_import_end,
    "placeholder_constructor_start": placeholder_constructor_start,
    "placeholder_constructor_end": placeholder_constructor_end,
    "placeholder_ui_start": placeholder_ui_start,
    "placeholder_ui_end": placeholder_ui_end,
    "placeholder_view_start": placeholder_view_start,
    "placeholder_view_end": placeholder_view_end,
    "placeholder_viewmodel_start": placeholder_viewmodel_start,
    "placeholder_viewmodel_end": placeholder_viewmodel_end,
    # plugin文件占位符
    "placeholder_plugin_init_start": placeholder_plugin_init_start,
    "placeholder_plugin_init_end": placeholder_plugin_init_end,
    "placeholder_plugin_initialize_start": placeholder_plugin_initialize_start,
    "placeholder_plugin_initialize_end": placeholder_plugin_initialize_end,
    "placeholder_plugin_assembled_start": placeholder_plugin_assembled_start,
    "placeholder_plugin_assembled_end": placeholder_plugin_assembled_end,
    # vmbuild方法占位符
    "placeholder_vmbuild_method_start": placeholder_vmbuild_method_start,
    "placeholder_vmbuild_method_end": placeholder_vmbuild_method_end,
}

placeholder_import_seq = [
    "placeholder_import_start",
    "placeholder_constructor_start",
    "placeholder_constructor_end",
    "placeholder_ui_start",
    "placeholder_ui_end",
    "placeholder_view_start",
    "placeholder_view_end",
    "placeholder_viewmodel_start",
    "placeholder_viewmodel_end",
    "placeholder_import_end"
]

placeholder_plugin_init_seq = [
    "placeholder_plugin_init_start",
    "placeholder_plugin_init_end"
]

placeholder_plugin_initialize_seq = [
    "placeholder_plugin_initialize_start",
    "placeholder_plugin_initialize_end"
]

placeholder_plugin_assembled_seq = [
    "placeholder_plugin_assembled_start",
    "placeholder_plugin_assembled_end"
]

placeholder_vmbuild_method_seq = [
    "placeholder_vmbuild_method_start",
    "placeholder_vmbuild_method_end"
]

def config_create_plugin(plugin_name: str, feat_name: str):
    """
    配置创建插件
    """
    PluginName = ''.join([word.capitalize() for word in plugin_name.split("_")])
    FeatName = ''.join([word.capitalize() for word in feat_name.split("_")])
    context["plugin_name"] = plugin_name
    context["PluginName"] = PluginName
    context["feat_name"] = feat_name
    context["FeatName"] = FeatName
    context["plugin_main_feat"] = True
    return context

def config_add_feat(plugin_name: str, feat_name: str):
    """
    配置添加特性
    """
    PluginName = ''.join([word.capitalize() for word in plugin_name.split("_")])
    FeatName = ''.join([word.capitalize() for word in feat_name.split("_")])
    context["plugin_name"] = plugin_name
    context["PluginName"] = PluginName
    context["feat_name"] = feat_name
    context["FeatName"] = FeatName
    context["plugin_main_feat"] = False
    return context

def config_del_feat(plugin_name: str, feat_name: str):
    """
    配置删除特性
    """
    PluginName = ''.join([word.capitalize() for word in plugin_name.split("_")])
    FeatName = ''.join([word.capitalize() for word in feat_name.split("_")])
    context["plugin_name"] = plugin_name
    context["PluginName"] = PluginName
    context["feat_name"] = feat_name
    context["FeatName"] = FeatName
    context["plugin_main_feat"] = False
    return context