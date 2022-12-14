'''
Created on 30 abr. 2020

@author: Guille
@comment: Clase que controla importacion/exportacion de ficheros json
'''

import json

from UTIL.Class_JsonEncoder import CompactJSONEncoder


class JsonManager(object):


    def __init__(self):
        self.path = None
        self.jsonEncoder = CompactJSONEncoder()
        
        
    def loadJson(self):
        with open(self.path) as json_file:  
            self.jsonFile = json.load(json_file)
          
            
    def getJsonFile(self, path):
        self.path = path
        self.loadJson()
        return self.jsonFile
    
    
    def exportJson(self, outputdict, ruta):
        with open(ruta,"w+") as f:
            f.seek(0)
            f.write(self.jsonEncoder.encode(outputdict))
            f.truncate()
            f.close()
        return