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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_DashboardWidget(object):
    def setupUi(self, DashboardWidget):
        if not DashboardWidget.objectName():
            DashboardWidget.setObjectName(u"DashboardWidget")
        DashboardWidget.resize(525, 307)
        self.verticalLayout = QVBoxLayout(DashboardWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.topWidget = QWidget(DashboardWidget)
        self.topWidget.setObjectName(u"topWidget")
        self.topWidget.setMaximumSize(QSize(16777215, 100))
        self.verticalLayout_2 = QVBoxLayout(self.topWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget = QWidget(self.topWidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pageTitle = QLabel(self.widget)
        self.pageTitle.setObjectName(u"pageTitle")

        self.horizontalLayout.addWidget(self.pageTitle)

        self.horizontalSpacer = QSpacerItem(414, 17, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addWidget(self.widget)

        self.widget_2 = QWidget(self.topWidget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pageDesc = QLabel(self.widget_2)
        self.pageDesc.setObjectName(u"pageDesc")

        self.horizontalLayout_2.addWidget(self.pageDesc)

        self.horizontalSpacer_2 = QSpacerItem(354, 17, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addWidget(self.widget_2)


        self.verticalLayout.addWidget(self.topWidget)

        self.contentWidget = QWidget(DashboardWidget)
        self.contentWidget.setObjectName(u"contentWidget")

        self.verticalLayout.addWidget(self.contentWidget)


        self.retranslateUi(DashboardWidget)

        QMetaObject.connectSlotsByName(DashboardWidget)
    # setupUi

    def retranslateUi(self, DashboardWidget):
        DashboardWidget.setWindowTitle(QCoreApplication.translate("DashboardWidget", u"Dashboard", None))
        self.pageTitle.setText(QCoreApplication.translate("DashboardWidget", u"\u63a7\u5236\u9762\u677f", None))
        self.pageDesc.setText(QCoreApplication.translate("DashboardWidget", u"\u7cfb\u7edf\u76d1\u63a7\u4e0e\u914d\u7f6e\u7ba1\u7406", None))
    # retranslateUi

