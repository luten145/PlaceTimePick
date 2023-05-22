import re
from tkinter import *
from konlpy.tag import Kkma
import PythonSource.Util.DicApi as dicApi
from PythonSource.Util import LogUtil as logUtil
from PythonSource.UI.UIListener import UIEventListener
from PythonSource.UI import UIMain
from PythonSource.Engine.Engine1 import Engine1
from PythonSource.Engine.Engine2 import Engine2
from PythonSource.Engine.Engine3 import Engine3
from PythonSource.Engine.Engine4 import Engine4
TAG = "MainManager"
kkma = Kkma()

class MainEngine:

    TAG = "MainEngine"

    def __init__(self,uiManager:UIEventListener):
        self.mUIManager = uiManager
        pass

    def tkinterHandler(self, data):
        Engine4(self.mUIManager).tkinterHandler(data)
        pass

    def jsonHandler(self,data):
        #j = Engine4(self.mUIManager)
        #j.jsonHandler(data)
        Engine2(self.mUIManager).jsonHandler(data)
        #Engine3(self.mUIManager).jsonHandler(data)
        Engine4(self.mUIManager).jsonHandler(data)
        pass

    pass


