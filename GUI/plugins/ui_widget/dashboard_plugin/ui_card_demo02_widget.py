# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'card_demo02_widget.ui'
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

class Ui_CardDemo02Widget(object):
    def setupUi(self, CardDemo02Widget):
        if not CardDemo02Widget.objectName():
            CardDemo02Widget.setObjectName(u"CardDemo02Widget")
        CardDemo02Widget.resize(400, 300)
        self.verticalLayout = QVBoxLayout(CardDemo02Widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.titleWidgetSXF = QWidget(CardDemo02Widget)
        self.titleWidgetSXF.setObjectName(u"titleWidgetSXF")
        self.titleWidgetSXF.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout = QHBoxLayout(self.titleWidgetSXF)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.titleWidgetSXF)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addWidget(self.titleWidgetSXF)

        self.widget_4 = QWidget(CardDemo02Widget)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_2 = QVBoxLayout(self.widget_4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget_3 = QWidget(self.widget_4)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_6 = QLabel(self.widget_3)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_2.addWidget(self.label_6)

        self.horizontalSpacer_7 = QSpacerItem(283, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_7)


        self.verticalLayout_2.addWidget(self.widget_3)

        self.horizontalSlider = QSlider(self.widget_4)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.verticalLayout_2.addWidget(self.horizontalSlider)


        self.verticalLayout.addWidget(self.widget_4)

        self.widget_5 = QWidget(CardDemo02Widget)
        self.widget_5.setObjectName(u"widget_5")
        self.verticalLayout_3 = QVBoxLayout(self.widget_5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.widget_2 = QWidget(self.widget_5)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_5 = QLabel(self.widget_2)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.horizontalSpacer_8 = QSpacerItem(283, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_8)


        self.verticalLayout_3.addWidget(self.widget_2)

        self.horizontalSlider_2 = QSlider(self.widget_5)
        self.horizontalSlider_2.setObjectName(u"horizontalSlider_2")
        self.horizontalSlider_2.setOrientation(Qt.Horizontal)

        self.verticalLayout_3.addWidget(self.horizontalSlider_2)


        self.verticalLayout.addWidget(self.widget_5)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(CardDemo02Widget)

        QMetaObject.connectSlotsByName(CardDemo02Widget)
    # setupUi

    def retranslateUi(self, CardDemo02Widget):
        CardDemo02Widget.setWindowTitle(QCoreApplication.translate("CardDemo02Widget", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("CardDemo02Widget", u"TextLabel", None))
        self.label_6.setText(QCoreApplication.translate("CardDemo02Widget", u"TextLabel", None))
        self.label_5.setText(QCoreApplication.translate("CardDemo02Widget", u"TextLabel", None))
    # retranslateUi

