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
    QSpacerItem, QTabWidget, QVBoxLayout, QWidget)

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
        self.cpu_info = QWidget(self.info)
        self.cpu_info.setObjectName(u"cpu_info")
        self.verticalLayout_4 = QVBoxLayout(self.cpu_info)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.cpu_title = QLabel(self.cpu_info)
        self.cpu_title.setObjectName(u"cpu_title")
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.cpu_title.setFont(font1)

        self.verticalLayout_4.addWidget(self.cpu_title)

        self.cpu_name = QLabel(self.cpu_info)
        self.cpu_name.setObjectName(u"cpu_name")

        self.verticalLayout_4.addWidget(self.cpu_name)

        self.cpu_core_count = QLabel(self.cpu_info)
        self.cpu_core_count.setObjectName(u"cpu_core_count")

        self.verticalLayout_4.addWidget(self.cpu_core_count)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)


        self.verticalLayout_3.addWidget(self.cpu_info)

        self.ram_info = QWidget(self.info)
        self.ram_info.setObjectName(u"ram_info")
        self.verticalLayout_5 = QVBoxLayout(self.ram_info)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_3)

        self.ram_title = QLabel(self.ram_info)
        self.ram_title.setObjectName(u"ram_title")
        self.ram_title.setFont(font1)

        self.verticalLayout_5.addWidget(self.ram_title)

        self.ram_amount = QLabel(self.ram_info)
        self.ram_amount.setObjectName(u"ram_amount")

        self.verticalLayout_5.addWidget(self.ram_amount)

        self.swap_amount = QLabel(self.ram_info)
        self.swap_amount.setObjectName(u"swap_amount")

        self.verticalLayout_5.addWidget(self.swap_amount)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_4)


        self.verticalLayout_3.addWidget(self.ram_info)

        self.gpu_info = QWidget(self.info)
        self.gpu_info.setObjectName(u"gpu_info")
        self.verticalLayout_6 = QVBoxLayout(self.gpu_info)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_5)

        self.gpu_title = QLabel(self.gpu_info)
        self.gpu_title.setObjectName(u"gpu_title")
        self.gpu_title.setFont(font1)

        self.verticalLayout_6.addWidget(self.gpu_title)

        self.gpu_name = QLabel(self.gpu_info)
        self.gpu_name.setObjectName(u"gpu_name")

        self.verticalLayout_6.addWidget(self.gpu_name)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_6)


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
        self.software = QWidget()
        self.software.setObjectName(u"software")
        self.verticalLayout_7 = QVBoxLayout(self.software)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.system = QWidget(self.software)
        self.system.setObjectName(u"system")
        self.verticalLayout_8 = QVBoxLayout(self.system)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_7)

        self.system_title = QLabel(self.system)
        self.system_title.setObjectName(u"system_title")
        self.system_title.setFont(font1)

        self.verticalLayout_8.addWidget(self.system_title)

        self.hostname = QLabel(self.system)
        self.hostname.setObjectName(u"hostname")

        self.verticalLayout_8.addWidget(self.hostname)

        self.kernel_name = QLabel(self.system)
        self.kernel_name.setObjectName(u"kernel_name")

        self.verticalLayout_8.addWidget(self.kernel_name)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_8)


        self.verticalLayout_7.addWidget(self.system)

        self.gui = QWidget(self.software)
        self.gui.setObjectName(u"gui")
        self.gui.setMinimumSize(QSize(0, 0))
        self.verticalLayout_9 = QVBoxLayout(self.gui)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_9)

        self.gui_title = QLabel(self.gui)
        self.gui_title.setObjectName(u"gui_title")
        self.gui_title.setFont(font1)

        self.verticalLayout_9.addWidget(self.gui_title)

        self.de = QLabel(self.gui)
        self.de.setObjectName(u"de")

        self.verticalLayout_9.addWidget(self.de)

        self.wm = QLabel(self.gui)
        self.wm.setObjectName(u"wm")

        self.verticalLayout_9.addWidget(self.wm)

        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_10)


        self.verticalLayout_7.addWidget(self.gui)

        self.widget_3 = QWidget(self.software)
        self.widget_3.setObjectName(u"widget_3")

        self.verticalLayout_7.addWidget(self.widget_3)

        self.content.addTab(self.software, "")
        self.processes = QWidget()
        self.processes.setObjectName(u"processes")
        self.content.addTab(self.processes, "")

        self.verticalLayout.addWidget(self.content)


        self.retranslateUi(SysInfo)

        self.content.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(SysInfo)
    # setupUi

    def retranslateUi(self, SysInfo):
        SysInfo.setWindowTitle(QCoreApplication.translate("SysInfo", u"Form", None))
        self.title.setText(QCoreApplication.translate("SysInfo", u"System information", None))
        self.cpu_title.setText(QCoreApplication.translate("SysInfo", u"CPU", None))
        self.cpu_name.setText(QCoreApplication.translate("SysInfo", u"Name: ", None))
        self.cpu_core_count.setText(QCoreApplication.translate("SysInfo", u"Core count:", None))
        self.ram_title.setText(QCoreApplication.translate("SysInfo", u"RAM", None))
        self.ram_amount.setText(QCoreApplication.translate("SysInfo", u"Used:", None))
        self.swap_amount.setText(QCoreApplication.translate("SysInfo", u"Swap disabled.", None))
        self.gpu_title.setText(QCoreApplication.translate("SysInfo", u"GPU", None))
        self.gpu_name.setText(QCoreApplication.translate("SysInfo", u"GPU:", None))
        self.content.setTabText(self.content.indexOf(self.hardware), QCoreApplication.translate("SysInfo", u"Hardware", None))
        self.system_title.setText(QCoreApplication.translate("SysInfo", u"System", None))
        self.hostname.setText(QCoreApplication.translate("SysInfo", u"Hostname:", None))
        self.kernel_name.setText(QCoreApplication.translate("SysInfo", u"Kernel:", None))
        self.gui_title.setText(QCoreApplication.translate("SysInfo", u"GUI", None))
        self.de.setText(QCoreApplication.translate("SysInfo", u"Desktop environment:", None))
        self.wm.setText(QCoreApplication.translate("SysInfo", u"Window manager:", None))
        self.content.setTabText(self.content.indexOf(self.software), QCoreApplication.translate("SysInfo", u"Software", None))
        self.content.setTabText(self.content.indexOf(self.processes), QCoreApplication.translate("SysInfo", u"Processes", None))
    # retranslateUi

