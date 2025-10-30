# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'top_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_TopWidget(object):
    def setupUi(self, TopWidget):
        if not TopWidget.objectName():
            TopWidget.setObjectName(u"TopWidget")
        TopWidget.resize(719, 54)
        self.verticalLayout = QVBoxLayout(TopWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
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
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.icon_night = QLabel(self.icon_widget)
        self.icon_night.setObjectName(u"icon_night")

        self.horizontalLayout.addWidget(self.icon_night)

        self.icon_diaginostics = QLabel(self.icon_widget)
        self.icon_diaginostics.setObjectName(u"icon_diaginostics")

        self.horizontalLayout.addWidget(self.icon_diaginostics)

        self.icon_min = QLabel(self.icon_widget)
        self.icon_min.setObjectName(u"icon_min")

        self.horizontalLayout.addWidget(self.icon_min)

        self.icon_max = QLabel(self.icon_widget)
        self.icon_max.setObjectName(u"icon_max")

        self.horizontalLayout.addWidget(self.icon_max)

        self.icon_close = QLabel(self.icon_widget)
        self.icon_close.setObjectName(u"icon_close")

        self.horizontalLayout.addWidget(self.icon_close)


        self.horizontalLayout_2.addWidget(self.icon_widget)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(TopWidget)

        QMetaObject.connectSlotsByName(TopWidget)
    # setupUi

    def retranslateUi(self, TopWidget):
        TopWidget.setWindowTitle(QCoreApplication.translate("TopWidget", u"Form", None))
        self.top_theme.setText(QCoreApplication.translate("TopWidget", u"Zengnui Manage", None))
        self.icon_night.setText(QCoreApplication.translate("TopWidget", u"night", None))
        self.icon_diaginostics.setText(QCoreApplication.translate("TopWidget", u"diaginostics", None))
        self.icon_min.setText(QCoreApplication.translate("TopWidget", u"min", None))
        self.icon_max.setText(QCoreApplication.translate("TopWidget", u"max", None))
        self.icon_close.setText(QCoreApplication.translate("TopWidget", u"close", None))
    # retranslateUi

