# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'groupdeletedialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QSizePolicy, QVBoxLayout, QWidget)

class Ui_GroupDeleteDialog(object):
    def setupUi(self, GroupDeleteDialog):
        if not GroupDeleteDialog.objectName():
            GroupDeleteDialog.setObjectName(u"GroupDeleteDialog")
        GroupDeleteDialog.resize(400, 100)
        GroupDeleteDialog.setMaximumSize(QSize(16777215, 100))
        self.verticalLayout = QVBoxLayout(GroupDeleteDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.group_delete_label = QLabel(GroupDeleteDialog)
        self.group_delete_label.setObjectName(u"group_delete_label")

        self.verticalLayout.addWidget(self.group_delete_label)

        self.button_box = QDialogButtonBox(GroupDeleteDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.button_box)


        self.retranslateUi(GroupDeleteDialog)
        self.button_box.accepted.connect(GroupDeleteDialog.accept)
        self.button_box.rejected.connect(GroupDeleteDialog.reject)

        QMetaObject.connectSlotsByName(GroupDeleteDialog)
    # setupUi

    def retranslateUi(self, GroupDeleteDialog):
        GroupDeleteDialog.setWindowTitle(QCoreApplication.translate("GroupDeleteDialog", u"Deleting group", None))
        self.group_delete_label.setText(QCoreApplication.translate("GroupDeleteDialog", u"Are you sure you want to delete group ...?", None))
    # retranslateUi

