# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'useradddialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QButtonGroup, QComboBox,
    QDialog, QDialogButtonBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QRadioButton, QSizePolicy,
    QToolButton, QVBoxLayout, QWidget)

class Ui_UserAddDialog(object):
    def setupUi(self, UserAddDialog):
        if not UserAddDialog.objectName():
            UserAddDialog.setObjectName(u"UserAddDialog")
        UserAddDialog.resize(608, 401)
        self.verticalLayout = QVBoxLayout(UserAddDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.grid_layout = QGridLayout()
        self.grid_layout.setObjectName(u"grid_layout")
        self.home_choice_layout = QHBoxLayout()
        self.home_choice_layout.setObjectName(u"home_choice_layout")
        self.auto_home_button = QRadioButton(UserAddDialog)
        self.home_button_group = QButtonGroup(UserAddDialog)
        self.home_button_group.setObjectName(u"home_button_group")
        self.home_button_group.addButton(self.auto_home_button)
        self.auto_home_button.setObjectName(u"auto_home_button")
        self.auto_home_button.setChecked(True)

        self.home_choice_layout.addWidget(self.auto_home_button)

        self.existing_home_button = QRadioButton(UserAddDialog)
        self.home_button_group.addButton(self.existing_home_button)
        self.existing_home_button.setObjectName(u"existing_home_button")

        self.home_choice_layout.addWidget(self.existing_home_button)

        self.no_home_button = QRadioButton(UserAddDialog)
        self.home_button_group.addButton(self.no_home_button)
        self.no_home_button.setObjectName(u"no_home_button")

        self.home_choice_layout.addWidget(self.no_home_button)


        self.grid_layout.addLayout(self.home_choice_layout, 4, 0, 1, 1)

        self.home_select_layout = QHBoxLayout()
        self.home_select_layout.setObjectName(u"home_select_layout")
        self.home_label = QLabel(UserAddDialog)
        self.home_label.setObjectName(u"home_label")

        self.home_select_layout.addWidget(self.home_label)

        self.home_dir_edit = QLineEdit(UserAddDialog)
        self.home_dir_edit.setObjectName(u"home_dir_edit")
        self.home_dir_edit.setEnabled(False)

        self.home_select_layout.addWidget(self.home_dir_edit)

        self.file_browser_button = QToolButton(UserAddDialog)
        self.file_browser_button.setObjectName(u"file_browser_button")
        self.file_browser_button.setEnabled(False)

        self.home_select_layout.addWidget(self.file_browser_button)


        self.grid_layout.addLayout(self.home_select_layout, 5, 0, 1, 1)

        self.shell_layout = QHBoxLayout()
        self.shell_layout.setObjectName(u"shell_layout")
        self.shell_label = QLabel(UserAddDialog)
        self.shell_label.setObjectName(u"shell_label")

        self.shell_layout.addWidget(self.shell_label)

        self.shells_box = QComboBox(UserAddDialog)
        self.shells_box.setObjectName(u"shells_box")

        self.shell_layout.addWidget(self.shells_box)


        self.grid_layout.addLayout(self.shell_layout, 6, 0, 1, 1)

        self.password_layout = QHBoxLayout()
        self.password_layout.setObjectName(u"password_layout")
        self.password_label = QLabel(UserAddDialog)
        self.password_label.setObjectName(u"password_label")

        self.password_layout.addWidget(self.password_label)

        self.password_edit = QLineEdit(UserAddDialog)
        self.password_edit.setObjectName(u"password_edit")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.password_layout.addWidget(self.password_edit)


        self.grid_layout.addLayout(self.password_layout, 3, 0, 1, 1)

        self.name_layout = QHBoxLayout()
        self.name_layout.setObjectName(u"name_layout")
        self.user_name_label = QLabel(UserAddDialog)
        self.user_name_label.setObjectName(u"user_name_label")

        self.name_layout.addWidget(self.user_name_label)

        self.user_name_edit = QLineEdit(UserAddDialog)
        self.user_name_edit.setObjectName(u"user_name_edit")

        self.name_layout.addWidget(self.user_name_edit)


        self.grid_layout.addLayout(self.name_layout, 1, 0, 1, 1)

        self.full_name_layout = QHBoxLayout()
        self.full_name_layout.setObjectName(u"full_name_layout")
        self.full_name_label = QLabel(UserAddDialog)
        self.full_name_label.setObjectName(u"full_name_label")

        self.full_name_layout.addWidget(self.full_name_label)

        self.full_name_edit = QLineEdit(UserAddDialog)
        self.full_name_edit.setObjectName(u"full_name_edit")

        self.full_name_layout.addWidget(self.full_name_edit)


        self.grid_layout.addLayout(self.full_name_layout, 2, 0, 1, 1)


        self.verticalLayout.addLayout(self.grid_layout)

        self.button_box = QDialogButtonBox(UserAddDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.button_box)


        self.retranslateUi(UserAddDialog)
        self.button_box.accepted.connect(UserAddDialog.accept)
        self.button_box.rejected.connect(UserAddDialog.reject)

        QMetaObject.connectSlotsByName(UserAddDialog)
    # setupUi

    def retranslateUi(self, UserAddDialog):
        UserAddDialog.setWindowTitle(QCoreApplication.translate("UserAddDialog", u"Add a user", None))
        self.auto_home_button.setText(QCoreApplication.translate("UserAddDialog", u"Auto create home", None))
        self.existing_home_button.setText(QCoreApplication.translate("UserAddDialog", u"Select existing home", None))
        self.no_home_button.setText(QCoreApplication.translate("UserAddDialog", u"Don't assign home", None))
        self.home_label.setText(QCoreApplication.translate("UserAddDialog", u"Home directory", None))
        self.file_browser_button.setText(QCoreApplication.translate("UserAddDialog", u"...", None))
        self.shell_label.setText(QCoreApplication.translate("UserAddDialog", u"Shell", None))
        self.password_label.setText(QCoreApplication.translate("UserAddDialog", u"Password", None))
        self.user_name_label.setText(QCoreApplication.translate("UserAddDialog", u"Username", None))
        self.full_name_label.setText(QCoreApplication.translate("UserAddDialog", u"Full name", None))
    # retranslateUi

