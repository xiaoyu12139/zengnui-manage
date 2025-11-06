# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'card_demo01_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QRadioButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_CardDemo01Widget(object):
    def setupUi(self, CardDemo01Widget):
        if not CardDemo01Widget.objectName():
            CardDemo01Widget.setObjectName(u"CardDemo01Widget")
        CardDemo01Widget.resize(400, 300)
        self.verticalLayout = QVBoxLayout(CardDemo01Widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.titleWidget = QWidget(CardDemo01Widget)
        self.titleWidget.setObjectName(u"titleWidget")
        self.titleWidget.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout = QHBoxLayout(self.titleWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.titleWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer_5 = QSpacerItem(319, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addWidget(self.titleWidget)

        self.widget_2 = QWidget(CardDemo01Widget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.horizontalSpacer_6 = QSpacerItem(206, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)

        self.radioButton = QRadioButton(self.widget_2)
        self.radioButton.setObjectName(u"radioButton")

        self.horizontalLayout_2.addWidget(self.radioButton)


        self.verticalLayout.addWidget(self.widget_2)

        self.widget_3 = QWidget(CardDemo01Widget)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget_4 = QWidget(self.widget_3)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.widget_4)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addWidget(self.widget_4)

        self.comboBox = QComboBox(self.widget_3)
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout_2.addWidget(self.comboBox)


        self.verticalLayout.addWidget(self.widget_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(CardDemo01Widget)

        QMetaObject.connectSlotsByName(CardDemo01Widget)
    # setupUi

    def retranslateUi(self, CardDemo01Widget):
        CardDemo01Widget.setWindowTitle(QCoreApplication.translate("CardDemo01Widget", u"Form", None))
        self.label.setText(QCoreApplication.translate("CardDemo01Widget", u"demo01", None))
        self.label_3.setText(QCoreApplication.translate("CardDemo01Widget", u"TextLabel", None))
        self.radioButton.setText(QCoreApplication.translate("CardDemo01Widget", u"RadioButton", None))
        self.label_4.setText(QCoreApplication.translate("CardDemo01Widget", u"TextLabel", None))
    # retranslateUi

