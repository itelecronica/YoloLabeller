# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainGUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_selectedImage = QtWidgets.QLabel(self.centralwidget)
        self.label_selectedImage.setObjectName("label_selectedImage")
        self.verticalLayout.addWidget(self.label_selectedImage)
        self.graphicsView_visualizer = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_visualizer.setObjectName("graphicsView_visualizer")
        self.verticalLayout.addWidget(self.graphicsView_visualizer)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_prevImg = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_prevImg.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_prevImg.setObjectName("pushButton_prevImg")
        self.horizontalLayout_2.addWidget(self.pushButton_prevImg)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton_nextImg = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_nextImg.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_nextImg.setObjectName("pushButton_nextImg")
        self.horizontalLayout_2.addWidget(self.pushButton_nextImg)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.horizontalLayout_2.setStretch(0, 4)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)
        self.horizontalLayout_2.setStretch(3, 1)
        self.horizontalLayout_2.setStretch(4, 4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.graphicsView_logo = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView_logo.setObjectName("graphicsView_logo")
        self.verticalLayout_8.addWidget(self.graphicsView_logo)
        self.verticalLayout_7.addWidget(self.frame)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.PageDetection = QtWidgets.QWidget()
        self.PageDetection.setObjectName("PageDetection")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.PageDetection)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.PageDetection)
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.checkBox_showLabels = QtWidgets.QCheckBox(self.PageDetection)
        self.checkBox_showLabels.setChecked(True)
        self.checkBox_showLabels.setObjectName("checkBox_showLabels")
        self.verticalLayout_2.addWidget(self.checkBox_showLabels)
        self.groupBox_modePellets = QtWidgets.QGroupBox(self.PageDetection)
        self.groupBox_modePellets.setObjectName("groupBox_modePellets")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_modePellets)
        self.verticalLayout_3.setContentsMargins(-1, 18, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.checkBox_mode_free = QtWidgets.QCheckBox(self.groupBox_modePellets)
        self.checkBox_mode_free.setChecked(True)
        self.checkBox_mode_free.setAutoExclusive(True)
        self.checkBox_mode_free.setObjectName("checkBox_mode_free")
        self.verticalLayout_3.addWidget(self.checkBox_mode_free)
        self.checkBox_mode_fixed = QtWidgets.QCheckBox(self.groupBox_modePellets)
        self.checkBox_mode_fixed.setAutoExclusive(True)
        self.checkBox_mode_fixed.setObjectName("checkBox_mode_fixed")
        self.verticalLayout_3.addWidget(self.checkBox_mode_fixed)
        self.verticalLayout_2.addWidget(self.groupBox_modePellets)
        self.groupBox_selectClass = QtWidgets.QGroupBox(self.PageDetection)
        self.groupBox_selectClass.setObjectName("groupBox_selectClass")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_selectClass)
        self.horizontalLayout_3.setContentsMargins(-1, 18, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.listWidget_classes = QtWidgets.QListWidget(self.groupBox_selectClass)
        self.listWidget_classes.setObjectName("listWidget_classes")
        self.horizontalLayout_3.addWidget(self.listWidget_classes)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.textEdit_newClass = QtWidgets.QTextEdit(self.groupBox_selectClass)
        self.textEdit_newClass.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textEdit_newClass.setObjectName("textEdit_newClass")
        self.verticalLayout_5.addWidget(self.textEdit_newClass)
        self.pushButton_addClass = QtWidgets.QPushButton(self.groupBox_selectClass)
        self.pushButton_addClass.setObjectName("pushButton_addClass")
        self.verticalLayout_5.addWidget(self.pushButton_addClass)
        self.pushButton_deleteClass = QtWidgets.QPushButton(self.groupBox_selectClass)
        self.pushButton_deleteClass.setObjectName("pushButton_deleteClass")
        self.verticalLayout_5.addWidget(self.pushButton_deleteClass)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
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
        self.groupBox_format = QtWidgets.QGroupBox(self.PageDetection)
        self.groupBox_format.setObjectName("groupBox_format")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_format)
        self.verticalLayout_4.setContentsMargins(-1, 18, -1, 9)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.checkBox_FormatYolotxt = QtWidgets.QCheckBox(self.groupBox_format)
        self.checkBox_FormatYolotxt.setAutoExclusive(True)
        self.checkBox_FormatYolotxt.setObjectName("checkBox_FormatYolotxt")
        self.verticalLayout_4.addWidget(self.checkBox_FormatYolotxt)
        self.checkBox_FormatYoloxml = QtWidgets.QCheckBox(self.groupBox_format)
        self.checkBox_FormatYoloxml.setEnabled(False)
        self.checkBox_FormatYoloxml.setAutoExclusive(True)
        self.checkBox_FormatYoloxml.setObjectName("checkBox_FormatYoloxml")
        self.verticalLayout_4.addWidget(self.checkBox_FormatYoloxml)
        self.verticalLayout_2.addWidget(self.groupBox_format)
        self.groupBox_pelletsScale = QtWidgets.QGroupBox(self.PageDetection)
        self.groupBox_pelletsScale.setObjectName("groupBox_pelletsScale")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_pelletsScale)
        self.horizontalLayout_4.setContentsMargins(-1, 18, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.graphicsView_pelletImg = QtWidgets.QGraphicsView(self.groupBox_pelletsScale)
        self.graphicsView_pelletImg.setObjectName("graphicsView_pelletImg")
        self.verticalLayout_6.addWidget(self.graphicsView_pelletImg)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.groupBox_pelletsScale)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.label_pixels = QtWidgets.QLabel(self.groupBox_pelletsScale)
        self.label_pixels.setObjectName("label_pixels")
        self.horizontalLayout_5.addWidget(self.label_pixels)
        self.horizontalSlider_size_pellets = QtWidgets.QSlider(self.groupBox_pelletsScale)
        self.horizontalSlider_size_pellets.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_size_pellets.setObjectName("horizontalSlider_size_pellets")
        self.horizontalLayout_5.addWidget(self.horizontalSlider_size_pellets)
        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 1)
        self.horizontalLayout_5.setStretch(2, 5)
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4.addLayout(self.verticalLayout_6)
        self.horizontalLayout_4.setStretch(0, 4)
        self.verticalLayout_2.addWidget(self.groupBox_pelletsScale)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem5)
        self.pushButton_save = QtWidgets.QPushButton(self.PageDetection)
        self.pushButton_save.setObjectName("pushButton_save")
        self.verticalLayout_2.addWidget(self.pushButton_save)
        self.pushButton_discard = QtWidgets.QPushButton(self.PageDetection)
        self.pushButton_discard.setObjectName("pushButton_discard")
        self.verticalLayout_2.addWidget(self.pushButton_discard)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 2)
        self.verticalLayout_2.setStretch(3, 1)
        self.verticalLayout_2.setStretch(4, 4)
        self.verticalLayout_2.setStretch(5, 2)
        self.verticalLayout_2.setStretch(6, 1)
        self.verticalLayout_2.setStretch(7, 1)
        self.verticalLayout_2.setStretch(8, 1)
        self.tabWidget.addTab(self.PageDetection, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem6)
        self.checkBox_labelsSegmentation = QtWidgets.QCheckBox(self.tab)
        self.checkBox_labelsSegmentation.setObjectName("checkBox_labelsSegmentation")
        self.verticalLayout_9.addWidget(self.checkBox_labelsSegmentation)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem7)
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidget_clasesSegmentation = QtWidgets.QListWidget(self.groupBox)
        self.listWidget_clasesSegmentation.setObjectName("listWidget_clasesSegmentation")
        self.gridLayout.addWidget(self.listWidget_clasesSegmentation, 0, 0, 1, 1)
        self.verticalLayout_9.addWidget(self.groupBox)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem8)
        self.checkBox_onlyOneClass = QtWidgets.QCheckBox(self.tab)
        self.checkBox_onlyOneClass.setObjectName("checkBox_onlyOneClass")
        self.verticalLayout_9.addWidget(self.checkBox_onlyOneClass)
        self.comboBox_Class = QtWidgets.QComboBox(self.tab)
        self.comboBox_Class.setEnabled(False)
        self.comboBox_Class.setObjectName("comboBox_Class")
        self.comboBox_Class.addItem("")
        self.comboBox_Class.setItemText(0, "")
        self.verticalLayout_9.addWidget(self.comboBox_Class)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem9)
        self.groupBox1 = QtWidgets.QGroupBox(self.tab)
        self.groupBox1.setObjectName("groupBox1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem10, 0, 0, 1, 1)
        self.lineEdit_Class3 = QtWidgets.QLineEdit(self.groupBox1)
        self.lineEdit_Class3.setObjectName("lineEdit_Class3")
        self.gridLayout_2.addWidget(self.lineEdit_Class3, 2, 3, 1, 1)
        self.lineEdit_Class1 = QtWidgets.QLineEdit(self.groupBox1)
        self.lineEdit_Class1.setObjectName("lineEdit_Class1")
        self.gridLayout_2.addWidget(self.lineEdit_Class1, 0, 3, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem11, 0, 2, 1, 1)
        self.label_Class2 = QtWidgets.QLabel(self.groupBox1)
        self.label_Class2.setObjectName("label_Class2")
        self.gridLayout_2.addWidget(self.label_Class2, 1, 1, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox1)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_2.addWidget(self.lineEdit_2, 1, 3, 1, 1)
        self.label_Class3 = QtWidgets.QLabel(self.groupBox1)
        self.label_Class3.setObjectName("label_Class3")
        self.gridLayout_2.addWidget(self.label_Class3, 2, 1, 1, 1)
        self.label_Class1 = QtWidgets.QLabel(self.groupBox1)
        self.label_Class1.setObjectName("label_Class1")
        self.gridLayout_2.addWidget(self.label_Class1, 0, 1, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem12, 0, 4, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 2)
        self.gridLayout_2.setColumnStretch(2, 2)
        self.gridLayout_2.setColumnStretch(3, 1)
        self.gridLayout_2.setColumnStretch(4, 1)
        self.gridLayout_2.setRowStretch(0, 1)
        self.gridLayout_2.setRowStretch(1, 1)
        self.gridLayout_2.setRowStretch(2, 1)
        self.verticalLayout_9.addWidget(self.groupBox1)
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem13)
        self.verticalLayout_9.setStretch(0, 1)
        self.verticalLayout_9.setStretch(1, 4)
        self.verticalLayout_9.setStretch(2, 1)
        self.verticalLayout_9.setStretch(3, 2)
        self.verticalLayout_9.setStretch(4, 1)
        self.verticalLayout_9.setStretch(5, 2)
        self.verticalLayout_9.setStretch(6, 2)
        self.verticalLayout_9.setStretch(7, 1)
        self.verticalLayout_9.setStretch(8, 2)
        self.verticalLayout_9.setStretch(9, 1)
        self.tabWidget.addTab(self.tab, "")
        self.verticalLayout_7.addWidget(self.tabWidget)
        spacerItem14 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem14)
        self.verticalLayout_7.setStretch(0, 1)
        self.verticalLayout_7.setStretch(1, 38)
        self.verticalLayout_7.setStretch(2, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_7)
        self.horizontalLayout.setStretch(0, 4)
        self.horizontalLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_selectedImage.setText(_translate("MainWindow", "&Mostrando imagen: 0 de 0"))
        self.pushButton_prevImg.setText(_translate("MainWindow", "<"))
        self.pushButton_nextImg.setText(_translate("MainWindow", ">"))
        self.checkBox_showLabels.setText(_translate("MainWindow", "Show Labels"))
        self.groupBox_modePellets.setTitle(_translate("MainWindow", "Pellets Mode"))
        self.checkBox_mode_free.setText(_translate("MainWindow", "Free Selection Mode"))
        self.checkBox_mode_fixed.setText(_translate("MainWindow", "Fixed Mode"))
        self.groupBox_selectClass.setTitle(_translate("MainWindow", "Selected Class"))
        self.pushButton_addClass.setText(_translate("MainWindow", "Add"))
        self.pushButton_deleteClass.setText(_translate("MainWindow", "Delete"))
        self.groupBox_format.setTitle(_translate("MainWindow", "Output Format"))
        self.checkBox_FormatYolotxt.setText(_translate("MainWindow", "YoloTXT"))
        self.checkBox_FormatYoloxml.setText(_translate("MainWindow", "YoloXML"))
        self.groupBox_pelletsScale.setTitle(_translate("MainWindow", "Fixed Scale"))
        self.label_2.setText(_translate("MainWindow", "Sca&le:"))
        self.label_pixels.setText(_translate("MainWindow", "&0 px"))
        self.pushButton_save.setText(_translate("MainWindow", "Save"))
        self.pushButton_discard.setText(_translate("MainWindow", "Discard"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.PageDetection), _translate("MainWindow", "Deteccion Obj"))
        self.checkBox_labelsSegmentation.setText(_translate("MainWindow", "Show Labels"))
        self.groupBox.setTitle(_translate("MainWindow", "Classes"))
        self.checkBox_onlyOneClass.setText(_translate("MainWindow", "Show 1 Class"))
        self.groupBox1.setTitle(_translate("MainWindow", "N Objetos"))
        self.label_Class2.setText(_translate("MainWindow", "TextLabel"))
        self.label_Class3.setText(_translate("MainWindow", "TextLabel"))
        self.label_Class1.setText(_translate("MainWindow", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Segmentacion"))
