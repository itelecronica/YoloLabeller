'''
Created on 14 jun. 2021

@author: Guille
@comment: Clase de escena grafica que gestiona los eventos sobre las imagenes
'''


from PyQt5 import QtCore
from PyQt5.QtWidgets import QGraphicsScene, QAction, QMenu
from PyQt5.QtGui import QImage, QPixmap, QCursor
import cv2
from scipy.spatial import Delaunay
from random import randint


#Clase hija de la ventana grafica QGraphicsScene
class GraphicsScene(QGraphicsScene):
    
    initialPosition = QtCore.QPointF(0,0)
    finalPosition = QtCore.QPointF(0,0)
    roiColor, selectionColor = (255,0,0), (0,255,0)
    mouseEnabled, isClassSelected, showLabels = False, False, False
    selectedRoi, selectedClass, lastChange, rois = None, None, None, []
    
    
    def __init__ (self, parent, configGeneral):
        super(GraphicsScene, self).__init__ (parent)
        self.menu = QMenu()
        removeAction = QAction('Eliminar', self)
        removeAction.triggered.connect(lambda: self.removeRoi())
        self.menu.addAction(removeAction)
        
        self.configGeneral = configGeneral
        fixedDims = self.configGeneral["fixed_dims"]["ROI"]
        randomSize = self.configGeneral["fixed_dims"]["randomSize_percent"]
        self.setFixedDims(fixedDims, randomSize)
        self.showLabels = self.configGeneral["showLabels"]
        
        
    def clearRois(self):
        self.rois = []
        try: self.renderScene()
        except: pass 
        
        
    def getImage(self):
        return self.image
    
    
    def getRois(self):
        return self.rois 
    
    
    def undoneChanges(self):
        if self.lastChange is None: return
        if isinstance(self.lastChange, int):
            self.rois.pop(self.lastChange)
        if isinstance(self.lastChange, list):
            self.rois.append(self.lastChange)
        self.lastChange = None
        self.renderScene()
        
        
    def setSelectedImage(self, selectedImage, rois):
        self.image = selectedImage
        self.rois = rois
        self.mouseEnabled = True
        self.renderScene()
        
        
    def setLastChange(self, lastChange):
        self.lastChange = lastChange
        
        
    def setShowLabels(self, state):
        self.showLabels = state
        try: self.renderScene()
        except: pass
        
        
    def setSelectionMode(self, selectionMode): #0 modo libre, 1 modo prefijado
        self.selectionMode = selectionMode
    
    
    def setSelectedClass(self, selectedClass):
        self.selectedClass = selectedClass
        if self.selectedClass is not None:
            self.isClassSelected = True
        else:
            self.isClassSelected = False
            
            
    def setFixedDims(self, fixedDims, randomSize):
        self.fixedDims = fixedDims
        self.randomSize = randomSize
        self.randomRangeX = [int(self.fixedDims[0] - self.fixedDims[0] * self.randomSize), int(self.fixedDims[0] + self.fixedDims[0] * self.randomSize)]
        self.randomRangeY = [int(self.fixedDims[1] - self.fixedDims[1] * self.randomSize), int(self.fixedDims[1] + self.fixedDims[1] * self.randomSize)]
        
        
    def setCoordinatesForFixedRoi(self, px, py):
        h, w, _ = self.image.shape
        dx = randint(self.randomRangeX[0], self.randomRangeX[1])
        dy = randint(self.randomRangeY[0], self.randomRangeY[1])
        xmin = max(0, int(px - (dx/2.0)))
        if xmin == 0: 
            xmax = xmin + dx
        else:
            xmax = min(w-1, int(px + (dx/2.0)))
            if xmax == (w-1):
                xmin = xmax - dx
        ymin = max(0, int(py - (dy/2.0)))
        if ymin == 0:
            ymax = ymin + dy 
        else:
            ymax = min(h-1, int(py + (dy/2.0)))
            if ymax == (h-1):
                ymin = ymax - dy
        return [xmin, ymin, xmax, ymax, self.selectedClass]
    
    
    def removeRoi(self):
        self.lastChange = self.rois[self.selectedRoi]
        self.rois.pop(self.selectedRoi)
        self.selectedRoi = None
        self.renderScene()
            
            
    def mousePressEvent(self, event):
        self.newRoi = None
        self.selectedRoi = None
        if self.mouseEnabled:
            self._mouse_button = event.buttons()
            self.posicionInicial = QtCore.QPointF(event.scenePos())
            self.posicionInicialX = int(self.posicionInicial.x())
            self.posicionInicialY = int(self.posicionInicial.y())
            if (self._mouse_button == QtCore.Qt.LeftButton) and self.isClassSelected:
                if self.selectionMode == 1:
                    self.rois.append(self.setCoordinatesForFixedRoi(self.posicionInicialX, self.posicionInicialY))
                    self.lastChange = len(self.rois) - 1
                else:
                    self.newRoi = True
                    self.rois.append([])
            if (self._mouse_button == QtCore.Qt.RightButton):
                self.checkIfRoiSelected()
                if self.selectedRoi is not None:
                    self.menu.popup(QCursor.pos())
            self.renderScene()
            
            
    def mouseMoveEvent(self, event):
        if self.isClassSelected and self.mouseEnabled:
            self._mouse_button = event.buttons()
            if (self._mouse_button == QtCore.Qt.LeftButton):
                self.posicionFinal = QtCore.QPointF(event.scenePos())
                self.posicionFinalX = int(self.posicionFinal.x())
                self.posicionFinalY = int(self.posicionFinal.y())
                if self.newRoi:
                    roiIndex = len(self.rois) - 1
                    self.rois[roiIndex] = [self.posicionInicialX, self.posicionInicialY, self.posicionFinalX, self.posicionFinalY, self.selectedClass]
                    self.rois[roiIndex] = self.sortRoiValues(self.rois[roiIndex])
                    self.lastChange = roiIndex
                    self.renderScene()
                    
            
    def mouseReleaseEvent(self, event):
        if self.isClassSelected and self.mouseEnabled:
            if (self._mouse_button == QtCore.Qt.LeftButton):
                if self.newRoi: 
                    self.newRoi = None
                    if self.rois[len(self.rois) - 1] == []: self.rois.pop(len(self.rois) - 1)
        
        
    def in_hull(self, p, hull):
        try:
            if not isinstance(hull,Delaunay):
                hull = Delaunay(hull)
            return hull.find_simplex(p)>=0
        except:
            return 0
    
    
    def checkIfRoiSelected(self):
        i = 0
        for roi in self.rois:
            hull = [[roi[0], roi[1]], [roi[2], roi[1]], [roi[2], roi[3]], [roi[0], roi[3]]]
            if self.in_hull((self.posicionInicialX, self.posicionInicialY), hull):
                self.selectedRoi = i
                break
            i += 1
            
            
    def sortRoiValues(self, roi):
        xmin = min(roi[0], roi[2])
        ymin = min(roi[1], roi[3])
        xmax = max(roi[0], roi[2])
        ymax = max(roi[1], roi[3])
        h, w, _ = self.image.shape
        if xmax > w - 1: 
            xmax = w - 1
        if ymax > h - 1: 
            ymax = h - 1
        if xmin < 0: 
            xmin = 0
        if ymin < 0: 
            ymin = 0
        newRoi = [xmin, ymin, xmax, ymax, roi[4]]
        return newRoi
    
    
    def getLabelCoords(self, roi, w, h):
        cx, cy = ((roi[2] - roi[0]) / 2.0) + roi[0], ((roi[3] - roi[1]) / 2.0) + roi[1]
        labelpxwidth = len(roi[4]) * 10
        if cx < w / 2.0:
            pxmin = roi[0]
            pxmax = roi[0] + labelpxwidth
        else:
            pxmin = roi[2] - labelpxwidth
            pxmax = roi[2]
        if cy < h / 2:
            pymin = roi[3] + 30
            pymax = roi[3]
            dy = -10
        else:
            pymin = roi[1] - 30
            pymax = roi[1]
            dy = 20
        return pxmin, pymin, pxmax, pymax, dy
        
        
    def renderScene(self):
        image = self.image.copy()
        h, w, _ = image.shape
        i = 0
        for roi in self.rois:
            if roi == []: continue
            color = self.roiColor
            if i == self.selectedRoi:
                color = self.selectionColor
            try:
                cv2.rectangle(image, (roi[0], roi[1]), (roi[2], roi[3]), color, 1, 4)
            except:
                self.rois.pop(len(self.rois)-1)
                continue
            if self.showLabels:
                pxmin, pymin, pxmax, pymax, dy = self.getLabelCoords(roi, w, h)
                cv2.rectangle(image, (pxmin, pymin), (pxmax, pymax), color, cv2.FILLED)
                cv2.putText(image, self.rois[i][4], (pxmin + 10, pymin + dy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
            i += 1
        self.showImage(image)
        
        
    def showImage(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, channels = image.shape
        bytesPerLine = channels * w
        frame = QImage(image.data, w, h, bytesPerLine, QImage.Format_RGB888)
        self.clear()
        self.addPixmap(QPixmap.fromImage(frame))
        self.update()
        return 
    