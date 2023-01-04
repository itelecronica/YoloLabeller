'''
Created on 26 abr. 2021

@author: Guille
@comment: Clase que gestiona la interfaz
'''


from PyQt5.QtCore import QTimer, pyqtSignal, Qt
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QMessageBox
from PyQt5.QtGui import QImage, QPixmap, QTransform
import cv2, os, time#, threading
import numpy as np

from GUI.Class_Graphicscene import GraphicsScene
from UTIL.Class_KBD import KBD
#from GUI.Class_Painter import PainterMask
from LOGIC.Class_Conversor import ConversorMasks
from GUI.Class_ConvertDataset import DatasetConverter

class MainGUIManager(QMainWindow):

    imageBorder = 20
    exportConfigGeneralFile = pyqtSignal(object)
    indexOfList = 0
    modeApp = "detection"
    zoom = 1

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
        self.conversorMask = ConversorMasks()
        self.conversorDataset = DatasetConverter()
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
            self.ui.listWidget_clasesSegmentation.addItem(cls)
            self.ui.comboBox_Class.addItem(cls)
        self.ui.tabWidget.setCurrentIndex(0)
        self.loadMask(self.widthFixedPellets, self.heightFixedPellets)
        self.checkSelectionMode(0)
        self.kbd.start()
        
        
    def initGUIVariables(self):
        #Inicializando la lista de ventanas graficas
        self.outputRoisPath = None
        self.maskPath = None
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
        #self.paint = PainterMask()
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
        #self.mainScene.zoomEvent.connect(self.zoomAux)
        #self.ui.checkBox_showContorno.setAutoExclusive(False)
        #self.ui.checkBox_showMascara.setAutoExclusive(False)
        self.ui.checkBox_showMascara.setChecked(False)
        self.ui.checkBox_showContorno.setChecked(True)
        #self.ui.checkBox_showContorno.setAutoExclusive(True)
        #self.ui.checkBox_showMascara.setAutoExclusive(True)
        self.ui.pushButton_ImportDataset.clicked.connect(self.openConversor)

        return
    
    def openConversor(self):
        self.conversorDataset.exportaDatos()
    
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
        self.ui.tabWidget.currentChanged.connect(self.onModeChange)
        self.ui.checkBox_onlyOneClass.clicked.connect(self.OnshowOnly1Class)
        self.ui.comboBox_Class.currentIndexChanged.connect(self.getLabelOneClass)


        self.ui.checkBox_EnablePaint.clicked.connect(self.openPaint)
        self.ui.pushButton_Dibujar.clicked.connect(self.enablePaint)
        self.ui.pushButton_Borrar.clicked.connect(self.enableErase)
        self.ui.checkBox_showMascara.clicked.connect(lambda _: self.changeSegmentationView("mask"))
        self.ui.checkBox_showContorno.clicked.connect(lambda _: self.changeSegmentationView("contour"))
        self.ui.horizontalSlider.valueChanged.connect(lambda _: self.mainScene.updateSizePixel(self.ui.horizontalSlider.value()))
        self.ui.pushButton_ExportContornos.clicked.connect(self.exportMascaras)
        return

    # Cuando se modifica o define una mascara, al pulsar sobre el boton "Exportar", aqui se almacena y se transforma en listado de contornos YOLO
    def exportMascaras(self):
        mask = self.exportMask()
        if os.path.exists(self.configGeneral["outputDir_Mask"]):
            if os.path.isfile(self.maskPath):
                reply = QMessageBox.question(None, 'WARNING', "Se sobreescribira la mascara existente, continuar?", buttons = QMessageBox.No|QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    cv2.imwrite(self.maskPath, mask)
                    self.conversorMask.mask_to_polygon(mask,self.outputRoisPath)
                else:
                    pass
            else:
                cv2.imwrite(self.maskPath, mask)
                _ = QMessageBox.question(None, '', "Mascara almacenada correctamente", buttons = QMessageBox.Ok) 
                self.conversorMask.mask_to_polygon(mask,self.outputRoisPath)
            #self.setSelectedImage()
        else:
            try:
                os.makedirs(self.configGeneral["outputDir_Mask"])
                cv2.imwrite(self.maskPath, mask)
                _ = QMessageBox.question(None, '', "Mascara almacenada correctamente", buttons = QMessageBox.Ok) 
                
            except:
                pass
        #self.mainScene.paintEnable = False
        self.ui.checkBox_EnablePaint.setChecked(False)
        self.openPaint()
        self.setSelectedImage()

    # Cambiar la manera de visualizacion de los dataset de segmentacion (Mascara superpuesta/Contornos de la mascara)
    def changeSegmentationView(self, mode):
        if mode == "mask":
            self.ui.checkBox_showContorno.setChecked(False)
            self.ui.checkBox_showMascara.setChecked(True)
            self.mainScene.showContours = False
            
        else:
            self.ui.checkBox_showContorno.setChecked(True)
            self.ui.checkBox_showMascara.setChecked(False)
            self.mainScene.showContours = True
        self.mainScene.renderScene()

    # Habilitar el borrado de zonas definidas en la mascara
    def enableErase(self):
        if self.mainScene.isDelete == False:
            self.mainScene.isDelete = True
            self.ui.pushButton_Borrar.setStyleSheet("background-color: yellow")
        else:
            self.mainScene.isDelete = False
            self.ui.pushButton_Borrar.setStyleSheet("background-color: ")
        self.mainScene.isPaint = False
        self.ui.pushButton_Dibujar.setStyleSheet("background-color: ")

    # Habilitar la funcion de pintado sobre la mascara
    def enablePaint(self):
        if self.mainScene.isPaint == False:
            self.mainScene.isPaint = True
            self.ui.pushButton_Dibujar.setStyleSheet("background-color: yellow")
        else:
            self.mainScene.isPaint = False
            self.ui.pushButton_Dibujar.setStyleSheet("")
        self.mainScene.isDelete = False
        self.ui.pushButton_Borrar.setStyleSheet("background-color: ")
        
    # Habilitar las caracteristicas para definir mascaras en segmentacion
    def openPaint(self):
        #self.paint.initPaint()
        if self.ui.checkBox_EnablePaint.isChecked():
            self.mainScene.paintEnable = True
            self.mainScene.paintImage()
            self.ui.pushButton_Dibujar.setEnabled(True)
            self.ui.pushButton_Borrar.setEnabled(True)
            self.ui.horizontalSlider.setEnabled(True)
            self.ui.pushButton_ExportContornos.setEnabled(True)
            self.mainScene.isPaint = False
            self.mainScene.isDelete = False
        else:
            self.mainScene.paintEnable = False
            self.mainScene.renderScene()
            self.ui.pushButton_Dibujar.setEnabled(False)
            self.ui.pushButton_Borrar.setEnabled(False)
            self.ui.horizontalSlider.setEnabled(False)
            self.ui.pushButton_ExportContornos.setEnabled(False)
            self.ui.pushButton_Borrar.setStyleSheet("background-color: ")
            self.ui.pushButton_Dibujar.setStyleSheet("background-color: ")
            self.mainScene.isPaint = False
            self.mainScene.isDelete = False

    # Funcion que detecta el cambio de pestanha en el tabulador y actualiza la imagen en funcion de si se esta en Deteccion o Segmentacion
    def onModeChange(self):
        modes = ["detection","segmentation"]
        self.modeApp = modes[self.ui.tabWidget.currentIndex()]
        if self.modeApp == "detection":
            self.ui.checkBox_onlyOneClass.setChecked(False)
        self.setSelectedImage()
        
    
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
        self.ui.checkBox_onlyOneClass.setChecked(False)
        self.ui.comboBox_Class.setEnabled(False)
        self.ui.comboBox_Class.setCurrentIndex(0)
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
        # se ha anhadido las dos opciones de YOLO, haciendo diferencia para recoger labels y mascaras
        if self.modeApp == "detection":
            self.outputImagePath = (self.appDir + self.configGeneral["outputDir"] + imageName).replace(extension, ".png")
            self.outputRoisPath = self.outputImagePath.replace(".png", ".txt")
            rois = self.mainController.importRois_YoloTXT(image, self.outputRoisPath)
        else:
            self.outputImagePath = (self.appDir + self.configGeneral["outputDir_Segmentation"] + imageName).replace(extension, ".png")
            self.outputRoisPath = self.outputImagePath.replace(".png", ".txt")
            self.maskPath = (self.appDir + self.configGeneral["outputDir_Mask"] + imageName).replace(extension, ".png")
            self.ui.checkBox_EnablePaint.setChecked(False)
            self.openPaint()
            try:
                #print(self.maskPath)
                if os.path.isfile(self.maskPath):
                    self.mainScene.mask = cv2.imread(self.maskPath)
                else:
                    self.mainScene.mask = np.zeros_like(image)

                self.mainScene.isMask = True
            except:
                print("no existe mascara")
                self.mainScene.isMask = False
                self.mainScene.mask = np.zeros_like(image)
            roisTxt = self.mainController.importRois_YoloTXTSegmentation(image, self.outputRoisPath) # Importar las labels de contornos de YOLO
            rois = []
            # en caso de que se seleccione mostrar una unica clase, aqui se filtran unicamente los contornos de la clase a mostrar
            if self.ui.checkBox_onlyOneClass.isChecked():
                for roi in roisTxt:
                    if roi[0]== self.labelOneClass:
                        rois.append(roi)
            else: rois = roisTxt
            self.showCountSegmentation(rois) # mostrar por interfaz los contadores de clases en cada imagen
        self.ui.label_selectedImage.setText(f"Image: {self.indexOfList + 1} of {len(self.imageList)}:    {imageName}")
        self.resetZoom()
        self.mainScene.setSelectedImage(image, rois, self.modeApp)
        return

    # en segmentacion, mostrar una unica clase en imagen, ocultando el resto de clases presentes 
    def OnshowOnly1Class(self):
        if self.ui.checkBox_onlyOneClass.isChecked():
            self.ui.comboBox_Class.setEnabled(True)
        else:
            self.ui.comboBox_Class.setEnabled(False)
            self.ui.comboBox_Class.setCurrentIndex(0)
            self.setSelectedImage()
        return

    # Definir la clase que se quiere mostrar
    def getLabelOneClass(self): 
        if self.ui.checkBox_onlyOneClass.isChecked():
            clase = str(self.ui.comboBox_Class.currentText()) # Recoger de la interfaz la clase seleccionada
            if clase in self.configGeneral["classes"]:
                self.labelOneClass = self.configGeneral["classes"].index(clase)
                self.setSelectedImage()
            else:
                _ = QMessageBox.question(None, 'ERROR', "Es necesario seleccionar una clase a mostrar", buttons = QMessageBox.Ok)
        else: pass
        return
    
    # mostrar los contadores de elementos por clase
    def showCountSegmentation(self, rois):

        count_classes = [0]*len(self.configGeneral["classes"])
        if len(rois)!=0:
            for roi in rois:
                count_classes[roi[0]]+=1
        else:
            pass
        labels = [self.ui.label_Class1, self.ui.label_Class2, self.ui.label_Class3]
        contadores = [self.ui.lineEdit_Class1,self.ui.lineEdit_Class2,self.ui.lineEdit_Class3]
        for i in range(len(labels)):
            labels[i].setText(self.configGeneral["classes"][i])
            contadores[i].clear()
            contadores[i].setText(str(count_classes[i]))

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

    '''def zoomAux(self, type):
        if type == -1:
            self.zoomOut()
        else:
            self.zoomIn()

    def zoomIn(self):
        self.zoom *= 1.05
        self.updateView()
        
    def zoomOut(self):
        self.zoom /= 1.05
        self.updateView()

    def updateView(self):

        self.ui.graphicsView_visualizer.setTransform(QTransform().scale(self.zoom, self.zoom))
        self.ui.graphicsView_visualizer.setScene(self.mainScene)
        self.mainScene.update()'''        

    def resetZoom (self):
        self.mainScene._zoom=1
        self.mainScene.updateView()

    # Convertir la mascara definida a binaria
    def exportMask(self):
       
        mask = cv2.cvtColor(self.mainScene.mask, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(mask, 50,255,0)
        return mask
    
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