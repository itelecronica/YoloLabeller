'''
Created on 26 abr. 2021

@author: Guille
@comment: Clase que gestiona la logica del programa
'''

from PyQt5.QtCore import pyqtSignal, QObject
import os 
import cv2
import numpy as np
import traceback


class MainController(QObject):
    
    newImageList = pyqtSignal(list)
    
    
    def __init__(self, configGeneral, appDir):
        QObject.__init__(self)
        self.configGeneral = configGeneral
        self.appDir = appDir
        
        
    def setConfigGeneral(self, configGeneral):
        self.configGeneral = configGeneral
        
        
    def initController(self):
        self.inputPath = self.appDir + self.configGeneral["inputDir"]
        self.outputPath = self.appDir + self.configGeneral["outputDir"]
        if not os.path.exists(self.outputPath):
            try:
                os.makedirs(self.outputPath)
            except:
                pass
        if not os.path.exists(self.inputPath):
            try:
                os.makedirs(self.inputPath)
            except:
                pass
        self.getImageList()
        
        
    def getImageList(self):
        self.imageList = []
        imageList = sorted(os.listdir(self.inputPath))
        for imagePath in imageList:
            self.imageList.append(self.inputPath + imagePath)
        self.newImageList.emit(self.imageList)
        return
        
        
    def exportFiles(self, imagePath, roiPath, image, rois):
        notation = self.generateYoloTxt(image, rois)
        f = open (roiPath,'w')
        f.write(notation)
        f.close()
        cv2.imwrite(imagePath, image)
        return
    

    def importRois_YoloTXT(self, image, roisPath):
        roisToImport = []
        try:
            file = open(roisPath, 'r')
            rois = file.readlines()
            file.close()
            dh, dw, _ = image.shape
            for roi in rois:
                n, x, y, w, h = map(float, roi.split(' '))
                l = int((x - w / 2) * dw)
                r = int((x + w / 2) * dw)
                t = int((y - h / 2) * dh)
                b = int((y + h / 2) * dh)
                if l < 0:
                    l = 0
                if r > dw - 1:
                    r = dw - 1
                if t < 0:
                    t = 0
                if b > dh - 1:
                    b = dh - 1
                roisToImport.append([l, t, r, b, self.configGeneral["classes"][int(n)]])
        except: roisToImport = []
        return roisToImport

    # Importar los txt en formato YOLO de segmentation referentes a una imagen
    def importRois_YoloTXTSegmentation(self, image, roisPath):
        roisToImport = []
        try:
            f = open(roisPath, 'r')
            rois = f.readlines()
            f.close()
            dh, dw, _ = image.shape
            #print (dh,dw)
            for roi in rois: # rois => nClase x1 y1 x2 y2 x3 y3 ..... xN yN 
                nClase = int(roi[0]) # Recogemos el primer campo de cada linea, que hace referencia a la clase de dicho contorno
                coords = roi[1:].split()
                coordenadas = []
                # convertir las coordenadas absolutas (formatYOLO) a coordenadas de la imagen. Los pares son los puntos 'x', impares 'y'
                for i in range(0,len(coords)):
                    if i%2==0:
                        coordenadas.append(float(coords[i])*dw)
                    else:
                        coordenadas.append(float(coords[i])*dh)
                
                polygon = np.array([[x,y] for x, y in zip(coordenadas[0::2], coordenadas[1::2])], dtype ='int32') # convert list of coordinates to numpy massive 
                roisToImport.append([nClase,polygon]) # lista de contornos, cada elemento es su clase y su contorno en np.array para poder dibujarlo
        except Exception as e: 
            print(e)
            print(traceback.format_exc())
            roisToImport = []
        return roisToImport

    def generateYoloTxt(self, image, rois):
        classList = self.configGeneral["classes"]
        notation = ""
        height, width, _ = image.shape
        i = 0
        for roi in rois: #roi => xmin, ymin, xmax, ymax, class
            nclase = classList.index(roi[4])
            dw = 1.0 / width
            dh = 1.0 / height 
            x = (roi[0] + roi[2]) / 2.0
            y = (roi[1] + roi[3]) / 2.0
            w = roi[2] - roi[0]
            h = roi[3] - roi[1]
            x = x*dw; y = y*dh; w = w*dw; h = h*dh 
            notation += str(nclase) + " " + str("{:.6f}".format(x)) + " " + str("{:.6f}".format(y)) + " " + str("{:.6f}".format(w)) + " " + str("{:.6f}".format(h))
            if i < (len(rois) - 1): notation += "\n"
            i += 1
        return notation
