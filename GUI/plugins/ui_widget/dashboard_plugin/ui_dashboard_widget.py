# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dashboard_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QWidget)

class Ui_DashboardWidget(object):
    def setupUi(self, DashboardWidget):
        if not DashboardWidget.objectName():
            DashboardWidget.setObjectName(u"DashboardWidget")
        DashboardWidget.resize(400, 300)
        self.label = QLabel(DashboardWidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(160, 130, 54, 12))

        self.retranslateUi(DashboardWidget)

        QMetaObject.connectSlotsByName(DashboardWidget)
    # setupUi

    def retranslateUi(self, DashboardWidget):
        DashboardWidget.setWindowTitle(QCoreApplication.translate("DashboardWidget", u"Form", None))
        self.label.setText(QCoreApplication.translate("DashboardWidget", u"dashbord", None))
    # retranslateUi

