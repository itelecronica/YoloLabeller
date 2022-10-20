'''
Created on 7 nov. 2019

@author: Guille
@comment: Script que monitoriza el teclado vigilando que el contexto sea la ventana del programa
'''


import time, threading, os
from pynput import keyboard
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
import re, subprocess


class KBD(QThread):
    
    nextImgSignal = pyqtSignal(int)
    backImgSignal = pyqtSignal(int)
    scapeSignal = pyqtSignal()
    saveSignal = pyqtSignal()
    discardSignal = pyqtSignal()
    showLabelSignal = pyqtSignal(int)
    classSelectedSignal = pyqtSignal(int)
    changeSelectionMode = pyqtSignal(int)
    undoneSignal = pyqtSignal()
    waitingSecondKey, kbdEnabled = False, False
    backPressed, nextPressed = False, False
    key_arrow_isPressed = pyqtSignal(int)
    
    
    
    def __init__(self):
        QThread.__init__(self)
        self.holdingKeyPressed = QTimer()
        self.holdingKeyPressed.timeout.connect(self.onHoldedKey)
        self.key_arrow_isPressed.connect(lambda _: self.holdingKeyPressed.start(100))
        self.kbdEnabled = True
        self.screen = b'MainWindow'
        self.screenThread = threading.Thread(target=self.currentWindowMonitor)
        self.screenThread.start()
        return
        
        
    def on_release(self,key):
        if not self.kbdEnabled: return
        if key == keyboard.Key.esc:
            self.scapeSignal.emit()
        elif key == keyboard.Key.left:
            self.backPressed = False
        elif key == keyboard.Key.right:
            self.nextPressed = False
        elif key == keyboard.Key.enter:
            self.saveSignal.emit()
        elif key == keyboard.Key.backspace:
            self.discardSignal.emit()
        elif key == keyboard.KeyCode(char = '1'):
            self.classSelectedSignal.emit(0)
        elif key == keyboard.KeyCode(char = '2'):
            self.classSelectedSignal.emit(1)
        elif key == keyboard.KeyCode(char = '3'):
            self.classSelectedSignal.emit(2)
        elif key == keyboard.KeyCode(char = '4'):
            self.classSelectedSignal.emit(3)
        elif key == keyboard.KeyCode(char = '5'):
            self.classSelectedSignal.emit(4)
        elif key == keyboard.KeyCode(char = '6'):
            self.classSelectedSignal.emit(5)
        elif key == keyboard.KeyCode(char = '7'):
            self.classSelectedSignal.emit(6)
        elif key == keyboard.KeyCode(char = '8'):
            self.classSelectedSignal.emit(7)
        elif key == keyboard.KeyCode(char = '9'):
            self.classSelectedSignal.emit(8)
        elif key == keyboard.Key.shift: 
            self.showLabelSignal.emit(1)
        elif key == keyboard.Key.ctrl:
            self.waitingSecondKey = False
        elif key == keyboard.Key.f1:
            self.changeSelectionMode.emit(1)
        
        
    def on_press(self, key):
        if not self.kbdEnabled: return
        if key == keyboard.Key.ctrl:
            self.waitingSecondKey = True
        elif key == keyboard.Key.left:
            self.backPressed = True
            self.backImgSignal.emit(-1)
            self.key_arrow_isPressed.emit(-1)
        elif key == keyboard.Key.right:
            self.nextPressed = True
            self.nextImgSignal.emit(1)
            self.key_arrow_isPressed.emit(1)
        elif key == keyboard.KeyCode(char = 'z') and self.waitingSecondKey:
            self.undoneSignal.emit()
        return
    
    
    def onHoldedKey(self):
        self.holdingKeyPressed.stop()
        if self.backPressed:
            self.backImgSignal.emit(-1)
        elif self.nextPressed:
            self.nextImgSignal.emit(1)
        else: return
        self.holdingKeyPressed.start(300)
        
        
    def run(self):
        with keyboard.Listener(on_press=self.on_press,on_release=self.on_release) as listener:listener.join()
        self.listener = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        self.listener.start()
        
        
    def get_active_window_title(self):
        root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
        stdout, stderr = root.communicate()
    
        m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
        if m != None:
            window_id = m.group(1)
            window = subprocess.Popen(['xprop', '-id', window_id, 'WM_NAME'], stdout=subprocess.PIPE)
            stdout, stderr = window.communicate()
        else:
            return None
    
        match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", stdout)
        if match != None:
            return match.group("name").strip(b'"')
        return None

    
    def currentWindowMonitor(self):
        while True:
            current_screen = self.get_active_window_title()
            if current_screen == self.screen:
                self.kbdEnabled = True 
            else:
                self.kbdEnabled = False 
            time.sleep(0.1)
                
            
        
        
        