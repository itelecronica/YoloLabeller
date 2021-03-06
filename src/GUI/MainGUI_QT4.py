# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainGUI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1920, 1080)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_selectedImage = QtGui.QLabel(self.centralwidget)
        self.label_selectedImage.setObjectName(_fromUtf8("label_selectedImage"))
        self.verticalLayout.addWidget(self.label_selectedImage)
        self.graphicsView_visualizer = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView_visualizer.setObjectName(_fromUtf8("graphicsView_visualizer"))
        self.verticalLayout.addWidget(self.graphicsView_visualizer)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_prevImg = QtGui.QPushButton(self.centralwidget)
        self.pushButton_prevImg.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_prevImg.setObjectName(_fromUtf8("pushButton_prevImg"))
        self.horizontalLayout_2.addWidget(self.pushButton_prevImg)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton_nextImg = QtGui.QPushButton(self.centralwidget)
        self.pushButton_nextImg.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_nextImg.setObjectName(_fromUtf8("pushButton_nextImg"))
        self.horizontalLayout_2.addWidget(self.pushButton_nextImg)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.horizontalLayout_2.setStretch(0, 4)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)
        self.horizontalLayout_2.setStretch(3, 1)
        self.horizontalLayout_2.setStretch(4, 4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setText(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.graphicsView_logo = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView_logo.setObjectName(_fromUtf8("graphicsView_logo"))
        self.verticalLayout_2.addWidget(self.graphicsView_logo)
        self.checkBox_showLabels = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_showLabels.setChecked(True)
        self.checkBox_showLabels.setObjectName(_fromUtf8("checkBox_showLabels"))
        self.verticalLayout_2.addWidget(self.checkBox_showLabels)
        self.groupBox_modePellets = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_modePellets.setObjectName(_fromUtf8("groupBox_modePellets"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_modePellets)
        self.verticalLayout_3.setContentsMargins(-1, 18, -1, -1)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.checkBox_mode_free = QtGui.QCheckBox(self.groupBox_modePellets)
        self.checkBox_mode_free.setChecked(True)
        self.checkBox_mode_free.setAutoExclusive(True)
        self.checkBox_mode_free.setObjectName(_fromUtf8("checkBox_mode_free"))
        self.verticalLayout_3.addWidget(self.checkBox_mode_free)
        self.checkBox_mode_fixed = QtGui.QCheckBox(self.groupBox_modePellets)
        self.checkBox_mode_fixed.setAutoExclusive(True)
        self.checkBox_mode_fixed.setObjectName(_fromUtf8("checkBox_mode_fixed"))
        self.verticalLayout_3.addWidget(self.checkBox_mode_fixed)
        self.verticalLayout_2.addWidget(self.groupBox_modePellets)
        self.groupBox_selectClass = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_selectClass.setObjectName(_fromUtf8("groupBox_selectClass"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.groupBox_selectClass)
        self.horizontalLayout_3.setContentsMargins(-1, 18, -1, -1)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.listWidget_classes = QtGui.QListWidget(self.groupBox_selectClass)
        self.listWidget_classes.setObjectName(_fromUtf8("listWidget_classes"))
        self.horizontalLayout_3.addWidget(self.listWidget_classes)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.textEdit_newClass = QtGui.QTextEdit(self.groupBox_selectClass)
        self.textEdit_newClass.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textEdit_newClass.setObjectName(_fromUtf8("textEdit_newClass"))
        self.verticalLayout_5.addWidget(self.textEdit_newClass)
        self.pushButton_addClass = QtGui.QPushButton(self.groupBox_selectClass)
        self.pushButton_addClass.setObjectName(_fromUtf8("pushButton_addClass"))
        self.verticalLayout_5.addWidget(self.pushButton_addClass)
        self.pushButton_deleteClass = QtGui.QPushButton(self.groupBox_selectClass)
        self.pushButton_deleteClass.setObjectName(_fromUtf8("pushButton_deleteClass"))
        self.verticalLayout_5.addWidget(self.pushButton_deleteClass)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem4)
        self.verticalLayout_5.setStretch(0, 2)
        self.verticalLayout_5.setStretch(1, 1)
        self.verticalLayout_5.setStretch(2, 1)
        self.verticalLayout_5.setStretch(3, 2)
        self.verticalLayout_5.setStretch(4, 2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        self.horizontalLayout_3.setStretch(0, 3)
        self.horizontalLayout_3.setStretch(1, 2)
        self.verticalLayout_2.addWidget(self.groupBox_selectClass)
        self.groupBox_format = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_format.setObjectName(_fromUtf8("groupBox_format"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox_format)
        self.verticalLayout_4.setContentsMargins(-1, 18, -1, 9)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.checkBox_FormatYolotxt = QtGui.QCheckBox(self.groupBox_format)
        self.checkBox_FormatYolotxt.setAutoExclusive(True)
        self.checkBox_FormatYolotxt.setObjectName(_fromUtf8("checkBox_FormatYolotxt"))
        self.verticalLayout_4.addWidget(self.checkBox_FormatYolotxt)
        self.checkBox_FormatYoloxml = QtGui.QCheckBox(self.groupBox_format)
        self.checkBox_FormatYoloxml.setAutoExclusive(True)
        self.checkBox_FormatYoloxml.setObjectName(_fromUtf8("checkBox_FormatYoloxml"))
        self.verticalLayout_4.addWidget(self.checkBox_FormatYoloxml)
        self.verticalLayout_2.addWidget(self.groupBox_format)
        self.groupBox_pelletsScale = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_pelletsScale.setObjectName(_fromUtf8("groupBox_pelletsScale"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.groupBox_pelletsScale)
        self.horizontalLayout_4.setContentsMargins(-1, 18, -1, -1)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.graphicsView_pelletImg = QtGui.QGraphicsView(self.groupBox_pelletsScale)
        self.graphicsView_pelletImg.setObjectName(_fromUtf8("graphicsView_pelletImg"))
        self.verticalLayout_6.addWidget(self.graphicsView_pelletImg)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_2 = QtGui.QLabel(self.groupBox_pelletsScale)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_5.addWidget(self.label_2)
        self.label_pixels = QtGui.QLabel(self.groupBox_pelletsScale)
        self.label_pixels.setObjectName(_fromUtf8("label_pixels"))
        self.horizontalLayout_5.addWidget(self.label_pixels)
        self.horizontalSlider_size_pellets = QtGui.QSlider(self.groupBox_pelletsScale)
        self.horizontalSlider_size_pellets.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_size_pellets.setObjectName(_fromUtf8("horizontalSlider_size_pellets"))
        self.horizontalLayout_5.addWidget(self.horizontalSlider_size_pellets)
        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 1)
        self.horizontalLayout_5.setStretch(2, 5)
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4.addLayout(self.verticalLayout_6)
        self.horizontalLayout_4.setStretch(0, 4)
        self.verticalLayout_2.addWidget(self.groupBox_pelletsScale)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem5)
        self.pushButton_save = QtGui.QPushButton(self.centralwidget)
        self.pushButton_save.setObjectName(_fromUtf8("pushButton_save"))
        self.verticalLayout_2.addWidget(self.pushButton_save)
        self.pushButton_discard = QtGui.QPushButton(self.centralwidget)
        self.pushButton_discard.setObjectName(_fromUtf8("pushButton_discard"))
        self.verticalLayout_2.addWidget(self.pushButton_discard)
        self.verticalLayout_2.setStretch(1, 2)
        self.verticalLayout_2.setStretch(2, 1)
        self.verticalLayout_2.setStretch(3, 1)
        self.verticalLayout_2.setStretch(4, 2)
        self.verticalLayout_2.setStretch(5, 1)
        self.verticalLayout_2.setStretch(6, 4)
        self.verticalLayout_2.setStretch(7, 2)
        self.verticalLayout_2.setStretch(8, 1)
        self.verticalLayout_2.setStretch(9, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.setStretch(0, 4)
        self.horizontalLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label_selectedImage.setText(_translate("MainWindow", "Mostrando imagen: 0 de 0", None))
        self.pushButton_prevImg.setText(_translate("MainWindow", "<", None))
        self.pushButton_nextImg.setText(_translate("MainWindow", ">", None))
        self.checkBox_showLabels.setText(_translate("MainWindow", "Show Labels", None))
        self.groupBox_modePellets.setTitle(_translate("MainWindow", "Pellets Mode", None))
        self.checkBox_mode_free.setText(_translate("MainWindow", "Free Selection Mode", None))
        self.checkBox_mode_fixed.setText(_translate("MainWindow", "Fixed Mode", None))
        self.groupBox_selectClass.setTitle(_translate("MainWindow", "Selected Class", None))
        self.pushButton_addClass.setText(_translate("MainWindow", "Add", None))
        self.pushButton_deleteClass.setText(_translate("MainWindow", "Delete", None))
        self.groupBox_format.setTitle(_translate("MainWindow", "Output Format", None))
        self.checkBox_FormatYolotxt.setText(_translate("MainWindow", "YoloTXT", None))
        self.checkBox_FormatYoloxml.setText(_translate("MainWindow", "YoloXML", None))
        self.groupBox_pelletsScale.setTitle(_translate("MainWindow", "Pellets Scale Configuration", None))
        self.label_2.setText(_translate("MainWindow", "Scale:", None))
        self.label_pixels.setText(_translate("MainWindow", "0 px", None))
        self.pushButton_save.setText(_translate("MainWindow", "Save", None))
        self.pushButton_discard.setText(_translate("MainWindow", "Discard", None))

