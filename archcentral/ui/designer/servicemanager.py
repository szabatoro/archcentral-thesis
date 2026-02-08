# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'servicemanager.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_ServiceManager(object):
    def setupUi(self, ServiceManager):
        if not ServiceManager.objectName():
            ServiceManager.setObjectName(u"ServiceManager")
        ServiceManager.resize(862, 552)
        self.verticalLayout = QVBoxLayout(ServiceManager)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(ServiceManager)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.tabWidget = QTabWidget(ServiceManager)
        self.tabWidget.setObjectName(u"tabWidget")
        self.sys_level = QWidget()
        self.sys_level.setObjectName(u"sys_level")
        self.tabWidget.addTab(self.sys_level, "")
        self.user_level = QWidget()
        self.user_level.setObjectName(u"user_level")
        self.tabWidget.addTab(self.user_level, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(ServiceManager)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ServiceManager)
    # setupUi

    def retranslateUi(self, ServiceManager):
        ServiceManager.setWindowTitle(QCoreApplication.translate("ServiceManager", u"Form", None))
        self.label.setText(QCoreApplication.translate("ServiceManager", u"Systemd Service Management", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.sys_level), QCoreApplication.translate("ServiceManager", u"System level", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.user_level), QCoreApplication.translate("ServiceManager", u"User level", None))
    # retranslateUi

