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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QSizePolicy, QTabWidget, QTableView, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_PackageManager(object):
    def setupUi(self, PackageManager):
        if not PackageManager.objectName():
            PackageManager.setObjectName(u"PackageManager")
        PackageManager.resize(927, 623)
        self.verticalLayout_7 = QVBoxLayout(PackageManager)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.title = QLabel(PackageManager)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.title.setFont(font)

        self.verticalLayout_7.addWidget(self.title)

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
        self.verticalLayout_8 = QVBoxLayout(self.management)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.search_layout = QWidget(self.management)
        self.search_layout.setObjectName(u"search_layout")
        self.search_layout.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_2 = QHBoxLayout(self.search_layout)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.package_search = QLineEdit(self.search_layout)
        self.package_search.setObjectName(u"package_search")

        self.horizontalLayout_2.addWidget(self.package_search)

        self.package_search_button = QPushButton(self.search_layout)
        self.package_search_button.setObjectName(u"package_search_button")

        self.horizontalLayout_2.addWidget(self.package_search_button)


        self.verticalLayout_8.addWidget(self.search_layout)

        self.package_list_layout = QHBoxLayout()
        self.package_list_layout.setObjectName(u"package_list_layout")
        self.package_list_table = QTableView(self.management)
        self.package_list_table.setObjectName(u"package_list_table")
        self.package_list_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.package_list_table.horizontalHeader().setStretchLastSection(True)
        self.package_list_table.verticalHeader().setVisible(False)

        self.package_list_layout.addWidget(self.package_list_table)

        self.package_list_options_layout = QVBoxLayout()
        self.package_list_options_layout.setObjectName(u"package_list_options_layout")
        self.pushButton_2 = QPushButton(self.management)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.package_list_options_layout.addWidget(self.pushButton_2)


        self.package_list_layout.addLayout(self.package_list_options_layout)


        self.verticalLayout_8.addLayout(self.package_list_layout)

        self.operations_layout = QHBoxLayout()
        self.operations_layout.setObjectName(u"operations_layout")
        self.tabWidget = QTabWidget(self.management)
        self.tabWidget.setObjectName(u"tabWidget")
        self.package_details_tab = QWidget()
        self.package_details_tab.setObjectName(u"package_details_tab")
        self.verticalLayout_5 = QVBoxLayout(self.package_details_tab)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.package_details_tree = QTreeWidget(self.package_details_tab)
        self.package_details_tree.setObjectName(u"package_details_tree")
        self.package_details_tree.setColumnCount(2)
        self.package_details_tree.header().setVisible(True)
        self.package_details_tree.header().setCascadingSectionResizes(True)

        self.verticalLayout_5.addWidget(self.package_details_tree)

        self.tabWidget.addTab(self.package_details_tab, "")
        self.pacman_output_tab = QWidget()
        self.pacman_output_tab.setObjectName(u"pacman_output_tab")
        self.verticalLayout_6 = QVBoxLayout(self.pacman_output_tab)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.pacman_output_tr = QPlainTextEdit(self.pacman_output_tab)
        self.pacman_output_tr.setObjectName(u"pacman_output_tr")

        self.verticalLayout_6.addWidget(self.pacman_output_tr)

        self.tabWidget.addTab(self.pacman_output_tab, "")

        self.operations_layout.addWidget(self.tabWidget)

        self.operation_buttons_layout = QVBoxLayout()
        self.operation_buttons_layout.setObjectName(u"operation_buttons_layout")
        self.run_transaction_button = QPushButton(self.management)
        self.run_transaction_button.setObjectName(u"run_transaction_button")

        self.operation_buttons_layout.addWidget(self.run_transaction_button)


        self.operations_layout.addLayout(self.operation_buttons_layout)


        self.verticalLayout_8.addLayout(self.operations_layout)

        self.content.addTab(self.management, "")

        self.verticalLayout_7.addWidget(self.content)


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
        self.package_search_button.setText(QCoreApplication.translate("PackageManager", u"Search", None))
        self.pushButton_2.setText(QCoreApplication.translate("PackageManager", u"PushButton", None))
        ___qtreewidgetitem = self.package_details_tree.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("PackageManager", u"Value", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("PackageManager", u"Name", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.package_details_tab), QCoreApplication.translate("PackageManager", u"Package details", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pacman_output_tab), QCoreApplication.translate("PackageManager", u"Pacman output", None))
        self.run_transaction_button.setText(QCoreApplication.translate("PackageManager", u"Run", None))
        self.content.setTabText(self.content.indexOf(self.management), QCoreApplication.translate("PackageManager", u"Install/Remove packages", None))
    # retranslateUi

