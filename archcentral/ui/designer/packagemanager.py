# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'packagemanager.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QPlainTextEdit,
    QPushButton, QSizePolicy, QTabWidget, QTableView,
    QVBoxLayout, QWidget)

class Ui_PackageManager(object):
    def setupUi(self, PackageManager):
        if not PackageManager.objectName():
            PackageManager.setObjectName(u"PackageManager")
        PackageManager.resize(927, 623)
        self.verticalLayout = QVBoxLayout(PackageManager)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title = QLabel(PackageManager)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.title.setFont(font)

        self.verticalLayout.addWidget(self.title)

        self.content = QTabWidget(PackageManager)
        self.content.setObjectName(u"content")
        self.update = QWidget()
        self.update.setObjectName(u"update")
        self.verticalLayout_2 = QVBoxLayout(self.update)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.update_table = QTableView(self.update)
        self.update_table.setObjectName(u"update_table")

        self.verticalLayout_2.addWidget(self.update_table)

        self.fetch_update_button = QPushButton(self.update)
        self.fetch_update_button.setObjectName(u"fetch_update_button")

        self.verticalLayout_2.addWidget(self.fetch_update_button)

        self.update_button = QPushButton(self.update)
        self.update_button.setObjectName(u"update_button")

        self.verticalLayout_2.addWidget(self.update_button)

        self.pacman_output = QPlainTextEdit(self.update)
        self.pacman_output.setObjectName(u"pacman_output")
        self.pacman_output.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.pacman_output)

        self.content.addTab(self.update, "")
        self.management = QWidget()
        self.management.setObjectName(u"management")
        font1 = QFont()
        font1.setBold(True)
        self.management.setFont(font1)
        self.content.addTab(self.management, "")

        self.verticalLayout.addWidget(self.content)


        self.retranslateUi(PackageManager)

        self.content.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PackageManager)
    # setupUi

    def retranslateUi(self, PackageManager):
        PackageManager.setWindowTitle(QCoreApplication.translate("PackageManager", u"Form", None))
        self.title.setText(QCoreApplication.translate("PackageManager", u"Package Manager", None))
        self.fetch_update_button.setText(QCoreApplication.translate("PackageManager", u"Fetch updates", None))
        self.update_button.setText(QCoreApplication.translate("PackageManager", u"Update", None))
        self.pacman_output.setPlaceholderText(QCoreApplication.translate("PackageManager", u"Pacman update output will be printed here...", None))
        self.content.setTabText(self.content.indexOf(self.update), QCoreApplication.translate("PackageManager", u"Update packages", None))
        self.content.setTabText(self.content.indexOf(self.management), QCoreApplication.translate("PackageManager", u"Install/Remove packages", None))
    # retranslateUi

