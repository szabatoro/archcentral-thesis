# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sysinfo.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QVBoxLayout,
    QWidget)

from archcentral.ui.custom_widgets.graph import (CPUGraph, NetworkGraph, RAMGraph)
from archcentral.ui.custom_widgets.legendwidget import LegendWidget

class Ui_SysInfo(object):
    def setupUi(self, SysInfo):
        if not SysInfo.objectName():
            SysInfo.setObjectName(u"SysInfo")
        SysInfo.resize(1200, 595)
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
        self.info.setMinimumSize(QSize(300, 0))
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

        self.cpu_legend = LegendWidget(self.cpu_info)
        self.cpu_legend.setObjectName(u"cpu_legend")

        self.verticalLayout_4.addWidget(self.cpu_legend)

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

        self.ram_legend = LegendWidget(self.ram_info)
        self.ram_legend.setObjectName(u"ram_legend")

        self.verticalLayout_5.addWidget(self.ram_legend)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_4)


        self.verticalLayout_3.addWidget(self.ram_info)

        self.network_info = QWidget(self.info)
        self.network_info.setObjectName(u"network_info")
        self.verticalLayout_6 = QVBoxLayout(self.network_info)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_5)

        self.network_title = QLabel(self.network_info)
        self.network_title.setObjectName(u"network_title")
        self.network_title.setFont(font1)

        self.verticalLayout_6.addWidget(self.network_title)

        self.network_active_interface = QLabel(self.network_info)
        self.network_active_interface.setObjectName(u"network_active_interface")

        self.verticalLayout_6.addWidget(self.network_active_interface)

        self.network_local_ip = QLabel(self.network_info)
        self.network_local_ip.setObjectName(u"network_local_ip")

        self.verticalLayout_6.addWidget(self.network_local_ip)

        self.network_public_ip_layout = QHBoxLayout()
        self.network_public_ip_layout.setObjectName(u"network_public_ip_layout")
        self.network_public_ip = QLabel(self.network_info)
        self.network_public_ip.setObjectName(u"network_public_ip")

        self.network_public_ip_layout.addWidget(self.network_public_ip)

        self.network_public_ip_switch = QPushButton(self.network_info)
        self.network_public_ip_switch.setObjectName(u"network_public_ip_switch")

        self.network_public_ip_layout.addWidget(self.network_public_ip_switch)


        self.verticalLayout_6.addLayout(self.network_public_ip_layout)

        self.network_legend = LegendWidget(self.network_info)
        self.network_legend.setObjectName(u"network_legend")

        self.verticalLayout_6.addWidget(self.network_legend)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_6)


        self.verticalLayout_3.addWidget(self.network_info)


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

        self.network_graph = NetworkGraph(self.monitors)
        self.network_graph.setObjectName(u"network_graph")

        self.verticalLayout_2.addWidget(self.network_graph)


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

        self.uptime = QLabel(self.system)
        self.uptime.setObjectName(u"uptime")

        self.verticalLayout_8.addWidget(self.uptime)

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

        self.content.setCurrentIndex(0)


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
        self.network_title.setText(QCoreApplication.translate("SysInfo", u"Network", None))
        self.network_active_interface.setText(QCoreApplication.translate("SysInfo", u"Active interface: ", None))
        self.network_local_ip.setText(QCoreApplication.translate("SysInfo", u"Local IP: ", None))
        self.network_public_ip.setText(QCoreApplication.translate("SysInfo", u"Public IP:", None))
#if QT_CONFIG(tooltip)
        self.network_public_ip_switch.setToolTip(QCoreApplication.translate("SysInfo", u"This will connect to api.ipify.org to determine public IP.", None))
#endif // QT_CONFIG(tooltip)
        self.network_public_ip_switch.setText(QCoreApplication.translate("SysInfo", u"Get IP", None))
        self.content.setTabText(self.content.indexOf(self.hardware), QCoreApplication.translate("SysInfo", u"Hardware", None))
        self.system_title.setText(QCoreApplication.translate("SysInfo", u"System", None))
        self.hostname.setText(QCoreApplication.translate("SysInfo", u"Hostname:", None))
        self.kernel_name.setText(QCoreApplication.translate("SysInfo", u"Kernel:", None))
        self.uptime.setText(QCoreApplication.translate("SysInfo", u"Uptime: ", None))
        self.gui_title.setText(QCoreApplication.translate("SysInfo", u"GUI", None))
        self.de.setText(QCoreApplication.translate("SysInfo", u"Desktop environment:", None))
        self.wm.setText(QCoreApplication.translate("SysInfo", u"Window manager:", None))
        self.content.setTabText(self.content.indexOf(self.software), QCoreApplication.translate("SysInfo", u"Software", None))
        self.content.setTabText(self.content.indexOf(self.processes), QCoreApplication.translate("SysInfo", u"Processes", None))
    # retranslateUi

