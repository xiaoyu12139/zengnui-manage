# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'card_quick_option_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_CardQuickOptionWidget(object):
    def setupUi(self, CardQuickOptionWidget):
        if not CardQuickOptionWidget.objectName():
            CardQuickOptionWidget.setObjectName(u"CardQuickOptionWidget")
        CardQuickOptionWidget.resize(400, 300)
        self.verticalLayout = QVBoxLayout(CardQuickOptionWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.titleWidget = QWidget(CardQuickOptionWidget)
        self.titleWidget.setObjectName(u"titleWidget")
        self.titleWidget.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout = QHBoxLayout(self.titleWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.card1Title = QLabel(self.titleWidget)
        self.card1Title.setObjectName(u"card1Title")

        self.horizontalLayout.addWidget(self.card1Title)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addWidget(self.titleWidget)

        self.pushButton_2 = QPushButton(CardQuickOptionWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(CardQuickOptionWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_3 = QPushButton(CardQuickOptionWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.verticalLayout.addWidget(self.pushButton_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(CardQuickOptionWidget)

        QMetaObject.connectSlotsByName(CardQuickOptionWidget)
    # setupUi

    def retranslateUi(self, CardQuickOptionWidget):
        CardQuickOptionWidget.setWindowTitle(QCoreApplication.translate("CardQuickOptionWidget", u"Form", None))
        self.card1Title.setText(QCoreApplication.translate("CardQuickOptionWidget", u"\u5feb\u901f\u64cd\u4f5c", None))
        self.pushButton_2.setText(QCoreApplication.translate("CardQuickOptionWidget", u"PushButton", None))
        self.pushButton.setText(QCoreApplication.translate("CardQuickOptionWidget", u"PushButton", None))
        self.pushButton_3.setText(QCoreApplication.translate("CardQuickOptionWidget", u"PushButton", None))
    # retranslateUi

