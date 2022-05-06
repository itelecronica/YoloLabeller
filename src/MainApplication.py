'''
Created on 11 jun. 2021

@author: Guille
@comment: Main del configurador para entrenar deteccion de objetos en Floid.
'''


import sys, os
import qtmodern.styles
import qtmodern.windows
from PyQt5.QtWidgets import QApplication
from GUI.MainGUI_QT5 import Ui_MainWindow

PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from UTIL.Logger import logger
from UTIL.Class_JsonManager import JsonManager
from UTIL.Class_BootManager import BootManager
from GUI.Class_MainGUIManager import MainGUIManager
from LOGIC.Class_MainController import MainController





class MainApplication(QApplication):
    
    
    appDir = os.path.dirname(os.path.abspath(__file__)) + "/"
    configGeneralPath = appDir + "../cfg/cfg.json"
    
    
    
    def __init__(self,sys_argv):
        QApplication.__init__(self,sys_argv)
        qtmodern.styles.dark(self)
        self.jsonManager = JsonManager()
        self.getConfigFiles()
        self.mainController = MainController(self.configGeneral, self.appDir)
        self.mainGUIManager = MainGUIManager(Ui_MainWindow, self.configGeneral, self.configGeneralPath, self.mainController, self.appDir)
        self.GUI = qtmodern.windows.ModernWindow(self.mainGUIManager)
        self.GUI.showMaximized()
        self.mainController.initController()
        self.initSignals()


        
    def getConfigFiles(self):
        self.configGeneral = self.jsonManager.getJsonFile(self.configGeneralPath)
        
        
        
    def initSignals(self):
        self.mainGUIManager.exportConfigGeneralFile.connect(self.onConfigGeneralChange)
        
        
        
    def onConfigGeneralChange(self, configGeneral):
        self.configGeneral = configGeneral
        self.mainController.setConfigGeneral(configGeneral)
        self.jsonManager.exportJson(configGeneral, self.configGeneralPath)
        
        
        
        
        
if __name__ == '__main__':
    bootManager = BootManager(logger)
    app = MainApplication(sys.argv)
    sys.exit(app.exec_())
    app.processEvents()


