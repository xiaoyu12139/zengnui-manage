from PySide6.QtXml import QDomDocument
from PySide6.QtCore import QFile, QTextStream

def get_menu_list(xml_path: str) -> list:
    """
    从XML文件中获取菜单列表
    """
    # 加载 XML 文件
    file = QFile(xml_path)
    if not file.open(QFile.ReadOnly | QFile.Text):
        print(f"Cannot open file {xml_path} for reading")
        return []
    # 读取 XML 文件内容
    stream = QTextStream(file)
    xml_content = stream.readAll()
    file.close()
    # 解析 XML 内容
    doc = QDomDocument()
    if not doc.setContent(xml_content):
        print(f"Cannot parse XML content from file {xml_path}")
        return []
    # 获取根元素
    root = doc.documentElement()
    if root.isNull():
        print(f"XML file {xml_path} is empty or invalid")
        return []
    # 获取所有菜单元素
    menu_elements = root.elementsByTagName("menu")
    menu_list = []
    for i in range(menu_elements.length()):
        menu_element = menu_elements.item(i)
        if not menu_element.isNull():
            menu_name = menu_element.attribute("text")
            if menu_name:
                menu_list.append(menu_name)
    return menu_list