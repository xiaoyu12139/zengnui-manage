# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'card_resource_widget.ui'
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
    QSlider, QSpacerItem, QVBoxLayout, QWidget)

class Ui_CardResourceWidget(object):
    def setupUi(self, CardResourceWidget):
        if not CardResourceWidget.objectName():
            CardResourceWidget.setObjectName(u"CardResourceWidget")
        CardResourceWidget.resize(400, 297)
        self.verticalLayout = QVBoxLayout(CardResourceWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(CardResourceWidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_9 = QLabel(self.widget)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout.addWidget(self.label_9)

        self.horizontalSpacer_9 = QSpacerItem(277, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_9)


        self.verticalLayout.addWidget(self.widget)

        self.widget_3 = QWidget(CardResourceWidget)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget_2 = QWidget(self.widget_3)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_7 = QLabel(self.widget_2)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_2.addWidget(self.label_7)

        self.horizontalSpacer = QSpacerItem(283, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addWidget(self.widget_2)

        self.horizontalSlider_3 = QSlider(self.widget_3)
        self.horizontalSlider_3.setObjectName(u"horizontalSlider_3")
        self.horizontalSlider_3.setOrientation(Qt.Horizontal)

        self.verticalLayout_2.addWidget(self.horizontalSlider_3)


        self.verticalLayout.addWidget(self.widget_3)

        self.widget_4 = QWidget(CardResourceWidget)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_4 = QVBoxLayout(self.widget_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.widget_6 = QWidget(self.widget_4)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_10 = QLabel(self.widget_6)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_4.addWidget(self.label_10)

        self.horizontalSpacer_3 = QSpacerItem(283, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.verticalLayout_4.addWidget(self.widget_6)

        self.horizontalSlider_5 = QSlider(self.widget_4)
        self.horizontalSlider_5.setObjectName(u"horizontalSlider_5")
        self.horizontalSlider_5.setOrientation(Qt.Horizontal)

        self.verticalLayout_4.addWidget(self.horizontalSlider_5)


        self.verticalLayout.addWidget(self.widget_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(CardResourceWidget)

        QMetaObject.connectSlotsByName(CardResourceWidget)
    # setupUi

    def retranslateUi(self, CardResourceWidget):
        CardResourceWidget.setWindowTitle(QCoreApplication.translate("CardResourceWidget", u"Form", None))
        self.label_9.setText(QCoreApplication.translate("CardResourceWidget", u"resourceTitle", None))
        self.label_7.setText(QCoreApplication.translate("CardResourceWidget", u"TextLabel", None))
        self.label_10.setText(QCoreApplication.translate("CardResourceWidget", u"TextLabel", None))
    # retranslateUi

