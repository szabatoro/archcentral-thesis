# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'userchangehomedirdialog.ui'
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
    QToolButton, QVBoxLayout, QWidget)

class Ui_UserChangeHomeDirDialog(object):
    def setupUi(self, UserChangeHomeDirDialog):
        if not UserChangeHomeDirDialog.objectName():
            UserChangeHomeDirDialog.setObjectName(u"UserChangeHomeDirDialog")
        UserChangeHomeDirDialog.resize(400, 100)
        UserChangeHomeDirDialog.setMaximumSize(QSize(16777215, 100))
        self.verticalLayout = QVBoxLayout(UserChangeHomeDirDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.homedir_label = QLabel(UserChangeHomeDirDialog)
        self.homedir_label.setObjectName(u"homedir_label")

        self.horizontalLayout.addWidget(self.homedir_label)

        self.homedir_edit = QLineEdit(UserChangeHomeDirDialog)
        self.homedir_edit.setObjectName(u"homedir_edit")

        self.horizontalLayout.addWidget(self.homedir_edit)

        self.homedir_button = QToolButton(UserChangeHomeDirDialog)
        self.homedir_button.setObjectName(u"homedir_button")
        icon = QIcon(QIcon.fromTheme(u"folder"))
        self.homedir_button.setIcon(icon)

        self.horizontalLayout.addWidget(self.homedir_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.button_box = QDialogButtonBox(UserChangeHomeDirDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.button_box)


        self.retranslateUi(UserChangeHomeDirDialog)
        self.button_box.accepted.connect(UserChangeHomeDirDialog.accept)
        self.button_box.rejected.connect(UserChangeHomeDirDialog.reject)

        QMetaObject.connectSlotsByName(UserChangeHomeDirDialog)
    # setupUi

    def retranslateUi(self, UserChangeHomeDirDialog):
        UserChangeHomeDirDialog.setWindowTitle(QCoreApplication.translate("UserChangeHomeDirDialog", u"Change user home directory", None))
        self.homedir_label.setText(QCoreApplication.translate("UserChangeHomeDirDialog", u"Home directory", None))
        self.homedir_button.setText(QCoreApplication.translate("UserChangeHomeDirDialog", u"...", None))
    # retranslateUi

