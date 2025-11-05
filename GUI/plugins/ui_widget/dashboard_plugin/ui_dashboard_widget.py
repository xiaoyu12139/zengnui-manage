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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QSizePolicy, QSpacerItem, QSplitter,
    QVBoxLayout, QWidget)

class Ui_DashboardWidget(object):
    def setupUi(self, DashboardWidget):
        if not DashboardWidget.objectName():
            DashboardWidget.setObjectName(u"DashboardWidget")
        DashboardWidget.resize(441, 265)
        self.verticalLayout = QVBoxLayout(DashboardWidget)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.headerLayout = QHBoxLayout()
        self.headerLayout.setObjectName(u"headerLayout")
        self.headerLayout.setContentsMargins(12, 12, 12, 0)
        self.titleLabel = QLabel(DashboardWidget)
        self.titleLabel.setObjectName(u"titleLabel")

        self.headerLayout.addWidget(self.titleLabel)

        self.subtitleLabel = QLabel(DashboardWidget)
        self.subtitleLabel.setObjectName(u"subtitleLabel")

        self.headerLayout.addWidget(self.subtitleLabel)

        self.headerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerLayout.addItem(self.headerSpacer)


        self.verticalLayout.addLayout(self.headerLayout)

        self.summaryGrid = QGridLayout()
        self.summaryGrid.setSpacing(8)
        self.summaryGrid.setObjectName(u"summaryGrid")
        self.summaryGrid.setContentsMargins(12, 0, 12, 0)
        self.card1 = QFrame(DashboardWidget)
        self.card1.setObjectName(u"card1")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.card1.sizePolicy().hasHeightForWidth())
        self.card1.setSizePolicy(sizePolicy)
        self.card1.setFrameShape(QFrame.StyledPanel)
        self.card1Layout = QVBoxLayout(self.card1)
        self.card1Layout.setObjectName(u"card1Layout")
        self.card1Layout.setContentsMargins(12, 12, 12, 12)
        self.card1Header = QHBoxLayout()
        self.card1Header.setObjectName(u"card1Header")
        self.card1Icon = QLabel(self.card1)
        self.card1Icon.setObjectName(u"card1Icon")

        self.card1Header.addWidget(self.card1Icon)

        self.card1HeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.card1Header.addItem(self.card1HeaderSpacer)

        self.card1Delta = QLabel(self.card1)
        self.card1Delta.setObjectName(u"card1Delta")

        self.card1Header.addWidget(self.card1Delta)


        self.card1Layout.addLayout(self.card1Header)

        self.card1Value = QLabel(self.card1)
        self.card1Value.setObjectName(u"card1Value")

        self.card1Layout.addWidget(self.card1Value)

        self.card1Label = QLabel(self.card1)
        self.card1Label.setObjectName(u"card1Label")

        self.card1Layout.addWidget(self.card1Label)


        self.summaryGrid.addWidget(self.card1, 0, 0, 1, 1)

        self.card2 = QFrame(DashboardWidget)
        self.card2.setObjectName(u"card2")
        sizePolicy.setHeightForWidth(self.card2.sizePolicy().hasHeightForWidth())
        self.card2.setSizePolicy(sizePolicy)
        self.card2.setFrameShape(QFrame.StyledPanel)
        self.card2Layout = QVBoxLayout(self.card2)
        self.card2Layout.setObjectName(u"card2Layout")
        self.card2Layout.setContentsMargins(12, 12, 12, 12)
        self.card2Header = QHBoxLayout()
        self.card2Header.setObjectName(u"card2Header")
        self.card2Icon = QLabel(self.card2)
        self.card2Icon.setObjectName(u"card2Icon")

        self.card2Header.addWidget(self.card2Icon)

        self.card2HeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.card2Header.addItem(self.card2HeaderSpacer)

        self.card2Delta = QLabel(self.card2)
        self.card2Delta.setObjectName(u"card2Delta")

        self.card2Header.addWidget(self.card2Delta)


        self.card2Layout.addLayout(self.card2Header)

        self.card2Value = QLabel(self.card2)
        self.card2Value.setObjectName(u"card2Value")

        self.card2Layout.addWidget(self.card2Value)

        self.card2Label = QLabel(self.card2)
        self.card2Label.setObjectName(u"card2Label")

        self.card2Layout.addWidget(self.card2Label)


        self.summaryGrid.addWidget(self.card2, 0, 1, 1, 1)

        self.card3 = QFrame(DashboardWidget)
        self.card3.setObjectName(u"card3")
        sizePolicy.setHeightForWidth(self.card3.sizePolicy().hasHeightForWidth())
        self.card3.setSizePolicy(sizePolicy)
        self.card3.setFrameShape(QFrame.StyledPanel)
        self.card3Layout = QVBoxLayout(self.card3)
        self.card3Layout.setObjectName(u"card3Layout")
        self.card3Layout.setContentsMargins(12, 12, 12, 12)
        self.card3Header = QHBoxLayout()
        self.card3Header.setObjectName(u"card3Header")
        self.card3Icon = QLabel(self.card3)
        self.card3Icon.setObjectName(u"card3Icon")

        self.card3Header.addWidget(self.card3Icon)

        self.card3HeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.card3Header.addItem(self.card3HeaderSpacer)

        self.card3Delta = QLabel(self.card3)
        self.card3Delta.setObjectName(u"card3Delta")

        self.card3Header.addWidget(self.card3Delta)


        self.card3Layout.addLayout(self.card3Header)

        self.card3Value = QLabel(self.card3)
        self.card3Value.setObjectName(u"card3Value")

        self.card3Layout.addWidget(self.card3Value)

        self.card3Label = QLabel(self.card3)
        self.card3Label.setObjectName(u"card3Label")

        self.card3Layout.addWidget(self.card3Label)


        self.summaryGrid.addWidget(self.card3, 1, 0, 1, 1)

        self.card4 = QFrame(DashboardWidget)
        self.card4.setObjectName(u"card4")
        sizePolicy.setHeightForWidth(self.card4.sizePolicy().hasHeightForWidth())
        self.card4.setSizePolicy(sizePolicy)
        self.card4.setFrameShape(QFrame.StyledPanel)
        self.card4Layout = QVBoxLayout(self.card4)
        self.card4Layout.setObjectName(u"card4Layout")
        self.card4Layout.setContentsMargins(12, 12, 12, 12)
        self.card4Header = QHBoxLayout()
        self.card4Header.setObjectName(u"card4Header")
        self.card4Icon = QLabel(self.card4)
        self.card4Icon.setObjectName(u"card4Icon")

        self.card4Header.addWidget(self.card4Icon)

        self.card4HeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.card4Header.addItem(self.card4HeaderSpacer)

        self.card4Delta = QLabel(self.card4)
        self.card4Delta.setObjectName(u"card4Delta")

        self.card4Header.addWidget(self.card4Delta)


        self.card4Layout.addLayout(self.card4Header)

        self.card4Value = QLabel(self.card4)
        self.card4Value.setObjectName(u"card4Value")

        self.card4Layout.addWidget(self.card4Value)

        self.card4Label = QLabel(self.card4)
        self.card4Label.setObjectName(u"card4Label")

        self.card4Layout.addWidget(self.card4Label)


        self.summaryGrid.addWidget(self.card4, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.summaryGrid)

        self.contentSplitter = QSplitter(DashboardWidget)
        self.contentSplitter.setObjectName(u"contentSplitter")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.contentSplitter.sizePolicy().hasHeightForWidth())
        self.contentSplitter.setSizePolicy(sizePolicy1)
        self.contentSplitter.setOrientation(Qt.Horizontal)
        self.contentSplitter.setHandleWidth(6)
        self.chartFrame1 = QFrame(self.contentSplitter)
        self.chartFrame1.setObjectName(u"chartFrame1")
        self.chartFrame1.setFrameShape(QFrame.StyledPanel)
        self.chartInnerLayout1 = QVBoxLayout(self.chartFrame1)
        self.chartInnerLayout1.setObjectName(u"chartInnerLayout1")
        self.chartInnerLayout1.setContentsMargins(12, 12, 12, 12)
        self.chartPlaceholder1 = QLabel(self.chartFrame1)
        self.chartPlaceholder1.setObjectName(u"chartPlaceholder1")
        self.chartPlaceholder1.setAlignment(Qt.AlignCenter)

        self.chartInnerLayout1.addWidget(self.chartPlaceholder1)

        self.contentSplitter.addWidget(self.chartFrame1)
        self.chartFrame2 = QFrame(self.contentSplitter)
        self.chartFrame2.setObjectName(u"chartFrame2")
        self.chartFrame2.setFrameShape(QFrame.StyledPanel)
        self.chartInnerLayout2 = QVBoxLayout(self.chartFrame2)
        self.chartInnerLayout2.setObjectName(u"chartInnerLayout2")
        self.chartInnerLayout2.setContentsMargins(12, 12, 12, 12)
        self.chartPlaceholder2 = QLabel(self.chartFrame2)
        self.chartPlaceholder2.setObjectName(u"chartPlaceholder2")
        self.chartPlaceholder2.setAlignment(Qt.AlignCenter)

        self.chartInnerLayout2.addWidget(self.chartPlaceholder2)

        self.contentSplitter.addWidget(self.chartFrame2)

        self.verticalLayout.addWidget(self.contentSplitter)


        self.retranslateUi(DashboardWidget)

        QMetaObject.connectSlotsByName(DashboardWidget)
    # setupUi

    def retranslateUi(self, DashboardWidget):
        DashboardWidget.setWindowTitle(QCoreApplication.translate("DashboardWidget", u"Dashboard", None))
        self.titleLabel.setText(QCoreApplication.translate("DashboardWidget", u"\u4eea\u8868\u76d8\u6982\u89c8", None))
        self.subtitleLabel.setText(QCoreApplication.translate("DashboardWidget", u"\u5b9e\u65f6\u76d1\u63a7\u8fd0\u8425\u6570\u636e\u4e0e\u7cfb\u7edf\u72b6\u6001", None))
        self.card1Icon.setText("")
        self.card1Delta.setText(QCoreApplication.translate("DashboardWidget", u"+12.5%", None))
        self.card1Value.setText(QCoreApplication.translate("DashboardWidget", u"\u00a5245,680", None))
        self.card1Label.setText(QCoreApplication.translate("DashboardWidget", u"\u6536\u5165", None))
        self.card2Icon.setText("")
        self.card2Delta.setText(QCoreApplication.translate("DashboardWidget", u"+8.2%", None))
        self.card2Value.setText(QCoreApplication.translate("DashboardWidget", u"8,234", None))
        self.card2Label.setText(QCoreApplication.translate("DashboardWidget", u"\u6d3b\u8dc3\u7528\u6237", None))
        self.card3Icon.setText("")
        self.card3Delta.setText(QCoreApplication.translate("DashboardWidget", u"-3.1%", None))
        self.card3Value.setText(QCoreApplication.translate("DashboardWidget", u"1,432", None))
        self.card3Label.setText(QCoreApplication.translate("DashboardWidget", u"\u8ba2\u5355\u6570\u91cf", None))
        self.card4Icon.setText("")
        self.card4Delta.setText(QCoreApplication.translate("DashboardWidget", u"+2.4%", None))
        self.card4Value.setText(QCoreApplication.translate("DashboardWidget", u"94.2%", None))
        self.card4Label.setText(QCoreApplication.translate("DashboardWidget", u"\u7cfb\u7edf\u7a33\u5b9a\u5ea6", None))
        self.chartPlaceholder1.setText(QCoreApplication.translate("DashboardWidget", u"\u6536\u5165\u4e0e\u652f\u51fa\u8d8b\u52bf\uff08\u5360\u4f4d\uff09", None))
        self.chartPlaceholder2.setText(QCoreApplication.translate("DashboardWidget", u"\u7528\u6237\u6d3b\u8dc3\u5ea6\uff08\u5360\u4f4d\uff09", None))
    # retranslateUi

