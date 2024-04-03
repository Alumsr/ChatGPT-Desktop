# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QPlainTextEdit,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QSplitter, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(521, 504)
        icon = QIcon()
        icon.addFile(u"res/icon.ico", QSize(), QIcon.Normal, QIcon.Off)
        Widget.setWindowIcon(icon)
        Widget.setStyleSheet(u"")
        self.horizontalLayout_2 = QHBoxLayout(Widget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.parent_box = QGroupBox(Widget)
        self.parent_box.setObjectName(u"parent_box")
        self.verticalLayout_2 = QVBoxLayout(self.parent_box)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.header_layout = QHBoxLayout()
        self.header_layout.setSpacing(7)
        self.header_layout.setObjectName(u"header_layout")
        self.header_layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.title_label = QLabel(self.parent_box)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setMinimumSize(QSize(0, 30))
        self.title_label.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setFamilies([u"Sarasa Mono SC"])
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.title_label.setWordWrap(True)

        self.header_layout.addWidget(self.title_label)

        self.full_screen_btn = QPushButton(self.parent_box)
        self.full_screen_btn.setObjectName(u"full_screen_btn")
        self.full_screen_btn.setMinimumSize(QSize(25, 25))
        self.full_screen_btn.setMaximumSize(QSize(25, 25))
        self.full_screen_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.header_layout.addWidget(self.full_screen_btn)

        self.quit_btn = QPushButton(self.parent_box)
        self.quit_btn.setObjectName(u"quit_btn")
        self.quit_btn.setMinimumSize(QSize(25, 25))
        self.quit_btn.setMaximumSize(QSize(25, 25))
        self.quit_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.header_layout.addWidget(self.quit_btn)


        self.verticalLayout_2.addLayout(self.header_layout)

        self.body_splitter = QSplitter(self.parent_box)
        self.body_splitter.setObjectName(u"body_splitter")
        self.body_splitter.setOrientation(Qt.Vertical)
        self.input_group = QGroupBox(self.body_splitter)
        self.input_group.setObjectName(u"input_group")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_group.sizePolicy().hasHeightForWidth())
        self.input_group.setSizePolicy(sizePolicy)
        self.horizontalLayout_6 = QHBoxLayout(self.input_group)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.input_text = QPlainTextEdit(self.input_group)
        self.input_text.setObjectName(u"input_text")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.input_text.sizePolicy().hasHeightForWidth())
        self.input_text.setSizePolicy(sizePolicy1)
        self.input_text.setMinimumSize(QSize(30, 30))
        self.input_text.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setFamilies([u"Sarasa Mono SC"])
        font1.setPointSize(11)
        self.input_text.setFont(font1)
        self.input_text.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.input_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.horizontalLayout_6.addWidget(self.input_text)

        self.submit_btn_layout = QVBoxLayout()
        self.submit_btn_layout.setSpacing(0)
        self.submit_btn_layout.setObjectName(u"submit_btn_layout")
        self.submit_btn_layout.setContentsMargins(7, 7, 7, 7)
        self.input_btn_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.submit_btn_layout.addItem(self.input_btn_spacer)

        self.submit_btn = QPushButton(self.input_group)
        self.submit_btn.setObjectName(u"submit_btn")
        self.submit_btn.setMinimumSize(QSize(25, 25))
        self.submit_btn.setMaximumSize(QSize(25, 25))
        font2 = QFont()
        font2.setFamilies([u"Cascadia Code"])
        font2.setPointSize(10)
        font2.setBold(False)
        self.submit_btn.setFont(font2)
        self.submit_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.submit_btn.setIconSize(QSize(50, 50))

        self.submit_btn_layout.addWidget(self.submit_btn)


        self.horizontalLayout_6.addLayout(self.submit_btn_layout)

        self.body_splitter.addWidget(self.input_group)
        self.display_splitter = QSplitter(self.body_splitter)
        self.display_splitter.setObjectName(u"display_splitter")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.display_splitter.sizePolicy().hasHeightForWidth())
        self.display_splitter.setSizePolicy(sizePolicy2)
        self.display_splitter.setOrientation(Qt.Horizontal)
        self.display_splitter.setHandleWidth(7)
        self.chat_display = QScrollArea(self.display_splitter)
        self.chat_display.setObjectName(u"chat_display")
        self.chat_display.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chat_display.setWidgetResizable(True)
        self.chat_display.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 83, 226))
        self.chat_display.setWidget(self.scrollAreaWidgetContents)
        self.display_splitter.addWidget(self.chat_display)
        self.layoutWidget = QWidget(self.display_splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.table_vertical_layout = QVBoxLayout(self.layoutWidget)
        self.table_vertical_layout.setSpacing(7)
        self.table_vertical_layout.setObjectName(u"table_vertical_layout")
        self.table_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, -1, 0, -1)
        self.clear_btn = QPushButton(self.layoutWidget)
        self.clear_btn.setObjectName(u"clear_btn")
        self.clear_btn.setMinimumSize(QSize(0, 25))
        self.clear_btn.setMaximumSize(QSize(99999, 25))
        font3 = QFont()
        font3.setFamilies([u"Cascadia Code"])
        self.clear_btn.setFont(font3)
        self.clear_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_4.addWidget(self.clear_btn)

        self.set_btn = QPushButton(self.layoutWidget)
        self.set_btn.setObjectName(u"set_btn")
        self.set_btn.setMinimumSize(QSize(25, 25))
        self.set_btn.setMaximumSize(QSize(25, 25))
        self.set_btn.setFont(font3)
        self.set_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_4.addWidget(self.set_btn)


        self.table_vertical_layout.addLayout(self.horizontalLayout_4)

        self.tableWidget = QTableWidget(self.layoutWidget)
        if (self.tableWidget.columnCount() < 1):
            self.tableWidget.setColumnCount(1)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setMinimumSize(QSize(100, 0))
        self.tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(25)
        self.tableWidget.verticalHeader().setVisible(False)

        self.table_vertical_layout.addWidget(self.tableWidget)

        self.display_splitter.addWidget(self.layoutWidget)
        self.body_splitter.addWidget(self.display_splitter)

        self.verticalLayout_2.addWidget(self.body_splitter)


        self.horizontalLayout_2.addWidget(self.parent_box)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.title_label.setText("")
#if QT_CONFIG(tooltip)
        self.full_screen_btn.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.full_screen_btn.setText("")
#if QT_CONFIG(tooltip)
        self.quit_btn.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.quit_btn.setText("")
        self.input_group.setTitle("")
        self.submit_btn.setText("")
#if QT_CONFIG(tooltip)
        self.clear_btn.setToolTip(QCoreApplication.translate("Widget", u"New Chat", None))
#endif // QT_CONFIG(tooltip)
        self.clear_btn.setText("")
#if QT_CONFIG(tooltip)
        self.set_btn.setToolTip(QCoreApplication.translate("Widget", u"Settings", None))
#endif // QT_CONFIG(tooltip)
        self.set_btn.setText("")
    # retranslateUi

