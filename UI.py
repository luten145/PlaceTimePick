from tkinter import *


class ListenerSample:
    def hello(self, data: int, data22: str) -> bool:
        pass

class Hellooo:
    def __init__(self, listener_sample: ListenerSample):
        self.listener_sample = listener_sample
        self.listener_sample.hello(5, "fdsfsd")

class UIManager:

    global root
    global text
    global btn

    def uiInit(self):
        global root
        global text
        global btn
        root = Tk()
        root.title("Test Lab")
        root.geometry("500x500")


    def getRoot(self):
        return root

    def startLoop(self):
        root.mainloop()

pass