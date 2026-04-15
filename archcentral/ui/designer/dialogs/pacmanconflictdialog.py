# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pacmanconflictdialog.ui'
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

class Ui_PacmanConflictDialog(object):
    def setupUi(self, PacmanConflictDialog):
        if not PacmanConflictDialog.objectName():
            PacmanConflictDialog.setObjectName(u"PacmanConflictDialog")
        PacmanConflictDialog.resize(400, 100)
        PacmanConflictDialog.setMaximumSize(QSize(16777215, 100))
        self.verticalLayout = QVBoxLayout(PacmanConflictDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.conflict_label = QLabel(PacmanConflictDialog)
        self.conflict_label.setObjectName(u"conflict_label")

        self.verticalLayout.addWidget(self.conflict_label)

        self.label = QLabel(PacmanConflictDialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.button_box = QDialogButtonBox(PacmanConflictDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.No|QDialogButtonBox.StandardButton.Yes)

        self.verticalLayout.addWidget(self.button_box)


        self.retranslateUi(PacmanConflictDialog)
        self.button_box.accepted.connect(PacmanConflictDialog.accept)
        self.button_box.rejected.connect(PacmanConflictDialog.reject)

        QMetaObject.connectSlotsByName(PacmanConflictDialog)
    # setupUi

    def retranslateUi(self, PacmanConflictDialog):
        PacmanConflictDialog.setWindowTitle(QCoreApplication.translate("PacmanConflictDialog", u"Package conflict detected", None))
        self.conflict_label.setText("")
        self.label.setText(QCoreApplication.translate("PacmanConflictDialog", u"Refusing will quit the operation.", None))
    # retranslateUi

