# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'top_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QToolButton, QVBoxLayout, QWidget)

class Ui_TopWidget(object):
    def setupUi(self, TopWidget):
        if not TopWidget.objectName():
            TopWidget.setObjectName(u"TopWidget")
        TopWidget.resize(700, 24)
        self.verticalLayout = QVBoxLayout(TopWidget)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.top_theme = QLabel(TopWidget)
        self.top_theme.setObjectName(u"top_theme")

        self.horizontalLayout_2.addWidget(self.top_theme)

        self.top_input = QLineEdit(TopWidget)
        self.top_input.setObjectName(u"top_input")

        self.horizontalLayout_2.addWidget(self.top_input)

        self.icon_widget = QWidget(TopWidget)
        self.icon_widget.setObjectName(u"icon_widget")
        self.horizontalLayout = QHBoxLayout(self.icon_widget)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.btn_night = QToolButton(self.icon_widget)
        self.btn_night.setObjectName(u"btn_night")

        self.horizontalLayout.addWidget(self.btn_night)

        self.btn_diaginostics = QToolButton(self.icon_widget)
        self.btn_diaginostics.setObjectName(u"btn_diaginostics")

        self.horizontalLayout.addWidget(self.btn_diaginostics)

        self.btn_min = QToolButton(self.icon_widget)
        self.btn_min.setObjectName(u"btn_min")

        self.horizontalLayout.addWidget(self.btn_min)

        self.btn_max = QToolButton(self.icon_widget)
        self.btn_max.setObjectName(u"btn_max")

        self.horizontalLayout.addWidget(self.btn_max)

        self.btn_close = QToolButton(self.icon_widget)
        self.btn_close.setObjectName(u"btn_close")

        self.horizontalLayout.addWidget(self.btn_close)


        self.horizontalLayout_2.addWidget(self.icon_widget)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(TopWidget)

        QMetaObject.connectSlotsByName(TopWidget)
    # setupUi

    def retranslateUi(self, TopWidget):
        TopWidget.setWindowTitle(QCoreApplication.translate("TopWidget", u"Form", None))
        self.top_theme.setText(QCoreApplication.translate("TopWidget", u"Zengnui Manage", None))
        self.btn_night.setText(QCoreApplication.translate("TopWidget", u"night", None))
        self.btn_diaginostics.setText(QCoreApplication.translate("TopWidget", u"diaginostics", None))
        self.btn_min.setText(QCoreApplication.translate("TopWidget", u"min", None))
        self.btn_max.setText(QCoreApplication.translate("TopWidget", u"max", None))
        self.btn_close.setText(QCoreApplication.translate("TopWidget", u"close", None))
    # retranslateUi

