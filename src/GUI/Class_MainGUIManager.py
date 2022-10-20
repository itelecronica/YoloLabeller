'''
Created on 26 abr. 2021

@author: Guille
@comment: Clase que gestiona la interfaz
'''


from PyQt5.QtCore import QTimer, pyqtSignal, Qt
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
import cv2, os, time#, threading
import numpy as np

from GUI.Class_Graphicscene import GraphicsScene
from UTIL.Class_KBD import KBD


class MainGUIManager(QMainWindow):

    imageBorder = 20
    exportConfigGeneralFile = pyqtSignal(object)
    indexOfList = 0
    

    def __init__(self, MainWindow, configGeneral, configGeneralPath, mainController, appDir):
        QMainWindow.__init__(self)
        self.ui = MainWindow()
        self.ui.setupUi(self)
        self.configGeneral = configGeneral
        self.configGeneralPath = configGeneralPath
        self.mainController = mainController
        self.appDir = appDir
        self.logoPath = self.appDir + "../cfg/source/logo.jpg"
        self.kbd = KBD()
        self.initGUIVariables()
        self.initGUISignals()
        self.loadGUITimer = QTimer()
        self.loadGUITimer.timeout.connect(self.loadGUI)
        self.loadGUITimer.start(300)
        
        
    def loadGUI(self):
        self.loadGUITimer.stop()
        self.loadLogo()
        for cls in self.configGeneral["classes"]:
            self.ui.listWidget_classes.addItem(cls)
        self.loadMask(self.widthFixedPellets, self.heightFixedPellets)
        self.checkSelectionMode(0)
        self.kbd.start()
        
        
    def initGUIVariables(self):
        #Inicializando la lista de ventanas graficas
        self.outputRoisPath = None
        
        #Formato de etiquetas
        self.outputCheckBoxList = [self.ui.checkBox_FormatYolotxt, self.ui.checkBox_FormatYoloxml]
        for outputFormat in self.outputCheckBoxList:
            if self.configGeneral["savedParameters"]["outputFormat"] == str(outputFormat.text()):
                outputFormat.setChecked(True)
                self.outputFormat = str(outputFormat.text())
                break 
            else:
                outputFormat.setChecked(False)
                
        #Punto de guardado de imagen en que nos encontramos
        self.indexOfList = self.configGeneral["savedParameters"]["savePoint"]
        
        #Escena principal que muestra la imagen a regionar
        #Bloquear el scrolling a traves de las flechas del teclado
        self.ui.listWidget_classes.setFocusPolicy(Qt.NoFocus)
        
        self.ui.graphicsView_visualizer.setFocusPolicy(Qt.NoFocus)
        self.mainScene = GraphicsScene(self.ui.graphicsView_visualizer, self.configGeneral)
        self.ui.graphicsView_visualizer.setScene(self.mainScene)
        
        #Modo de seleccion
        self.selectionMode = self.configGeneral["savedParameters"]["selectionMode"]
        self.mainScene.setSelectionMode(self.selectionMode)
        if self.selectionMode: self.ui.checkBox_mode_fixed.setChecked(True)
        else: self.ui.checkBox_mode_free.setChecked(True)
        
        #Mostrar o no los nombres de etiqueta
        self.ui.checkBox_showLabels.setChecked(self.configGeneral["showLabels"])
        
        #Mascara que muestra el tamanio de los pellets
        self.maskScene = QGraphicsScene(self.ui.graphicsView_pelletImg)
        self.ui.graphicsView_pelletImg.setScene(self.maskScene)
        
        #Ajuste de tamanio de pellets para el regionamiento prefijado
        self.widthFixedPellets = self.configGeneral["fixed_dims"]["ROI"][0]
        self.heightFixedPellets = self.configGeneral["fixed_dims"]["ROI"][1]
        self.ui.horizontalSlider_size_pellets.setFocusPolicy(Qt.NoFocus)
        self.ui.horizontalSlider_size_pellets.setMinimum(10)
        self.ui.horizontalSlider_size_pellets.setMaximum(100)
        self.ui.horizontalSlider_size_pellets.setSingleStep(5)
        self.ui.horizontalSlider_size_pellets.setValue(self.widthFixedPellets)
        self.onFixedSizeChanged()
        return
    
    
    def initGUISignals(self):
        self.ui.pushButton_addClass.clicked.connect(self.addNewClass)
        self.ui.pushButton_deleteClass.clicked.connect(self.deleteSelectedClass)
        
        self.ui.checkBox_showLabels.clicked.connect(lambda _: self.onShowLabelsChecked(0))
        
        self.ui.checkBox_mode_fixed.clicked.connect(lambda _: self.checkSelectionMode(0))
        self.ui.checkBox_mode_free.clicked.connect(lambda _: self.checkSelectionMode(0))
        
        self.ui.checkBox_FormatYolotxt.clicked.connect(self.checkOutputFormat)
        self.ui.checkBox_FormatYoloxml.clicked.connect(self.checkOutputFormat)
        
        self.ui.pushButton_nextImg.clicked.connect(lambda _: self.updateImageIndex(1))
        self.ui.pushButton_prevImg.clicked.connect(lambda _: self.updateImageIndex(-1))
        
        self.mainController.newImageList.connect(self.onNewImageList)
        self.ui.listWidget_classes.clicked.connect(self.onClassSelected)
        
        self.ui.horizontalSlider_size_pellets.valueChanged.connect(self.onFixedSizeChanged)
        
        self.ui.pushButton_discard.clicked.connect(self.mainScene.clearRois)
        self.ui.pushButton_save.clicked.connect(self.saveChanges)
        
        self.kbd.backImgSignal.connect(self.updateImageIndex)
        self.kbd.nextImgSignal.connect(self.updateImageIndex)
        self.kbd.saveSignal.connect(self.saveChanges)
        self.kbd.discardSignal.connect(self.mainScene.clearRois)
        self.kbd.classSelectedSignal.connect(self.onClassKeyPressed)
        self.kbd.showLabelSignal.connect(self.onShowLabelsChecked)
        self.kbd.changeSelectionMode.connect(self.checkSelectionMode)
        self.kbd.scapeSignal.connect(self.onCloseProgram)
        self.kbd.undoneSignal.connect(self.mainScene.undoneChanges)
        return
    
    
    def onNewImageList(self, imageList):
        self.imageList = imageList
        self.setSelectedImage()
        
        
    def onFixedSizeChanged(self):
        self.widthFixedPellets = int(self.ui.horizontalSlider_size_pellets.value())
        self.heightFixedPellets = self.widthFixedPellets
        self.configGeneral["fixed_dims"]["ROI"][0] = self.widthFixedPellets
        self.configGeneral["fixed_dims"]["ROI"][1] = self.heightFixedPellets
        self.mainScene.setFixedDims([self.widthFixedPellets, self.heightFixedPellets], self.configGeneral["fixed_dims"]["randomSize_percent"])
        self.ui.label_pixels.setText(str(self.widthFixedPellets) + " px")
        self.loadMask(self.widthFixedPellets, self.heightFixedPellets)
        
        
    def onShowLabelsChecked(self, mode):
        state = int(self.ui.checkBox_showLabels.isChecked())
        if mode:
            state = not state
            self.ui.checkBox_showLabels.setChecked(state)
        self.configGeneral["showLabels"] = state
        self.mainScene.setShowLabels(state)
        self.exportConfigGeneralFile.emit(self.configGeneral)
        
        
    def updateImageIndex(self, sum):
        if sum > 0 and (len(self.imageList) - 1 == self.indexOfList):
            self.indexOfList = 0
        elif sum < 0 and self.indexOfList == 0:
            self.indexOfList = len(self.imageList) - 1
        else:
            self.indexOfList += sum
        self.setSelectedImage()
        
        
    def setSelectedImage(self):
        if len(self.imageList) == 0: return
        try:
            self.selectedImagePath = self.imageList[self.indexOfList]
        except:
            self.indexOfList = 0
            self.selectedImagePath = self.imageList[self.indexOfList]
        #self.ui.label_selectedImage.setText("Image: " + str(self.indexOfList + 1) + " of " + str(len(self.imageList)))
        
        image = cv2.imread(self.selectedImagePath)
        imageName = self.selectedImagePath.split("/")
        imageName = imageName[len(imageName) - 1]
        extension = imageName.split(".")
        extension = "." + extension[len(extension) - 1]
        self.outputImagePath = (self.appDir + self.configGeneral["outputDir"] + imageName).replace(extension, ".png")
        self.outputRoisPath = self.outputImagePath.replace(".png", ".txt")
        self.ui.label_selectedImage.setText(f"Image: {self.indexOfList + 1} of {len(self.imageList)}:    {imageName}")

        rois = self.mainController.importRois_YoloTXT(image, self.outputRoisPath)
        self.mainScene.setSelectedImage(image, rois)
        return
        
        
    def addNewClass(self):
        newClass = str(self.ui.textEdit_newClass.toPlainText())
        err = ""
        if newClass == "":
            err += "No class name found"
        if newClass in self.configGeneral["classes"]:
            err += "Class already exists"
            self.ui.textEdit_newClass.clear()
        if err != "": 
            _ = QMessageBox.question(None, 'ERROR', err, buttons = QMessageBox.Ok)
            return            
        self.configGeneral["classes"].append(newClass)
        self.ui.listWidget_classes.addItem(newClass)
        self.exportConfigGeneralFile.emit(self.configGeneral)
        self.ui.textEdit_newClass.clear()
        return
    
    
    def onClassKeyPressed(self, key):
        try:
            self.ui.listWidget_classes.setCurrentRow(key)
            self.onClassSelected()
        except: return
    
    
    def onClassSelected(self):
        classSelected = str(self.ui.listWidget_classes.currentItem().text())
        self.mainScene.setSelectedClass(classSelected)
        return 
    
    
    def deleteSelectedClass(self):
        try:
            classToDelete = str(self.ui.listWidget_classes.currentItem().text())
            '''if classToDelete == "pellets": 
                _ = QMessageBox.question(None, 'ERROR', "Operation denied", buttons = QMessageBox.Ok)
                return'''
            indexToDelete = self.configGeneral["classes"].index(classToDelete)
            self.configGeneral["classes"].pop(indexToDelete)
            self.exportConfigGeneralFile.emit(self.configGeneral)
            self.ui.listWidget_classes.clear()
            for cls in self.configGeneral["classes"]:
                self.ui.listWidget_classes.addItem(cls)
            self.mainScene.setSelectedClass(None)
        except:
            _ = QMessageBox.question(None, 'ERROR', "Must select a class to erase", buttons = QMessageBox.Ok)
        return
    
    
    def checkSelectionMode(self, mode):
        if mode:
            state = int(self.ui.checkBox_mode_fixed.isChecked())
            self.ui.checkBox_mode_fixed.setChecked(not state)
            self.ui.checkBox_mode_free.setChecked(state)
        if self.ui.checkBox_mode_fixed.isChecked():
            selectionMode = 1
        else: selectionMode = 0
        if selectionMode != self.selectionMode:
            self.selectionMode = selectionMode 
            self.configGeneral["savedParameters"]["selectionMode"] = selectionMode
            self.exportConfigGeneralFile.emit(self.configGeneral)
        self.mainScene.setSelectionMode(self.selectionMode)
        return 
    
    
    def checkOutputFormat(self):
        for outputFormat in self.outputCheckBoxList:
            if outputFormat.isChecked():
                self.configGeneral["savedParameters"]["outputFormat"] = str(outputFormat.text())
                self.outputFormat = str(outputFormat.text())
                self.exportConfigGeneralFile.emit(self.configGeneral)
                break
        return 
    
    
    def loadMask(self, width, height):
        maskWidth = self.ui.graphicsView_pelletImg.width() - self.imageBorder
        maskHeight = self.ui.graphicsView_pelletImg.height() - self.imageBorder
        mask = np.full((maskHeight, maskWidth), 0, dtype=np.uint8)  # mask is only 
        #cv2.ellipse(mask, (maskWidth/2, maskHeight/2),(width, height), 0, 0, 360, 255,-1)
        #cv2.circle(mask, (int(maskWidth/2), int(maskHeight/2)), int(width/2), 255, -1)
        cv2.rectangle(mask, (int(maskWidth/2) - int(width/2), int(maskHeight/2) -  int(height/2)), (int(maskWidth/2) + int(width/2), int(maskHeight/2) +  int(height/2)), 255, -1)
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
        height, width, channels = mask.shape
        bytesPerLine = channels * width
        frame = QImage(mask.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.maskScene.clear()
        self.maskScene.addPixmap(QPixmap.fromImage(frame))
        self.maskScene.update()
        return
        
        
    def loadLogo(self):
        logo = cv2.imread(self.logoPath)
        logoScene = QGraphicsScene(self.ui.graphicsView_logo)
        self.ui.graphicsView_logo.setScene(logoScene)
        
        logoWidth, logoHeight, _ = logo.shape
        viewWidth = self.ui.graphicsView_logo.width()
        viewHeight = self.ui.graphicsView_logo.height()
        propLogo = (float(logoWidth) / float(logoHeight))
        propView = (float(viewWidth) / float(viewHeight))
        
        if propLogo > propView:
            selectedWidth = viewWidth
            selectedHeight = int(selectedWidth * propLogo)
        else:
            selectedHeight = viewHeight
            selectedWidth = int(selectedHeight * (1 / propLogo))
        selectedWidth, selectedHeight = selectedWidth - self.imageBorder, selectedHeight - self.imageBorder
        
        resized_logo = cv2.resize(logo, (selectedWidth, selectedHeight))
        resized_logo = cv2.cvtColor(resized_logo, cv2.COLOR_BGR2RGB)
        height, width, channels = resized_logo.shape
        bytesPerLine = channels * width
        frame = QImage(resized_logo.data, width, height, bytesPerLine, QImage.Format_RGB888)
        logoScene.clear()
        logoScene.addPixmap(QPixmap.fromImage(frame))
        logoScene.update()
        return
    
    
    def saveChanges(self):
        try:
            image = self.mainScene.getImage()
            rois = self.mainScene.getRois()
            self.mainController.exportFiles(self.outputImagePath, self.outputRoisPath, image, rois)
        except: return
    
    
    def closeEvent (self, event):
        self.onCloseProgram()
        event.ignore()
        return
    
    
    def onCloseProgram(self):
        msg = "Crear punto de guardado?"
        reply = QMessageBox.question(None, 'Warning', msg, buttons = QMessageBox.No|QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.configGeneral["savedParameters"]["savePoint"] = self.indexOfList
        elif reply == QMessageBox.No:
            self.configGeneral["savedParameters"]["savePoint"] = 0
        else: return
        self.exportConfigGeneralFile.emit(self.configGeneral)
        os.system("pkill -f MainApplication")