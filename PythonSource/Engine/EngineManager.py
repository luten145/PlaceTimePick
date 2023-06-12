from PythonSource.UI.UIListener import UIEventListener
from PythonSource.Engine.Engine2 import Engine2
from PythonSource.Engine.Engine4 import Engine4
TAG = "EngineManager"


class MainEngine:
    def __init__(self,uiManager:UIEventListener):
        self.mUIManager = uiManager
        pass

    def tkinterHandler(self, data):
        Engine4(self.mUIManager).tkinterHandler(data)

    def jsonHandler(self,data):
        Engine2(self.mUIManager).jsonHandler(data)
        #Engine3(self.mUIManager).jsonHandler(data)
        Engine4(self.mUIManager).jsonHandler(data)