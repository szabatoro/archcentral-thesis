# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'packagemanager.ui'
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

class Ui_PackageManager(object):
    def setupUi(self, PackageManager):
        if not PackageManager.objectName():
            PackageManager.setObjectName(u"PackageManager")
        PackageManager.resize(400, 300)
        self.verticalLayout = QVBoxLayout(PackageManager)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(PackageManager)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)


        self.retranslateUi(PackageManager)

        QMetaObject.connectSlotsByName(PackageManager)
    # setupUi

    def retranslateUi(self, PackageManager):
        PackageManager.setWindowTitle(QCoreApplication.translate("PackageManager", u"Form", None))
        self.label.setText(QCoreApplication.translate("PackageManager", u"Package manager test", None))
    # retranslateUi

