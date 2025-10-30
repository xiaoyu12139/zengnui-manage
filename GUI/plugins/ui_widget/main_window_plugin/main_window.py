# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 596)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.top_widget = QWidget(self.centralwidget)
        self.top_widget.setObjectName(u"top_widget")
        self.top_widget.setMinimumSize(QSize(0, 50))
        self.top_widget.setMaximumSize(QSize(16777215, 50))

        self.verticalLayout.addWidget(self.top_widget)

        self.center_widget = QWidget(self.centralwidget)
        self.center_widget.setObjectName(u"center_widget")
        self.horizontalLayout = QHBoxLayout(self.center_widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.verticalLayout.addWidget(self.center_widget)

        self.bottom_widget = QWidget(self.centralwidget)
        self.bottom_widget.setObjectName(u"bottom_widget")
        self.bottom_widget.setMinimumSize(QSize(0, 30))
        self.bottom_widget.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout.addWidget(self.bottom_widget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
    # retranslateUi

