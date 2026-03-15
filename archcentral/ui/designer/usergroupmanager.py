# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'usergroupmanager.ui'
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
    QLabel, QPushButton, QSizePolicy, QTabWidget,
    QTableView, QVBoxLayout, QWidget)

class Ui_UserGroupManager(object):
    def setupUi(self, UserGroupManager):
        if not UserGroupManager.objectName():
            UserGroupManager.setObjectName(u"UserGroupManager")
        UserGroupManager.resize(927, 623)
        self.verticalLayout = QVBoxLayout(UserGroupManager)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title = QLabel(UserGroupManager)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.title.setFont(font)

        self.verticalLayout.addWidget(self.title)

        self.users_groups_tab = QTabWidget(UserGroupManager)
        self.users_groups_tab.setObjectName(u"users_groups_tab")
        self.users_tab = QWidget()
        self.users_tab.setObjectName(u"users_tab")
        self.verticalLayout_2 = QVBoxLayout(self.users_tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.user_list_table = QTableView(self.users_tab)
        self.user_list_table.setObjectName(u"user_list_table")
        self.user_list_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.user_list_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.user_list_table.horizontalHeader().setStretchLastSection(True)
        self.user_list_table.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.user_list_table)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.add_user_button = QPushButton(self.users_tab)
        self.add_user_button.setObjectName(u"add_user_button")

        self.horizontalLayout.addWidget(self.add_user_button)

        self.modify_user_button = QPushButton(self.users_tab)
        self.modify_user_button.setObjectName(u"modify_user_button")

        self.horizontalLayout.addWidget(self.modify_user_button)

        self.delete_user_button = QPushButton(self.users_tab)
        self.delete_user_button.setObjectName(u"delete_user_button")

        self.horizontalLayout.addWidget(self.delete_user_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.users_groups_tab.addTab(self.users_tab, "")
        self.groups_tab = QWidget()
        self.groups_tab.setObjectName(u"groups_tab")
        self.verticalLayout_3 = QVBoxLayout(self.groups_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.groups_tab)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.group_list_table = QTableView(self.groups_tab)
        self.group_list_table.setObjectName(u"group_list_table")
        self.group_list_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.group_list_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.group_list_table.horizontalHeader().setStretchLastSection(True)
        self.group_list_table.verticalHeader().setVisible(False)

        self.verticalLayout_3.addWidget(self.group_list_table)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.manage_users_button = QPushButton(self.groups_tab)
        self.manage_users_button.setObjectName(u"manage_users_button")

        self.horizontalLayout_2.addWidget(self.manage_users_button)

        self.create_group_button = QPushButton(self.groups_tab)
        self.create_group_button.setObjectName(u"create_group_button")

        self.horizontalLayout_2.addWidget(self.create_group_button)

        self.delete_group_button = QPushButton(self.groups_tab)
        self.delete_group_button.setObjectName(u"delete_group_button")

        self.horizontalLayout_2.addWidget(self.delete_group_button)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.users_groups_tab.addTab(self.groups_tab, "")

        self.verticalLayout.addWidget(self.users_groups_tab)


        self.retranslateUi(UserGroupManager)

        self.users_groups_tab.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(UserGroupManager)
    # setupUi

    def retranslateUi(self, UserGroupManager):
        UserGroupManager.setWindowTitle(QCoreApplication.translate("UserGroupManager", u"Form", None))
        self.title.setText(QCoreApplication.translate("UserGroupManager", u"User and groups manager", None))
        self.add_user_button.setText(QCoreApplication.translate("UserGroupManager", u"Add user", None))
        self.modify_user_button.setText(QCoreApplication.translate("UserGroupManager", u"Modify user", None))
        self.delete_user_button.setText(QCoreApplication.translate("UserGroupManager", u"Delete user", None))
        self.users_groups_tab.setTabText(self.users_groups_tab.indexOf(self.users_tab), QCoreApplication.translate("UserGroupManager", u"Users", None))
        self.label.setText(QCoreApplication.translate("UserGroupManager", u"Warning: You shouldn't delete groups you didn't make yourself.", None))
        self.manage_users_button.setText(QCoreApplication.translate("UserGroupManager", u"Manage users", None))
        self.create_group_button.setText(QCoreApplication.translate("UserGroupManager", u"Create group", None))
        self.delete_group_button.setText(QCoreApplication.translate("UserGroupManager", u"Delete group", None))
        self.users_groups_tab.setTabText(self.users_groups_tab.indexOf(self.groups_tab), QCoreApplication.translate("UserGroupManager", u"Groups", None))
    # retranslateUi

