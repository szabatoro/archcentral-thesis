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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QTableView, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

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
        self.service_list_table = QTableView(ServiceManager)
        self.service_list_table.setObjectName(u"service_list_table")
        font1 = QFont()
        font1.setBold(True)
        self.service_list_table.setFont(font1)
        self.service_list_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.service_list_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.service_list_table.verticalHeader().setVisible(False)

        self.horizontalLayout2.addWidget(self.service_list_table)

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

        QMetaObject.connectSlotsByName(ServiceManager)
    # setupUi

    def retranslateUi(self, ServiceManager):
        ServiceManager.setWindowTitle(QCoreApplication.translate("ServiceManager", u"Form", None))
        self.title.setText(QCoreApplication.translate("ServiceManager", u"Systemd Service Management", None))
        self.service_search.setText("")
        self.service_search.setPlaceholderText(QCoreApplication.translate("ServiceManager", u"Search systemd units", None))
        self.service_search_button.setText(QCoreApplication.translate("ServiceManager", u"Search", None))
        self.start_stop_button.setText(QCoreApplication.translate("ServiceManager", u"Start", None))
        self.enable_disable_button.setText(QCoreApplication.translate("ServiceManager", u"Enable", None))
        ___qtreewidgetitem = self.service_details_tree.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("ServiceManager", u"Value", None));
        self.statusbar.setText("")
    # retranslateUi

