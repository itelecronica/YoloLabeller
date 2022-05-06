'''
Created on 26 may. 2021

@author: Guille L.
@comment: Si ya hay un programa con el mismo nombre ejecutandose, evitara una segunda ejecucion.
'''


from PyQt5.QtWidgets import QMessageBox, QApplication
import psutil, sys, os


class BootManager(object):


    def __init__(self, logger):
        self.logger = logger
        nProcRunning, nProcOnATime = self.get_process()
        if nProcRunning > nProcOnATime:
            self.abortExec()
        
        
    def get_process(self):
        p = psutil.Process(os.getpid())
        command = p.cmdline()
        process_name = command[len(command)-1]
        self.logger.info("ARRANQUE:: Inicializando programa; nombre de proceso:")
        self.logger.info(process_name)
        process_name = self.getProgramName(process_name)
        if ".py" in process_name: 
            process_name = process_name.split(".py")
            process_name = process_name[0]
            nProcOnATime = 1
        else: nProcOnATime = 2
        processList = []
        for process_ in psutil.process_iter():
            processList_ = process_.cmdline()
            for name in processList_:
                if process_name in name:
                    processList.append(process_)
        return len(processList), nProcOnATime
    
    
    def getProgramName(self, processName):
        processName = processName.split("/")
        processName = processName[len(processName)-1]
        return processName

    
    def abortExec(self):
        self.logger.error("ARRANQUE:: Programa ya en ejecucion")
        _ = QApplication(sys.argv)
        QMessageBox.question(None, 'Error', "Programa ya en ejecucion")
        sys.exit()
        
        
        