from tkinter import *


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