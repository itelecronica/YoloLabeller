'''
Created on 20 dec. 2022

@author: Pablo
@comment: Conversor de Datasets de segmentacion (mascaras o contornos) a otros formatos de segmentacion, y tambien, a deteccion de objetos
'''

import os, cv2
from xmlrpc.server import resolve_dotted_attribute
import numpy as np

from GUI.DatasetConversorGUI import Ui_DatasetConverter
from GUI.MaksConfiguratorGUI import Ui_MasksConfigurator
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox


class Conversor:
    def __init__(self):
        return

    # Conversion del txt Segmentation YOLO en formato U-Net, mascaras, adaptado al tamanho deseado de la mascara definido por interfaz
    def polygon_to_mask(self, path, width, height, file):
        pathMask =path + "/../masks/" + file.replace("txt", "png")
        coords = self.importTxtYolo(path + "/"+ file, height, width)
        mask = np.zeros((height,width))
        if len(coords) != 0:
            for roi in coords:
                mask = cv2.fillPoly(mask,[roi],(255,2555,255))
        cv2.imwrite(pathMask,mask)


     # funcion encargada de convertir la mascara en contornos y escribe el txt formato YOLO para segmentacion 
    def mask_to_polygon(self, pathToMask, nameMask, conversionsType):
        mask = cv2.imread(pathToMask + "/" + nameMask,0)
        self.newFile = True
        h,w = mask.shape
        contours ,_= cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        kernel = np.ones((3,3), np.uint8)
        mask = cv2.erode(mask, kernel)
        i = 0
        if len(contours)==0:
            if "yolo" in conversionsType:
                name = pathToMask + "/../labelsSegmentation/" + nameMask
                self.generateWhiteTxt(name)
            if "bounding" in conversionsType:
                name = pathToMask + "/../labelsBounding/" + nameMask
                self.generateWhiteTxt(name)

        for object in contours:
            x, y, width, height = cv2.boundingRect(object)
            is_pellet = False
            coords = []
            #polygon = []
            nclase = 5
            for point in object:
                coords.append(int(point[0][0]))
                coords.append(int(point[0][1]))
            
            area = cv2.contourArea(object)
            if area > 330 and area < 7000 :
                nclase = 0
                limit = 80.0
            elif area >= 7000:
                nclase = 0
                limit = 80.0
            else:
                nclase = 0
                limit = 38.0
          
            mask_cut = np.zeros_like(mask)
            cv2.drawContours(mask_cut,[object],0,255,-1)
            img_mask = mask_cut[y:y+height, x: x+width]
            #is_pellet = self.checkBlack(img_mask,height,width, limit)
            is_pellet = True
            if is_pellet:
                if nclase != 5:
                    if "yolo" in conversionsType:
                        name = pathToMask + "/../labelsSegmentation/" + nameMask
                        self.generateTxtFileYOLO(coords,name,h,w, nclase)
                    if "bounding" in conversionsType:
                        name = pathToMask + "/../labelsBounding/" + nameMask
                        self.generateTxtFileBounding(name, nclase, x, y, width, height, h, w)
            self.newFile = False
        return 

    # generacion de txt en formato Segmentation YOLO
    def generateTxtFileYOLO(self, points, nameImg, h, w, nClase):
        
        path_txt = nameImg.replace("png","txt")
        #path_txt =  nameImg
        if os.path.isfile(path_txt):
            try:
                if self.newFile:
                    f = open(path_txt, "w")
                else:
                    f = open(path_txt, "a")
            except:
                print("Error abriendo txt")
        else:
            try: 
                if self.newFile:
                    f = open(path_txt, "w")
                else:
                    f = open(path_txt, "a")
            except:
                print("Error abriendo txt")

        f.write(str(nClase) + " ")
        for i in range(len(points)):
            if i%2 == 0:
                point_absolute = float(points[i])/float(w)
            else:
                point_absolute = float(points[i])/float(h)
            f.write(str(point_absolute) + " ")
        f.write("\n")
        f.close()

    # generacion de txt en formato Object Detection YOLO
    def generateTxtFileBounding(self,nameImg, nClase, x, y, width, height, h, w):

        path_txt2 = nameImg.replace("png", "txt")
        if os.path.isfile(path_txt2):
            try: 
                if self.newFile:
                    f2 = open(path_txt2, "w")
                else:
                    f2 = open(path_txt2, "a")
            except:
                print("Error abriendo txt")
        else:
            try: 
                f2 = open(path_txt2, "w")
            except:
                print("Error abriendo txt")

        f2.write(str(nClase) + " ")
        # hallar el centro de la bounding box
        x = float(x) + float(width)/2.0
        y = float(y) + float(height)/2.0
        # conversion de centro y dimensiones a coordenadas absolutas [0-1]
        x1, x2 = float(x)/float(w), float(width)/float(w)
        y1, y2 = float(y)/float(h), float(height)/float(h)
        f2.write(str(x1) + " " + str(y1) + " " + str(x2)+ " " + str(y2) + "\n") # escribir formato: nClase centroX centroY ancho alto
        f2.close()

    def generateWhiteTxt(self, nameImg):
        #nameImg = nameImg.replace("png","txt")
        path_txt = nameImg.replace("png","txt")
        if os.path.isfile(path_txt):
            try: 
                f = open(path_txt, "w")
            except:
                print("Error abriendo txt")
        else:
            try: 
                f = open(path_txt, "w")
            except:
                print("Error abriendo txt")
        f.write(" ")
        f.close()

    # leer el txt Segmentation YOLO, y convertir los puntos absolutos a relativos del tamanho de mascara definido en interfaz
    def importTxtYolo(self, path, h, w):
        roisToImport = []
        f = open(path,'r')
        rois = f.readlines()
        f.close()
        if rois != [' ']:
            for roi in rois:
                coords = roi[1:].split()
                coordenadas = []
                for i in range(0,len(coords)):
                    if i%2 == 0:
                        coordenadas.append(float(coords[i])*w)
                    else:
                        coordenadas.append(float(coords[i])*h)
                polygon = np.array([[x,y] for x, y in zip(coordenadas[0::2], coordenadas[1::2])], dtype ='int32')
                roisToImport.append(polygon)
        return roisToImport

class ConfiguratorMasks(QDialog, Ui_MasksConfigurator):

    def __init__(self):
        super(ConfiguratorMasks,self).__init__()
        self.setupUi(self)
        self.pushButton_ExportParameters.clicked.connect(self.completeDictionary)
        self.dictParameters = {"Dimensions":{"Width":"-----","Height":"--------"},
                                "Colours":{"type":"----","colours":"[-----]"},
                                "Area":{"0":"[----]"}}
        self.success = False
        return 

    def completeDictionary(self):
        if self.lineEdit_maskWidth.text() != "" or self.lineEdit_maskHeight.text() != "":
            self.dictParameters["Dimensions"]["Width"] = int(self.lineEdit_maskWidth.text())
            self.dictParameters["Dimensions"]["Height"] = int(self.lineEdit_maskHeight.text()) 
            self.success = True
            self.accept()
        else:
            _ = QMessageBox.question(None, 'ERROR', "Es necesario definir dimensiones de salida de la mascara.", buttons = QMessageBox.Ok)

    def exportParameters(self):
        self.show()
        
        if self.exec_() == QDialog.Accepted:
            self.completeDictionary()
            if self.success:
                self.success = False
                return self.dictParameters
            else:
                return None
        else:
            return None
            
        


class DatasetConverter(QDialog, Ui_DatasetConverter):
    
    def __init__(self):
        super(DatasetConverter,self).__init__()

        self.setupUi(self)
        self.conversor = Conversor()
        self.configuratorMasks = ConfiguratorMasks()
        self.pathToConvert = None
        self.formatsEnables = ["png", "txt"]
        self.formatToConvert = None
        self.checkBoxInputs = [self.checkBox_InputUnet, self.checkBox_InputYolo]
        self.checkBoxOutputs = [self.checkBox_outputUnet, self.checkBox_outputYolo, self.checkBox_outputBounding]
        self.outputFormats = ["unet","yolo","bounding"]
        self.pushButton_Navegador.clicked.connect(self.openFolderDialog)
        
        self.checkBox_InputUnet.clicked.connect(lambda _:self.defineInputExtension(0))
        self.checkBox_InputYolo.clicked.connect(lambda  _:self.defineInputExtension(1))

        self.checkBox_outputUnet.clicked.connect(self.showDimensionsMask)

        self.pushButton_Generar.clicked.connect(self.defineConversion)
        self.pushButton_ConfigMask.clicked.connect(self.defineParametersMask)
        self.pushButton_ConfigMask.setVisible(False)

    # chequea que se haya definido minimo un formato de salida para la conversion del dataset 
    def defineConversion(self):
        formatConversion = []
        for checkbox in self.checkBoxOutputs:
            if checkbox.isChecked():
                formatConversion.append(self.outputFormats[self.checkBoxOutputs.index(checkbox)])
        if formatConversion ==[]:
            _ = QMessageBox.question(None, 'ERROR', "Es necesario seleccionar al menos una salida.", buttons = QMessageBox.Ok)
            return
        else:
            print(formatConversion)
        self.startConversion(formatConversion)

    # en funcion de los formatos de entrada y salida definidos, realiza la conversion del dataset
    def startConversion(self,formatConversion):
        self.createOutputFolders(formatConversion)
        i = 1
        for file in self.filesToConvert:
            if self.formatToConvert == "png":
                self.conversor.mask_to_polygon(self.pathToConvert,file,formatConversion)
            else:
                '''height = int(self.lineEdit_Height.text())
                width = int(self.lineEdit_Width.text())'''
                height = int(self.parametersMaskDict["Dimensions"]["Height"])
                width = int(self.parametersMaskDict["Dimensions"]["Width"])
                self.conversor.polygon_to_mask(self.pathToConvert,width,height, file)
            i += 1
            self.updateProgressBar(i)

    # recoger de la interfaz formato de entrada, y activar navegador de archivos para definir ruta del dataset
    def defineInputExtension(self, n):
        if self.checkBoxInputs[n].isChecked():
            for checkBox in self.checkBoxInputs: # una vez definido formato de entrada, anula los otros formatos presentes
                if self.checkBoxInputs.index(checkBox) != n:
                    checkBox.setEnabled(False)
            for checkBox in self.checkBoxOutputs: # anula el formato de salida que es igual al formato de entrada
                if self.checkBoxOutputs.index(checkBox) == n:
                    checkBox.setEnabled(False)
            self.formatToConvert = self.formatsEnables[n]
            self.pushButton_Navegador.setEnabled(True)
        else:
            for checkBox in self.checkBoxInputs:
                checkBox.setEnabled(True)
            for checkBox in self.checkBoxOutputs:
                checkBox.setEnabled(True)
            self.pushButton_Navegador.setEnabled(False)
            self.formatToConvert = None
        print(self.formatToConvert)

    # comprobar el directorio de entrada y contabilizar los archivos compatibles con el formato de entrada definidos
    def checkFolder(self):
        self.filesToConvert = []
        if self.pathToConvert != None:
            for file in os.listdir(self.pathToConvert):
                if file.split(".")[1] == self.formatToConvert:
                    self.filesToConvert.append(file)
        self.label_filesCount.setText(f"Detectados {len(self.filesToConvert)} archivos") # mostrar numero de archivos disponibles en directorio

    # ejecutar navegador de archivos para definir ruta del dataset
    def openFolderDialog(self):
        dialogoSeleccionFolder = QFileDialog()
        dialogoSeleccionFolder.setOption(QFileDialog.DontUseNativeDialog,True)
        dialogoSeleccionFolder.setOption(QFileDialog.ReadOnly, True)
        dialogoSeleccionFolder.setFileMode(QFileDialog.DirectoryOnly) # Set para configurar solo directorios como seleccionables
        #dialogoSeleccionFolder.setNameFilter("Images (*.jpeg)");
        #dialogoSeleccionFolder.setDirectory(self.imagesFolder)
        self.pathToConvert = dialogoSeleccionFolder.getExistingDirectory(self, "Select Directory")
        '''done = dialogoSeleccionFolder.exec_()
        print (done)
        if done:
            folderPath = dialogoSeleccionFolder.getExistingDirectory(None, "Select Directory")'''
        self.label_folderSelect.clear()
        self.label_folderSelect.setText(self.pathToConvert)
        if self.pathToConvert != '':
            self.checkFolder()

    def createOutputFolders(self, formatos):
        for format in formatos:
            if format == "yolo":
                path = self.pathToConvert + "/../labelsSegmentation/"
            elif format == "bounding":
                path = self.pathToConvert + "/../labelsBounding/"
            else:
                path = self.pathToConvert + "/../masks/"
            try:
                os.makedirs(path)
            except:
                print("No se puede crear el directorio")

    def updateProgressBar(self, n):
        porcentaje = int(100.0*n/len(self.filesToConvert))
        print(porcentaje)
        self.progressBar.setValue(porcentaje)

    def showDimensionsMask(self):
        if self.checkBox_outputUnet.isChecked():
            self.pushButton_ConfigMask.setVisible(True)
            self.pushButton_ConfigMask.setEnabled(True)

        else: 
            self.pushButton_ConfigMask.setVisible(False)
            self.pushButton_ConfigMask.setEnabled(False)
        
    def defineParametersMask(self):
        parametersMask = self.configuratorMasks.exportParameters()
        if parametersMask is not None:
            self.parametersMaskDict = parametersMask
        return

    def exportaDatos(self):
        self.show()