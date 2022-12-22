import os, cv2
import numpy as np

from GUI.DatasetConversorGUI import Ui_DatasetConverter
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox


class Conversor:

    def __init__(self):
        return

    def polygon_to_mask(self, path, width, height, file):
        pathMask =path + "/../masks/" + file.replace("txt", "png")
        coords = self.importTxtYolo(path + "/"+ file, height, width)
        mask = np.zeros((height,width))
        if len(coords) != 0:
            for roi in coords:
                mask = cv2.fillPoly(mask,[roi],(255,2555,255))
        cv2.imwrite(pathMask,mask)

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
        x = float(x) + float(width)/2.0
        y = float(y) + float(height)/2.0
        x1, x2 = float(x)/float(w), float(width)/float(w)
        y1, y2 = float(y)/float(h), float(height)/float(h)
        f2.write(str(x1) + " " + str(y1) + " " + str(x2)+ " " + str(y2) + "\n")
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




class DatasetConverter(QDialog, Ui_DatasetConverter):
    
    def __init__(self):
        super(DatasetConverter,self).__init__()

        self.setupUi(self)
        self.conversor = Conversor()
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
        self.groupBox_4.setVisible(False)

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

    def startConversion(self,formatConversion):
        self.createOutputFolders(formatConversion)
        i = 1
        for file in self.filesToConvert:
            if self.formatToConvert == "png":
                self.conversor.mask_to_polygon(self.pathToConvert,file,formatConversion)
            else:
                height = int(self.lineEdit_Height.text())
                width = int(self.lineEdit_Width.text())
                self.conversor.polygon_to_mask(self.pathToConvert,height,width, file)
            i += 1
            self.updateProgressBar(i)


    def defineInputExtension(self, n):
        if self.checkBoxInputs[n].isChecked():
            for checkBox in self.checkBoxInputs:
                if self.checkBoxInputs.index(checkBox) != n:
                    checkBox.setEnabled(False)
            for checkBox in self.checkBoxOutputs:
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

    def checkFolder(self):
        self.filesToConvert = []
        if self.pathToConvert != None:
            for file in os.listdir(self.pathToConvert):
                if file.split(".")[1] == self.formatToConvert:
                    self.filesToConvert.append(file)
        self.label_filesCount.setText(f"Detectados {len(self.filesToConvert)} archivos")


    def openFolderDialog(self):
        dialogoSeleccionFolder = QFileDialog()
        dialogoSeleccionFolder.setOption(QFileDialog.DontUseNativeDialog,True)
        dialogoSeleccionFolder.setOption(QFileDialog.ReadOnly, True)
        dialogoSeleccionFolder.setFileMode(QFileDialog.DirectoryOnly)
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
            self.groupBox_4.setVisible(True)
        else: self.groupBox_4.setVisible(False)


    def exportaDatos(self):
        self.show()