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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QSizePolicy,
    QTabWidget, QTableView, QVBoxLayout, QWidget)

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

        self.content = QTabWidget(UserGroupManager)
        self.content.setObjectName(u"content")
        self.users = QWidget()
        self.users.setObjectName(u"users")
        self.verticalLayout_2 = QVBoxLayout(self.users)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.user_list_table = QTableView(self.users)
        self.user_list_table.setObjectName(u"user_list_table")

        self.verticalLayout_2.addWidget(self.user_list_table)

        self.content.addTab(self.users, "")
        self.groups = QWidget()
        self.groups.setObjectName(u"groups")
        self.content.addTab(self.groups, "")

        self.verticalLayout.addWidget(self.content)


        self.retranslateUi(UserGroupManager)

        self.content.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(UserGroupManager)
    # setupUi

    def retranslateUi(self, UserGroupManager):
        UserGroupManager.setWindowTitle(QCoreApplication.translate("UserGroupManager", u"Form", None))
        self.title.setText(QCoreApplication.translate("UserGroupManager", u"User and groups manager", None))
        self.content.setTabText(self.content.indexOf(self.users), QCoreApplication.translate("UserGroupManager", u"Users", None))
        self.content.setTabText(self.content.indexOf(self.groups), QCoreApplication.translate("UserGroupManager", u"Groups", None))
    # retranslateUi

