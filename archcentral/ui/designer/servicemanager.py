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
    QTabWidget, QTableView, QTableWidget, QTableWidgetItem,
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

        self.content = QTabWidget(ServiceManager)
        self.content.setObjectName(u"content")
        self.sys_level = QWidget()
        self.sys_level.setObjectName(u"sys_level")
        self.verticalLayout_4 = QVBoxLayout(self.sys_level)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.service_search = QLineEdit(self.sys_level)
        self.service_search.setObjectName(u"service_search")

        self.horizontalLayout.addWidget(self.service_search)

        self.service_search_button = QPushButton(self.sys_level)
        self.service_search_button.setObjectName(u"service_search_button")

        self.horizontalLayout.addWidget(self.service_search_button)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.service_list_table = QTableView(self.sys_level)
        self.service_list_table.setObjectName(u"service_list_table")
        self.service_list_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.service_list_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.horizontalLayout_3.addWidget(self.service_list_table)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pushButton_2 = QPushButton(self.sys_level)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout_2.addWidget(self.pushButton_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.service_details_table = QTableWidget(self.sys_level)
        self.service_details_table.setObjectName(u"service_details_table")

        self.verticalLayout_4.addWidget(self.service_details_table)

        self.content.addTab(self.sys_level, "")
        self.user_level = QWidget()
        self.user_level.setObjectName(u"user_level")
        self.content.addTab(self.user_level, "")

        self.verticalLayout.addWidget(self.content)


        self.retranslateUi(ServiceManager)

        self.content.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ServiceManager)
    # setupUi

    def retranslateUi(self, ServiceManager):
        ServiceManager.setWindowTitle(QCoreApplication.translate("ServiceManager", u"Form", None))
        self.title.setText(QCoreApplication.translate("ServiceManager", u"Systemd Service Management", None))
        self.service_search_button.setText(QCoreApplication.translate("ServiceManager", u"PushButton", None))
        self.pushButton_2.setText(QCoreApplication.translate("ServiceManager", u"PushButton", None))
        self.content.setTabText(self.content.indexOf(self.sys_level), QCoreApplication.translate("ServiceManager", u"System level", None))
        self.content.setTabText(self.content.indexOf(self.user_level), QCoreApplication.translate("ServiceManager", u"User level", None))
    # retranslateUi

