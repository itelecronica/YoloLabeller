# -*- coding: utf-8 -*-
'''
Created on 14 nov. 2017

@author: Manuel. Rev. Guille
'''

import os
import logging



from logging.handlers import TimedRotatingFileHandler





appDir = os.path.dirname(os.path.abspath(__file__))
logPath = appDir + "/../../logs/"





def CreateLogger(logName):
    #Creando logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    #Formato del log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
    #Creando handler para consola y para fichero, fichero rotativo en medianoche por lo que genera nuevo fichero
    fileHandler = TimedRotatingFileHandler(logPath + str(logName)+'.log', when = 'midnight', backupCount=2)
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)
    return logger





# Creamos un logger para salida por pantalla y a fichero
if not os.path.exists(logPath):
    try:
        os.makedirs(logPath)
    except:
        print ("ERROR:: generacion de directorio logs")
logger = CreateLogger("LOG")
