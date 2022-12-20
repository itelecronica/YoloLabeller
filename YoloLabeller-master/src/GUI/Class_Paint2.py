import sys
from PyQt5.QtWidgets import QApplication, QDialog, QGraphicsView, QGraphicsScene, QGridLayout, QPushButton, QComboBox
from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QPen, QBrush, QImage, QPixmap, QTransform
from PyQt5 import uic
import cv2
import numpy as np


class Paint(QGraphicsView):
    def __init__(self):
        QGraphicsView.__init__(self)
        self.img = cv2.imread("./YoloLabeller-master/src/a.jpg")
        self.mask = np.zeros_like(self.img)
        #pixmap = self.createPixmap()
        #self.setSceneRect(QRectF(self.viewport().rect()))
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

    def paintImage(self):
        img = self.img.copy()
        
        self.showImage(img)

    def exportMask(self):
        '''mask = np.zeros_like(self.mask)
        x,y = self.mask.shape[0],self.mask.shape[1]
        print(self.mask[1][1])
        for i in range(x):
            for a in range(y):
                if self.mask[i,a] != [0 0 0]:
                   mask[i][a] = (255,255,255)'''
        mask = cv2.cvtColor(self.mask, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(mask, 50,255,0)
        cv2.imwrite("mask.png", mask)
    
    '''def createPixmap(self):
        #img = cv2.imread("./YoloLabeller-master/src/a.jpg")
        img = self.img.copy()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height1, width1, _ = img.shape
        ### Redimensionar Alto-limite
        #height = 900
        #width = int(height*(width1/height1))
        ### Redimensionar Ancho-limite
        width = self.width()
        height = int(width*(height1/width1))
        img = cv2.resize(img, (width, height))
        
        _, _, channels = img.shape
        bytesPerLine = channels * width
        frame = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)

        #self.setPixmap(QPixmap.fromImage(frame))
        return frame'''
    
    def tools(self, e):
        size_px = 3
        if self.isPaint == True:
            pen = QPen(Qt.red)
            brush = QBrush(Qt.SolidPattern)
            
            self.scene.addItem(self.scene.addEllipse(e.x(), e.y(),size_px,size_px, pen, brush))
            #self.img = cv2.ellipse(self.img,(int(e.x()),int(e.y())),(size_px, size_px),0.,0.,360,(0,0,0))
            if size_px == 1:
                self.mask[int(e.y())][int(e.x())] = (255,255,255)
                #self.img = cv2.rectangle(self.img,(int(e.x()),int(e.y())),(int(e.x()),int(e.y())),(0,0,0),-1)
            else:
                resize = int(size_px/2)
                self.mask = cv2.rectangle(self.mask,(int(e.x())-resize,int(e.y())-resize),(int(e.x())+resize,int(e.y())+resize),(0,0,255),-1)
            self.paintImage()
            self.setScene(self.scene)
        if self.isDelete == True:
            items = self.items(e.x(), e.y())
            for item in items:
                resize = int(size_px/2)
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
        self.tools(e)
        self.startX = e.x()
        self.startY = e.y()
    
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
        '''pixmap = self.createPixmap()
        #self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(pixmap))
        self.scene.update()'''
        '''self.ui.graphicsView_visualizer.setTransform(QTransform().scale(self.zoom, self.zoom))
        self.ui.graphicsView_visualizer.setScene(self.mainScene)
        self.mainScene.update()'''

class Dialogo(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.resize(1000, 800)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.paint = Paint()
        self.btn_paint = QPushButton("Dibujar")
        self.combo_object = QComboBox()
        self.combo_object.addItem("Seleccionar")
        self.combo_object.addItem("Line")
        self.combo_object.addItem("Rect")
        self.combo_object.addItem("Ellipse")
        self.btn_delete = QPushButton("Borrar")
        self.btn_clear = QPushButton("Export")
        self.layout.addWidget(self.btn_paint)
        self.layout.addWidget(self.combo_object)
        self.layout.addWidget(self.btn_delete)
        self.layout.addWidget(self.btn_clear)
        self.layout.addWidget(self.paint)
        self.btnDefault = "background-color: grey; border: 0; padding: 10px"
        self.btnActive = "background-color: orange; border: 0; padding: 10px"
        
        self.btn_paint.setStyleSheet(self.btnDefault)
        self.combo_object.setStyleSheet(self.btnDefault)
        self.btn_delete.setStyleSheet(self.btnDefault)
        self.btn_clear.setStyleSheet(self.btnDefault)
        
        self.btn_paint.clicked.connect(self.isPaint)
        self.combo_object.currentIndexChanged.connect(self.isObject)
        self.btn_delete.clicked.connect(self.isDelete)
        self.btn_clear.clicked.connect(self.paint.exportMask)
  
    def resizeEvent(self, event):
        self.paint.setSceneRect(QRectF(self.paint.viewport().rect()))
    
    def isPaint(self):
        if self.paint.isPaint == False:
            self.paint.isPaint = True
            self.btn_paint.setStyleSheet(self.btnActive)
        else:
            self.paint.isPaint = False
            self.btn_paint.setStyleSheet(self.btnDefault)
            
        self.paint.isObject = None  
        self.paint.isDelete = False
        self.paint.isClear = False
        self.btn_delete.setStyleSheet(self.btnDefault)
        self.btn_clear.setStyleSheet(self.btnDefault)
    
    def isObject(self):
        object = self.combo_object.currentIndex()
        self.paint.isObject = object
        self.paint.isPaint = False
        self.paint.isDelete = False
        self.paint.isClear = False
        self.btn_paint.setStyleSheet(self.btnDefault)
        self.btn_delete.setStyleSheet(self.btnDefault)
        self.btn_clear.setStyleSheet(self.btnDefault)
    
    
    def isDelete(self):
        if self.paint.isDelete == False:
            self.paint.isDelete = True
            self.btn_delete.setStyleSheet(self.btnActive)
        else:
            self.paint.isDelete = False
            self.btn_delete.setStyleSheet(self.btnDefault)
    
        self.paint.isObject = None 
        self.paint.isPaint = False
        self.paint.isClear = False
        self.btn_paint.setStyleSheet(self.btnDefault)
        self.btn_clear.setStyleSheet(self.btnDefault)
    
    def isClear(self):
        if self.paint.isClear == False:
            self.paint.isClear = True
            self.btn_clear.setStyleSheet(self.btnActive)
        else:
            self.paint.isClear = False
            self.btn_clear.setStyleSheet(self.btnDefault)
        
        self.paint.isObject = None 
        self.paint.isPaint = False
        self.paint.isDelete = False
        self.btn_paint.setStyleSheet(self.btnDefault)
        self.btn_delete.setStyleSheet(self.btnDefault)
        self.paint.scene.clear()
  
app = QApplication(sys.argv)
dialogo = Dialogo()
dialogo.show()
app.exec_()