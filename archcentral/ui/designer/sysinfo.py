# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sysinfo.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_SysInfo(object):
    def setupUi(self, SysInfo):
        if not SysInfo.objectName():
            SysInfo.setObjectName(u"SysInfo")
        SysInfo.resize(400, 300)
        self.verticalLayout = QVBoxLayout(SysInfo)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(SysInfo)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)


        self.retranslateUi(SysInfo)

        QMetaObject.connectSlotsByName(SysInfo)
    # setupUi

    def retranslateUi(self, SysInfo):
        SysInfo.setWindowTitle(QCoreApplication.translate("SysInfo", u"Form", None))
        self.label.setText(QCoreApplication.translate("SysInfo", u"System info test", None))
    # retranslateUi

