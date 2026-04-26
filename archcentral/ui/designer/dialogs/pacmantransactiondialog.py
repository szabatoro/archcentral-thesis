# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pacmantransactiondialog.ui'
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

class Ui_PacmanTransactionDialog(object):
    def setupUi(self, PacmanTransactionDialog):
        if not PacmanTransactionDialog.objectName():
            PacmanTransactionDialog.setObjectName(u"PacmanTransactionDialog")
        PacmanTransactionDialog.resize(400, 100)
        PacmanTransactionDialog.setMaximumSize(QSize(16777215, 100))
        self.verticalLayout = QVBoxLayout(PacmanTransactionDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.info_label = QLabel(PacmanTransactionDialog)
        self.info_label.setObjectName(u"info_label")

        self.verticalLayout.addWidget(self.info_label)

        self.button_box = QDialogButtonBox(PacmanTransactionDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.No|QDialogButtonBox.StandardButton.Yes)

        self.verticalLayout.addWidget(self.button_box)


        self.retranslateUi(PacmanTransactionDialog)
        self.button_box.accepted.connect(PacmanTransactionDialog.accept)
        self.button_box.rejected.connect(PacmanTransactionDialog.reject)

        QMetaObject.connectSlotsByName(PacmanTransactionDialog)
    # setupUi

    def retranslateUi(self, PacmanTransactionDialog):
        PacmanTransactionDialog.setWindowTitle(QCoreApplication.translate("PacmanTransactionDialog", u"Package conflict detected", None))
        self.info_label.setText("")
    # retranslateUi

