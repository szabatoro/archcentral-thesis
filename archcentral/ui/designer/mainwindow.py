# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 800)
        MainWindow.setMinimumSize(QSize(1000, 800))
        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName(u"central_widget")
        self.horizontalLayout = QHBoxLayout(self.central_widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.sidebar = QFrame(self.central_widget)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setMinimumSize(QSize(150, 0))
        self.sidebar.setFrameShape(QFrame.Shape.NoFrame)
        self.sidebar.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.sidebar)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.app_title = QLabel(self.sidebar)
        self.app_title.setObjectName(u"app_title")
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.app_title.setFont(font)

        self.verticalLayout.addWidget(self.app_title)

        self.app_ver = QLabel(self.sidebar)
        self.app_ver.setObjectName(u"app_ver")

        self.verticalLayout.addWidget(self.app_ver)

        self.menu_buttons = QFrame(self.sidebar)
        self.menu_buttons.setObjectName(u"menu_buttons")
        self.menu_buttons.setStyleSheet(u"QPushButton { border: 1px solid white; margin: 0 px; border-top: 0px; border-right: 0px; border-left: 0px; height: 30 px }\n"
"QPushButton:checked { border: 1px solid white; margin: 0 px; background-color:rgb(94, 94, 94); border-top: 0px; border-right: 0px; border-left: 0px; }")
        self.menu_buttons.setFrameShape(QFrame.Shape.Box)
        self.menu_buttons.setFrameShadow(QFrame.Shadow.Plain)
        self.menu_buttons.setLineWidth(1)
        self.menu_buttons.setMidLineWidth(0)
        self.menu_options = QVBoxLayout(self.menu_buttons)
        self.menu_options.setSpacing(0)
        self.menu_options.setObjectName(u"menu_options")
        self.menu_options.setContentsMargins(0, 0, 0, 0)
        self.sys_info_button = QPushButton(self.menu_buttons)
        self.sys_info_button.setObjectName(u"sys_info_button")
        icon = QIcon(QIcon.fromTheme(u"computer"))
        self.sys_info_button.setIcon(icon)
        self.sys_info_button.setCheckable(True)
        self.sys_info_button.setChecked(False)
        self.sys_info_button.setAutoExclusive(True)

        self.menu_options.addWidget(self.sys_info_button)

        self.package_manager_button = QPushButton(self.menu_buttons)
        self.package_manager_button.setObjectName(u"package_manager_button")
        icon1 = QIcon(QIcon.fromTheme(u"package-x-generic"))
        self.package_manager_button.setIcon(icon1)
        self.package_manager_button.setCheckable(True)
        self.package_manager_button.setAutoExclusive(True)

        self.menu_options.addWidget(self.package_manager_button)

        self.spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.menu_options.addItem(self.spacer)


        self.verticalLayout.addWidget(self.menu_buttons)


        self.horizontalLayout.addWidget(self.sidebar)

        self.display_area = QStackedWidget(self.central_widget)
        self.display_area.setObjectName(u"display_area")
        self.display_area.setStyleSheet(u"")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.display_area.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.display_area.addWidget(self.page_2)

        self.horizontalLayout.addWidget(self.display_area)

        MainWindow.setCentralWidget(self.central_widget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ArchCentral", None))
        self.app_title.setText(QCoreApplication.translate("MainWindow", u"ArchCentral", None))
        self.app_ver.setText(QCoreApplication.translate("MainWindow", u"Version: ", None))
        self.sys_info_button.setText(QCoreApplication.translate("MainWindow", u"System Info", None))
        self.package_manager_button.setText(QCoreApplication.translate("MainWindow", u"Package Manager", None))
    # retranslateUi

