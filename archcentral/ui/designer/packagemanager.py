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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPlainTextEdit, QPushButton, QSizePolicy,
    QTabWidget, QTableView, QVBoxLayout, QWidget)

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
        self.update_button.setEnabled(False)

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
        self.verticalLayout_3 = QVBoxLayout(self.management)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalWidget_2 = QWidget(self.management)
        self.horizontalWidget_2.setObjectName(u"horizontalWidget_2")
        self.horizontalWidget_2.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.package_search = QLineEdit(self.horizontalWidget_2)
        self.package_search.setObjectName(u"package_search")

        self.horizontalLayout_2.addWidget(self.package_search)

        self.pushButton_3 = QPushButton(self.horizontalWidget_2)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_2.addWidget(self.pushButton_3)


        self.verticalLayout_3.addWidget(self.horizontalWidget_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.package_list_table = QTableView(self.management)
        self.package_list_table.setObjectName(u"package_list_table")

        self.horizontalLayout.addWidget(self.package_list_table)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.pushButton_2 = QPushButton(self.management)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout_4.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.management)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_4.addWidget(self.pushButton)


        self.horizontalLayout.addLayout(self.verticalLayout_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.tabWidget = QTabWidget(self.management)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout_3.addWidget(self.tabWidget)

        self.content.addTab(self.management, "")

        self.verticalLayout.addWidget(self.content)


        self.retranslateUi(PackageManager)

        self.content.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PackageManager)
    # setupUi

    def retranslateUi(self, PackageManager):
        PackageManager.setWindowTitle(QCoreApplication.translate("PackageManager", u"Form", None))
        self.title.setText(QCoreApplication.translate("PackageManager", u"Package Manager", None))
        self.fetch_update_button.setText(QCoreApplication.translate("PackageManager", u"Fetch updates", None))
        self.update_button.setText(QCoreApplication.translate("PackageManager", u"Update", None))
        self.pacman_output.setPlaceholderText(QCoreApplication.translate("PackageManager", u"Pacman update output will be printed here...", None))
        self.content.setTabText(self.content.indexOf(self.update), QCoreApplication.translate("PackageManager", u"Update packages", None))
        self.package_search.setPlaceholderText(QCoreApplication.translate("PackageManager", u"Search a package...", None))
        self.pushButton_3.setText(QCoreApplication.translate("PackageManager", u"PushButton", None))
        self.pushButton_2.setText(QCoreApplication.translate("PackageManager", u"PushButton", None))
        self.pushButton.setText(QCoreApplication.translate("PackageManager", u"PushButton", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("PackageManager", u"Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("PackageManager", u"Tab 2", None))
        self.content.setTabText(self.content.indexOf(self.management), QCoreApplication.translate("PackageManager", u"Install/Remove packages", None))
    # retranslateUi

