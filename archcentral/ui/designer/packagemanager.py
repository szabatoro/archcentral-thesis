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

class Ui_package_manager(object):
    def setupUi(self, package_manager):
        if not package_manager.objectName():
            package_manager.setObjectName(u"package_manager")
        package_manager.resize(400, 300)
        self.verticalLayout = QVBoxLayout(package_manager)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(package_manager)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)


        self.retranslateUi(package_manager)

        QMetaObject.connectSlotsByName(package_manager)
    # setupUi

    def retranslateUi(self, package_manager):
        package_manager.setWindowTitle(QCoreApplication.translate("package_manager", u"Form", None))
        self.label.setText(QCoreApplication.translate("package_manager", u"Package manager test", None))
    # retranslateUi

