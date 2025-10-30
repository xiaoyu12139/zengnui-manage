# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'status_bar_widget.ui'
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
    QSpacerItem, QWidget)

class Ui_StatusBarWidget(object):
    def setupUi(self, StatusBarWidget):
        if not StatusBarWidget.objectName():
            StatusBarWidget.setObjectName(u"StatusBarWidget")
        StatusBarWidget.resize(591, 38)
        self.horizontalLayout = QHBoxLayout(StatusBarWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.status_label = QLabel(StatusBarWidget)
        self.status_label.setObjectName(u"status_label")

        self.horizontalLayout.addWidget(self.status_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.retranslateUi(StatusBarWidget)

        QMetaObject.connectSlotsByName(StatusBarWidget)
    # setupUi

    def retranslateUi(self, StatusBarWidget):
        StatusBarWidget.setWindowTitle(QCoreApplication.translate("StatusBarWidget", u"Form", None))
        self.status_label.setText(QCoreApplication.translate("StatusBarWidget", u"\u51c6\u5907\u5c31\u7eea", None))
    # retranslateUi

