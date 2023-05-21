from tkinter import *
class FrameworkListener:
    def onTkinterEvent(self, text : Text) -> bool:
        pass
    def onJsonOpenEvent(self) -> bool:
        pass

class UIEventListener:
    def onSetDataEvent(self,index : int,data) -> bool:
        pass