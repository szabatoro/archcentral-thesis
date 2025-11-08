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

class Ui_sys_info(object):
    def setupUi(self, sys_info):
        if not sys_info.objectName():
            sys_info.setObjectName(u"sys_info")
        sys_info.resize(400, 300)
        self.verticalLayout = QVBoxLayout(sys_info)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(sys_info)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)


        self.retranslateUi(sys_info)

        QMetaObject.connectSlotsByName(sys_info)
    # setupUi

    def retranslateUi(self, sys_info):
        sys_info.setWindowTitle(QCoreApplication.translate("sys_info", u"Form", None))
        self.label.setText(QCoreApplication.translate("sys_info", u"System info test", None))
    # retranslateUi

