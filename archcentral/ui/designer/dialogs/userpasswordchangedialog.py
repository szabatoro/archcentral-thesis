# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'userpasswordchangedialog.ui'
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
    QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_UserPasswordChangeDialog(object):
    def setupUi(self, UserPasswordChangeDialog):
        if not UserPasswordChangeDialog.objectName():
            UserPasswordChangeDialog.setObjectName(u"UserPasswordChangeDialog")
        UserPasswordChangeDialog.resize(400, 100)
        self.verticalLayout_2 = QVBoxLayout(UserPasswordChangeDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.password_label = QLabel(UserPasswordChangeDialog)
        self.password_label.setObjectName(u"password_label")

        self.horizontalLayout.addWidget(self.password_label)

        self.password_edit = QLineEdit(UserPasswordChangeDialog)
        self.password_edit.setObjectName(u"password_edit")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.horizontalLayout.addWidget(self.password_edit)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.button_box = QDialogButtonBox(UserPasswordChangeDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout_2.addWidget(self.button_box)


        self.retranslateUi(UserPasswordChangeDialog)
        self.button_box.accepted.connect(UserPasswordChangeDialog.accept)
        self.button_box.rejected.connect(UserPasswordChangeDialog.reject)

        QMetaObject.connectSlotsByName(UserPasswordChangeDialog)
    # setupUi

    def retranslateUi(self, UserPasswordChangeDialog):
        UserPasswordChangeDialog.setWindowTitle(QCoreApplication.translate("UserPasswordChangeDialog", u"Change user password", None))
        self.password_label.setText(QCoreApplication.translate("UserPasswordChangeDialog", u"New password:", None))
    # retranslateUi

