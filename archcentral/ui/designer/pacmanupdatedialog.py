# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pacmanupdatedialog.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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

class Ui_PacmanUpdateDialog(object):
    def setupUi(self, PacmanUpdateDialog):
        if not PacmanUpdateDialog.objectName():
            PacmanUpdateDialog.setObjectName(u"PacmanUpdateDialog")
        PacmanUpdateDialog.resize(391, 207)
        self.verticalLayout = QVBoxLayout(PacmanUpdateDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.update_info = QLabel(PacmanUpdateDialog)
        self.update_info.setObjectName(u"update_info")

        self.verticalLayout.addWidget(self.update_info)

        self.label = QLabel(PacmanUpdateDialog)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout.addWidget(self.label)

        self.confirm_box = QDialogButtonBox(PacmanUpdateDialog)
        self.confirm_box.setObjectName(u"confirm_box")
        self.confirm_box.setOrientation(Qt.Orientation.Horizontal)
        self.confirm_box.setStandardButtons(QDialogButtonBox.StandardButton.No|QDialogButtonBox.StandardButton.Yes)

        self.verticalLayout.addWidget(self.confirm_box)


        self.retranslateUi(PacmanUpdateDialog)
        self.confirm_box.accepted.connect(PacmanUpdateDialog.accept)
        self.confirm_box.rejected.connect(PacmanUpdateDialog.reject)

        QMetaObject.connectSlotsByName(PacmanUpdateDialog)
    # setupUi

    def retranslateUi(self, PacmanUpdateDialog):
        PacmanUpdateDialog.setWindowTitle(QCoreApplication.translate("PacmanUpdateDialog", u"Dialog", None))
        self.update_info.setText(QCoreApplication.translate("PacmanUpdateDialog", u"Update info.", None))
        self.label.setText(QCoreApplication.translate("PacmanUpdateDialog", u"Are you sure you want to proceed with this update?", None))
    # retranslateUi

