# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'userchangefullnamedialog.ui'
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

class Ui_UserChangeFullNameDialog(object):
    def setupUi(self, UserChangeFullNameDialog):
        if not UserChangeFullNameDialog.objectName():
            UserChangeFullNameDialog.setObjectName(u"UserChangeFullNameDialog")
        UserChangeFullNameDialog.resize(400, 100)
        UserChangeFullNameDialog.setMaximumSize(QSize(16777215, 100))
        self.verticalLayout = QVBoxLayout(UserChangeFullNameDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.full_name_label = QLabel(UserChangeFullNameDialog)
        self.full_name_label.setObjectName(u"full_name_label")

        self.horizontalLayout.addWidget(self.full_name_label)

        self.full_name_edit = QLineEdit(UserChangeFullNameDialog)
        self.full_name_edit.setObjectName(u"full_name_edit")

        self.horizontalLayout.addWidget(self.full_name_edit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.button_box = QDialogButtonBox(UserChangeFullNameDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.button_box)


        self.retranslateUi(UserChangeFullNameDialog)
        self.button_box.accepted.connect(UserChangeFullNameDialog.accept)
        self.button_box.rejected.connect(UserChangeFullNameDialog.reject)

        QMetaObject.connectSlotsByName(UserChangeFullNameDialog)
    # setupUi

    def retranslateUi(self, UserChangeFullNameDialog):
        UserChangeFullNameDialog.setWindowTitle(QCoreApplication.translate("UserChangeFullNameDialog", u"Change user full name", None))
        self.full_name_label.setText(QCoreApplication.translate("UserChangeFullNameDialog", u"Full name", None))
    # retranslateUi

