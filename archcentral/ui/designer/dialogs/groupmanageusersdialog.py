# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'groupmanageusersdialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QHeaderView, QSizePolicy, QTableView,
    QVBoxLayout, QWidget)

class Ui_GroupManageUsersDialog(object):
    def setupUi(self, GroupManageUsersDialog):
        if not GroupManageUsersDialog.objectName():
            GroupManageUsersDialog.setObjectName(u"GroupManageUsersDialog")
        GroupManageUsersDialog.resize(623, 419)
        self.verticalLayout = QVBoxLayout(GroupManageUsersDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.user_list_table = QTableView(GroupManageUsersDialog)
        self.user_list_table.setObjectName(u"user_list_table")
        self.user_list_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.user_list_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.user_list_table.horizontalHeader().setStretchLastSection(True)
        self.user_list_table.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.user_list_table)

        self.button_box = QDialogButtonBox(GroupManageUsersDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.button_box)


        self.retranslateUi(GroupManageUsersDialog)
        self.button_box.accepted.connect(GroupManageUsersDialog.accept)
        self.button_box.rejected.connect(GroupManageUsersDialog.reject)

        QMetaObject.connectSlotsByName(GroupManageUsersDialog)
    # setupUi

    def retranslateUi(self, GroupManageUsersDialog):
        GroupManageUsersDialog.setWindowTitle(QCoreApplication.translate("GroupManageUsersDialog", u"Manage group users", None))
    # retranslateUi

