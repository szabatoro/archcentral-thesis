# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'userchangeshelldialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QHBoxLayout, QLabel, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_UserChangeShellDialog(object):
    def setupUi(self, UserChangeShellDialog):
        if not UserChangeShellDialog.objectName():
            UserChangeShellDialog.setObjectName(u"UserChangeShellDialog")
        UserChangeShellDialog.resize(400, 100)
        UserChangeShellDialog.setMaximumSize(QSize(16777215, 100))
        self.verticalLayout_2 = QVBoxLayout(UserChangeShellDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.available_shells_label = QLabel(UserChangeShellDialog)
        self.available_shells_label.setObjectName(u"available_shells_label")

        self.horizontalLayout_2.addWidget(self.available_shells_label)

        self.available_shells_box = QComboBox(UserChangeShellDialog)
        self.available_shells_box.setObjectName(u"available_shells_box")

        self.horizontalLayout_2.addWidget(self.available_shells_box)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.button_box = QDialogButtonBox(UserChangeShellDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout_2.addWidget(self.button_box)


        self.retranslateUi(UserChangeShellDialog)
        self.button_box.accepted.connect(UserChangeShellDialog.accept)
        self.button_box.rejected.connect(UserChangeShellDialog.reject)

        QMetaObject.connectSlotsByName(UserChangeShellDialog)
    # setupUi

    def retranslateUi(self, UserChangeShellDialog):
        UserChangeShellDialog.setWindowTitle(QCoreApplication.translate("UserChangeShellDialog", u"Change user shell", None))
        self.available_shells_label.setText(QCoreApplication.translate("UserChangeShellDialog", u"Available shells", None))
    # retranslateUi

