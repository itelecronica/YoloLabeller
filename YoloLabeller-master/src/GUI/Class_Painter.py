import sys
from PyQt5.QtWidgets import QApplication, QDialog, QGraphicsView, QGraphicsScene, QGridLayout, QPushButton, QComboBox, QMainWindow
from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QPen, QBrush, QImage, QPixmap, QTransform
from PyQt5 import uic
import cv2
import numpy as np

from GUI.WindowPaint import Ui_WindowPaint


class Paint(QGraphicsView):
    def __init__(self):
        #print (parent)
        QGraphicsView.__init__(self)
        #super(Paint, self).__init__ (parent)
        #self.img = cv2.imread("./YoloLabeller-master/src/a.jpg")
        self.mask = np.zeros_like(self.img)
        #pixmap = self.createPixmap()
        self.setSceneRect(QRectF(self.viewport().rect()))
        self.scene = QGraphicsScene()
        #self.scene.addPixmap(QPixmap.fromImage(pixmap))
        #self.scene.update()
        self.showImage(self.img)
        self.isPaint = False
        self.isDelete = False
        self.isClear = False
        self.isObject = None
        self.startX = None
        self.startY = None
        self.zoom = 1
        self.sizePixel =1
        self.dragMode = False

    def showImage(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if np.sum(self.mask == 0) == (self.mask.shape[0]*self.mask.shape[1]):
            self.mask = np.zeros_like(image)
        image = cv2.addWeighted(image, 0.5,self.mask,0.5,0.0)
        h, w, channels = image.shape
        bytesPerLine = channels * w
        frame = QImage(image.data, w, h, bytesPerLine, QImage.Format_RGB888)
        self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(frame))
        self.scene.update()
        return 

    def exportMask(self):
        
        mask = cv2.cvtColor(self.mask, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(mask, 50,255,0)
        cv2.imwrite("mask.png", mask)

    def paintImage(self):
        img = self.img.copy()
        
        self.showImage(img)
    
    def tools(self, e):
        #size_px = 3
        if self.isPaint == True:
            pen = QPen(Qt.red)
            brush = QBrush(Qt.SolidPattern)
            try:
                self.scene.addItem(self.scene.addEllipse(e.x(), e.y(),self.sizePixel,self.sizePixel, pen, brush))
                #self.img = cv2.ellipse(self.img,(int(e.x()),int(e.y())),(size_px, size_px),0.,0.,360,(0,0,0))
                if self.sizePixel == 1:
                    #self.mask[int(e.y())][int(e.x())] = (255,255,255)
                    self.mask = cv2.rectangle(self.mask,(int(e.x()),int(e.y())),(int(e.x()),int(e.y())),(0,0,255),-1)
                else:
                    resize = int(self.sizePixel/2)
                    self.mask = cv2.rectangle(self.mask,(int(e.x())-resize,int(e.y())-resize),(int(e.x())+resize,int(e.y())+resize),(0,0,255),-1)
                self.paintImage()
                self.setScene(self.scene)
            except: 
                pass
        if self.isDelete == True:
            items = self.items(e.x(), e.y())
            for item in items:
                resize = int(self.sizePixel/2)
                self.mask = cv2.rectangle(self.mask,(int(e.x())-resize,int(e.y())-resize),(int(e.x())+resize,int(e.y())+resize),(0,0,0),-1)
                #self.scene.removeItem(item)
                self.paintImage()

        
    def paintObject(self, e):
        print(self.isObject)
        if self.isObject != None:
            object = self.isObject
            if object == 1: #Line
                pen = QPen(Qt.black)
                self.scene.addItem(self.scene.addLine(self.startX, self.startY, e.x(), e.y(), pen))
                self.setScene(self.scene)
            elif object == 2: #Rect
                pen = QPen(Qt.black)
                brush = QBrush(Qt.SolidPattern)
                self.scene.addItem(self.scene.addRect(self.startX, self.startY, e.x()-self.startX, e.y()-self.startY, pen, brush))
                self.setScene(self.scene)
            elif object == 3: #Ellipse
                pen = QPen(Qt.black)
                brush = QBrush(Qt.SolidPattern)
                self.scene.addItem(self.scene.addEllipse(self.startX, self.startY, e.x()-self.startX, e.y()-self.startY, pen, brush))
                self.setScene(self.scene)
        
        
    def mousePressEvent(self, event):
        e = QPointF(self.mapToScene(event.pos()))
        self._mouse_button = event.buttons()    
        if self._mouse_button == Qt.MiddleButton:
            if self.dragMode == False:
                self.setDragMode(QGraphicsView.ScrollHandDrag)
                self.dragMode = True
            else:
                self.setDragMode(QGraphicsView.NoDrag)
                self.dragMode = False
        else:
            try:
                self.tools(e)
                self.startX = e.x()
                self.startY = e.y()
            except: 
                pass
    
    def mouseReleaseEvent(self, event):
        e = QPointF(self.mapToScene(event.pos()))
        self.paintObject(e)
        
    def mouseMoveEvent(self, event):
        e = QPointF(self.mapToScene(event.pos()))
        self.tools(e)

    def wheelEvent(self, event):
        #print (int(event.angleDelta().y()))
        moose = (event.angleDelta().y())/120
        if moose > 0:
            #mainConfigurator.zoomIn()
            self.zoomIn()
        elif moose < 0:
            #mainConfigurator.zoomOut()
            self.zoomOut()

    def zoomIn(self):
        self.zoom *= 1.05
        self.updateView()
        
    def zoomOut(self):
        self.zoom /= 1.05
        self.updateView()

    def updateView(self):
        
        self.setTransform(QTransform().scale(self.zoom, self.zoom))
        self.paintImage()

        
    def paintObject(self, e):
        print(self.isObject)
        if self.isObject != None:
            object = self.isObject
            if object == 1: #Line
                pen = QPen(Qt.black)
                self.scene.addItem(self.scene.addLine(self.startX, self.startY, e.x(), e.y(), pen))
                self.setScene(self.scene)
            elif object == 2: #Rect
                pen = QPen(Qt.black)
                brush = QBrush(Qt.SolidPattern)
                self.scene.addItem(self.scene.addRect(self.startX, self.startY, e.x()-self.startX, e.y()-self.startY, pen, brush))
                self.setScene(self.scene)
            elif object == 3: #Ellipse
                pen = QPen(Qt.black)
                brush = QBrush(Qt.SolidPattern)
                self.scene.addItem(self.scene.addEllipse(self.startX, self.startY, e.x()-self.startX, e.y()-self.startY, pen, brush))
                self.setScene(self.scene)

    def updateSizePixel(self, value):
        self.sizePixel = value

class PainterMask(QDialog):

    def __init__(self):
        #super(PainterMask, self).__init__()
        QDialog.__init__(self)
        self.ui = Ui_WindowPaint()
        self.ui.setupUi(self)

        self.paint = Paint()
        self.ui.horizontalLayout.addWidget(self.paint)
        self.btnDefault = "background-color: grey; border: 0; padding: 10px"
        self.btnActive = "background-color: orange; border: 0; padding: 10px"

        self.ui.pushButton_Dibujar.clicked.connect(self.isPaint)
        self.ui.pushButton_Borrar.clicked.connect(self.isDelete)
        self.ui.pushButton_Exportar.clicked.connect(self.paint.exportMask)
        self.ui.horizontalSlider.valueChanged.connect(lambda _: self.paint.updateSizePixel(self.ui.horizontalSlider.value()))

    def resizeEvent(self, event):
        self.paint.setSceneRect(QRectF(self.paint.viewport().rect()))
    
    def isPaint(self):

        if self.paint.isPaint == False:
            self.paint.isPaint = True
            self.ui.pushButton_Dibujar.setStyleSheet(self.btnActive)
        else:
            self.paint.isPaint = False
            self.ui.pushButton_Dibujar.setStyleSheet(self.btnDefault)
        self.paint.isClear = False
        self.ui.pushButton_Borrar.setStyleSheet(self.btnDefault)

    def isDelete(self):
        if self.paint.isDelete == False:
            self.paint.isDelete = True
            self.ui.pushButton_Borrar.setStyleSheet(self.btnActive)
        else:
            self.paint.isDelete = False
            self.ui.pushButton_Borrar.setStyleSheet(self.btnDefault)
    
        self.paint.isPaint = False
        self.ui.pushButton_Dibujar.setStyleSheet(self.btnDefault)

    def initPaint(self):
        self.show()