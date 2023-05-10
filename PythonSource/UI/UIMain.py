from tkinter import *
from PythonSource.UI.UIListener import FrameworkListener
from PythonSource.UI.UIListener import UIEventListener
from PythonSource.Util import LogUtil as logUtil

TAG = "UIMain"

class UIManager:

    TAG = "UIManager"

    def __init__(self, listener_sample: FrameworkListener):
        self.listener_sample = listener_sample
        self.uiInit()


    class ListenerSampleImpl(UIEventListener):
        def onSetDataEvent(self,index : int,text : str) -> bool:
            logUtil.Log(TAG, "Index : " + str(index) + " | Data : " + text)
            return False


    def getDataEventListener(self):
        return self.ListenerSampleImpl()


    def uiInit(self):
        self.root = Tk()
        self.root.title("Test Lab")
        self.root.geometry("500x700")

        self.btn = Button(self.root, text="검색", command= lambda :self.listener_sample.onTkinterEvent(self.text))
        self.btn.place(x= 200,y=200,height=10,width=50)
        self.btn.pack()

        self.btn2 = Button(self.root, text="파일 열기", command= lambda :self.listener_sample.onJsonOpenEvent())
        self.btn2.place(x= 220,y=220,height=10,width=50)
        self.btn2.pack()

        self.text = Text(self.root, wrap=WORD)
        self.text.place(x= 50,y=50,height=100,width=400)
        self.text.pack()

        frame1 = Frame(self.root, relief='solid', bd=2)
        frame1.pack(side='top', fill="both", expand=FALSE)

        frame2 = Frame(self.root, relief='solid', bd=2)
        frame2.pack(side='bottom', fill='both', expand=True, padx= 50, pady=50)

        textlist = []

        for i in range(18):
            textlist.append(Label(frame2))


        textlist[0].config(text='시ㆍ도')
        textlist[2].config(text='군ㆍ구')
        textlist[4].config(text='읍ㆍ면ㆍ동')
        textlist[6].config(text='도로명')
        textlist[8].config(text='건물번호')
        textlist[10].config(text='동ㆍ층ㆍ호')
        textlist[12].config(text='추가정보')

        count = 0
        for i in range(3):
            for j in range(6):
                textlist[count].grid(row=i, column=j, ipadx=10, ipady=10)
                count += 1

pass