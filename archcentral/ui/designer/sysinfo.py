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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QTabWidget, QVBoxLayout, QWidget)

from archcentral.ui.graph import (CPUGraph, GPUGraph, RAMGraph)

class Ui_SysInfo(object):
    def setupUi(self, SysInfo):
        if not SysInfo.objectName():
            SysInfo.setObjectName(u"SysInfo")
        SysInfo.resize(856, 595)
        self.verticalLayout = QVBoxLayout(SysInfo)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title = QLabel(SysInfo)
        self.title.setObjectName(u"title")
        self.title.setMinimumSize(QSize(0, 0))
        self.title.setMaximumSize(QSize(16777215, 50))
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.title.setFont(font)

        self.verticalLayout.addWidget(self.title)

        self.content = QTabWidget(SysInfo)
        self.content.setObjectName(u"content")
        self.hardware = QWidget()
        self.hardware.setObjectName(u"hardware")
        self.horizontalLayout = QHBoxLayout(self.hardware)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.info = QWidget(self.hardware)
        self.info.setObjectName(u"info")
        self.verticalLayout_3 = QVBoxLayout(self.info)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.cpu_info = QLabel(self.info)
        self.cpu_info.setObjectName(u"cpu_info")

        self.verticalLayout_3.addWidget(self.cpu_info)

        self.ram_info = QLabel(self.info)
        self.ram_info.setObjectName(u"ram_info")

        self.verticalLayout_3.addWidget(self.ram_info)

        self.gpu_info = QLabel(self.info)
        self.gpu_info.setObjectName(u"gpu_info")

        self.verticalLayout_3.addWidget(self.gpu_info)


        self.horizontalLayout.addWidget(self.info)

        self.monitors = QWidget(self.hardware)
        self.monitors.setObjectName(u"monitors")
        self.verticalLayout_2 = QVBoxLayout(self.monitors)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.cpu_graph = CPUGraph(self.monitors)
        self.cpu_graph.setObjectName(u"cpu_graph")

        self.verticalLayout_2.addWidget(self.cpu_graph)

        self.ram_graph = RAMGraph(self.monitors)
        self.ram_graph.setObjectName(u"ram_graph")

        self.verticalLayout_2.addWidget(self.ram_graph)

        self.gpu_graph = GPUGraph(self.monitors)
        self.gpu_graph.setObjectName(u"gpu_graph")

        self.verticalLayout_2.addWidget(self.gpu_graph)


        self.horizontalLayout.addWidget(self.monitors)

        self.content.addTab(self.hardware, "")
        self.processes = QWidget()
        self.processes.setObjectName(u"processes")
        self.content.addTab(self.processes, "")

        self.verticalLayout.addWidget(self.content)


        self.retranslateUi(SysInfo)

        self.content.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SysInfo)
    # setupUi

    def retranslateUi(self, SysInfo):
        SysInfo.setWindowTitle(QCoreApplication.translate("SysInfo", u"Form", None))
        self.title.setText(QCoreApplication.translate("SysInfo", u"System information", None))
        self.cpu_info.setText(QCoreApplication.translate("SysInfo", u"CPU:", None))
        self.ram_info.setText(QCoreApplication.translate("SysInfo", u"RAM:", None))
        self.gpu_info.setText(QCoreApplication.translate("SysInfo", u"GPU:", None))
        self.content.setTabText(self.content.indexOf(self.hardware), QCoreApplication.translate("SysInfo", u"Hardware", None))
        self.content.setTabText(self.content.indexOf(self.processes), QCoreApplication.translate("SysInfo", u"Processes", None))
    # retranslateUi

