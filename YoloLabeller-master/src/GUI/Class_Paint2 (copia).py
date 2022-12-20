import sys
from PyQt5.QtWidgets import QApplication, QDialog, QGraphicsView, QGraphicsScene, QGridLayout, QPushButton, QComboBox
from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QPen, QBrush
from PyQt5 import uic

class Paint(QGraphicsView):
    def __init__(self):
        QGraphicsView.__init__(self)
        self.setSceneRect(QRectF(self.viewport().rect()))
        self.scene = QGraphicsScene()
        self.isPaint = False
        self.isDelete = False
        self.isClear = False
        self.isObject = None
        self.startX = None
        self.startY = None
    
    def tools(self, e):
        if self.isPaint == True:
            pen = QPen(Qt.black)
            brush = QBrush(Qt.SolidPattern)
            self.scene.addItem(self.scene.addEllipse(e.x(), e.y(), 3, 3, pen, brush))
            self.setScene(self.scene)
        if self.isDelete == True:
            items = self.items(e.x(), e.y())
            for item in items:
                self.scene.removeItem(item)
        
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

class Dialogo(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.resize(500, 500)
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
        self.btn_clear = QPushButton("Clear")
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
        self.btn_clear.clicked.connect(self.isClear)
  
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