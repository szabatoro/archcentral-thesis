# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'servicemanager.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QTabWidget, QTableView, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_ServiceManager(object):
    def setupUi(self, ServiceManager):
        if not ServiceManager.objectName():
            ServiceManager.setObjectName(u"ServiceManager")
        ServiceManager.resize(862, 552)
        self.verticalLayout = QVBoxLayout(ServiceManager)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title = QLabel(ServiceManager)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.title.setFont(font)

        self.verticalLayout.addWidget(self.title)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.service_search = QLineEdit(ServiceManager)
        self.service_search.setObjectName(u"service_search")

        self.horizontalLayout.addWidget(self.service_search)

        self.service_search_button = QPushButton(ServiceManager)
        self.service_search_button.setObjectName(u"service_search_button")

        self.horizontalLayout.addWidget(self.service_search_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout2 = QHBoxLayout()
        self.horizontalLayout2.setObjectName(u"horizontalLayout2")
        self.user_system_tab = QTabWidget(ServiceManager)
        self.user_system_tab.setObjectName(u"user_system_tab")
        self.user_system_tab.setTabPosition(QTabWidget.TabPosition.North)
        self.user_system_tab.setDocumentMode(False)
        self.system_services_tab = QWidget()
        self.system_services_tab.setObjectName(u"system_services_tab")
        self.verticalLayout_3 = QVBoxLayout(self.system_services_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.system_service_list_table = QTableView(self.system_services_tab)
        self.system_service_list_table.setObjectName(u"system_service_list_table")
        font1 = QFont()
        font1.setBold(True)
        self.system_service_list_table.setFont(font1)
        self.system_service_list_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.system_service_list_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.system_service_list_table.horizontalHeader().setStretchLastSection(True)
        self.system_service_list_table.verticalHeader().setVisible(False)
        self.system_service_list_table.verticalHeader().setStretchLastSection(True)

        self.verticalLayout_3.addWidget(self.system_service_list_table)

        self.user_system_tab.addTab(self.system_services_tab, "")
        self.user_services_tab = QWidget()
        self.user_services_tab.setObjectName(u"user_services_tab")
        self.verticalLayout_4 = QVBoxLayout(self.user_services_tab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.user_service_list_table = QTableView(self.user_services_tab)
        self.user_service_list_table.setObjectName(u"user_service_list_table")
        self.user_service_list_table.setFont(font1)
        self.user_service_list_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.user_service_list_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.user_service_list_table.horizontalHeader().setStretchLastSection(True)
        self.user_service_list_table.verticalHeader().setVisible(False)
        self.user_service_list_table.verticalHeader().setStretchLastSection(True)

        self.verticalLayout_4.addWidget(self.user_service_list_table)

        self.user_system_tab.addTab(self.user_services_tab, "")

        self.horizontalLayout2.addWidget(self.user_system_tab)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.start_stop_button = QPushButton(ServiceManager)
        self.start_stop_button.setObjectName(u"start_stop_button")

        self.verticalLayout_2.addWidget(self.start_stop_button)

        self.enable_disable_button = QPushButton(ServiceManager)
        self.enable_disable_button.setObjectName(u"enable_disable_button")

        self.verticalLayout_2.addWidget(self.enable_disable_button)


        self.horizontalLayout2.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.service_details_tree = QTreeWidget(ServiceManager)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"Name");
        self.service_details_tree.setHeaderItem(__qtreewidgetitem)
        self.service_details_tree.setObjectName(u"service_details_tree")
        self.service_details_tree.setColumnCount(2)
        self.service_details_tree.header().setVisible(True)

        self.verticalLayout.addWidget(self.service_details_tree)

        self.statusbar = QLabel(ServiceManager)
        self.statusbar.setObjectName(u"statusbar")

        self.verticalLayout.addWidget(self.statusbar)


        self.retranslateUi(ServiceManager)

        self.user_system_tab.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ServiceManager)
    # setupUi

    def retranslateUi(self, ServiceManager):
        ServiceManager.setWindowTitle(QCoreApplication.translate("ServiceManager", u"Form", None))
        self.title.setText(QCoreApplication.translate("ServiceManager", u"Systemd Service Management", None))
        self.service_search.setText("")
        self.service_search.setPlaceholderText(QCoreApplication.translate("ServiceManager", u"Search systemd units", None))
        self.service_search_button.setText(QCoreApplication.translate("ServiceManager", u"Search", None))
        self.user_system_tab.setTabText(self.user_system_tab.indexOf(self.system_services_tab), QCoreApplication.translate("ServiceManager", u"System services", None))
        self.user_system_tab.setTabText(self.user_system_tab.indexOf(self.user_services_tab), QCoreApplication.translate("ServiceManager", u"User services", None))
        self.start_stop_button.setText(QCoreApplication.translate("ServiceManager", u"Start", None))
        self.enable_disable_button.setText(QCoreApplication.translate("ServiceManager", u"Enable", None))
        ___qtreewidgetitem = self.service_details_tree.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("ServiceManager", u"Value", None));
        self.statusbar.setText("")
    # retranslateUi

