# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'groupadddialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_GroupAddDialog(object):
    def setupUi(self, GroupAddDialog):
        if not GroupAddDialog.objectName():
            GroupAddDialog.setObjectName(u"GroupAddDialog")
        GroupAddDialog.resize(400, 302)
        self.verticalLayout = QVBoxLayout(GroupAddDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.group_name_label = QLabel(GroupAddDialog)
        self.group_name_label.setObjectName(u"group_name_label")

        self.horizontalLayout.addWidget(self.group_name_label)

        self.group_name_edit = QLineEdit(GroupAddDialog)
        self.group_name_edit.setObjectName(u"group_name_edit")

        self.horizontalLayout.addWidget(self.group_name_edit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.system_group_checkbox = QCheckBox(GroupAddDialog)
        self.system_group_checkbox.setObjectName(u"system_group_checkbox")

        self.verticalLayout.addWidget(self.system_group_checkbox)

        self.user_list = QListWidget(GroupAddDialog)
        self.user_list.setObjectName(u"user_list")

        self.verticalLayout.addWidget(self.user_list)

        self.status_label = QLabel(GroupAddDialog)
        self.status_label.setObjectName(u"status_label")

        self.verticalLayout.addWidget(self.status_label)

        self.button_box = QDialogButtonBox(GroupAddDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.button_box)


        self.retranslateUi(GroupAddDialog)
        self.button_box.accepted.connect(GroupAddDialog.accept)
        self.button_box.rejected.connect(GroupAddDialog.reject)

        QMetaObject.connectSlotsByName(GroupAddDialog)
    # setupUi

    def retranslateUi(self, GroupAddDialog):
        GroupAddDialog.setWindowTitle(QCoreApplication.translate("GroupAddDialog", u"Create new group", None))
        self.group_name_label.setText(QCoreApplication.translate("GroupAddDialog", u"Group name", None))
        self.system_group_checkbox.setText(QCoreApplication.translate("GroupAddDialog", u"System group", None))
        self.status_label.setText("")
    # retranslateUi

