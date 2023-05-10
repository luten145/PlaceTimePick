from tkinter import *
class FrameworkListener:
    def onAnalyzeEvent(self,text : Text) -> bool:
        pass

class UIEventListener:
    def onSetDataEvent(self,index : int,text : str) -> bool:
        pass