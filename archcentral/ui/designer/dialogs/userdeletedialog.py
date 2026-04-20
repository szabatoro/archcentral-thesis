# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'userdeletedialog.ui'
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
    QDialogButtonBox, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_UserDeleteDialog(object):
    def setupUi(self, UserDeleteDialog):
        if not UserDeleteDialog.objectName():
            UserDeleteDialog.setObjectName(u"UserDeleteDialog")
        UserDeleteDialog.resize(400, 100)
        UserDeleteDialog.setMaximumSize(QSize(16777215, 100))
        self.verticalLayout = QVBoxLayout(UserDeleteDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.user_delete_label = QLabel(UserDeleteDialog)
        self.user_delete_label.setObjectName(u"user_delete_label")

        self.verticalLayout.addWidget(self.user_delete_label)

        self.delete_homedir_checkbox = QCheckBox(UserDeleteDialog)
        self.delete_homedir_checkbox.setObjectName(u"delete_homedir_checkbox")

        self.verticalLayout.addWidget(self.delete_homedir_checkbox)

        self.button_box = QDialogButtonBox(UserDeleteDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.No|QDialogButtonBox.StandardButton.Yes)

        self.verticalLayout.addWidget(self.button_box)


        self.retranslateUi(UserDeleteDialog)
        self.button_box.accepted.connect(UserDeleteDialog.accept)
        self.button_box.rejected.connect(UserDeleteDialog.reject)

        QMetaObject.connectSlotsByName(UserDeleteDialog)
    # setupUi

    def retranslateUi(self, UserDeleteDialog):
        UserDeleteDialog.setWindowTitle(QCoreApplication.translate("UserDeleteDialog", u"Delete user", None))
        self.user_delete_label.setText(QCoreApplication.translate("UserDeleteDialog", u"Are you sure you want to delete user ...?", None))
        self.delete_homedir_checkbox.setText(QCoreApplication.translate("UserDeleteDialog", u"Also delete their home directory", None))
    # retranslateUi

