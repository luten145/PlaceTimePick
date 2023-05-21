from tkinter import *
from PythonSource.UI.UIListener import FrameworkListener
from PythonSource.UI.UIListener import UIEventListener
from PythonSource.Util import LogUtil as logUtil
from PythonSource.Engine.Engine4 import *


placeTextList = []
timeTextList = []
globalIndex = 0
globalText = ''
addInfoTextList = []

PLACE_SI = 1
PLACE_GU = 3
PLACE_DONG = 5
PLACE_STREET = 7
PLACE_NUM = 9
PLACE_HO = 11
TIME_YEAR = 13
TIME_MONTH = 15
TIME_DATE = 17
TIME_HOUR = 19
TIME_MIN = 21


TAG = "UIMain"

class UIManager:

    TAG = "UIManager"

    def __init__(self, listener_sample: FrameworkListener):
        self.listener_sample = listener_sample
        self.uiInit()


    class ListenerSampleImpl(UIEventListener):
        def onSetDataEvent(self,index : int,text) -> bool:
            global globalIndex
            global globalText

            if (type(text) == str ):
                globalIndex = index
                globalText = text
                self.UIdEit.editLabel(self)
                logUtil.Log(TAG, "Index : " + str(index) + " | Data : " + text)
            elif(type(text) == SendData):
                text : SendData
                for i in text.addressTable:
                    Log(TAG,i.__dict__)
                for i in text.otherInfo:
                    Log(TAG,i)
            return False

        class UIdEit:
            def editLabel(self):
                global placeTextList
                global globalIndex
                global globalText
                global addInfoTextList

                if globalIndex < 13:
                    placeTextList[globalIndex].config(text=globalText)
                elif globalIndex == 23:
                    addInfoTextList[21 - globalIndex + 1].config(text=globalText)
                else:
                    timeTextList[globalIndex + 1 - 14].config(text=globalText)

    def getDataEventListener(self):
        return self.ListenerSampleImpl()

    def uiInit(self):
        global placeTextList
        global timeTextList
        global addInfoTextList
        self.root = Tk()
        self.root.title("Test Lab")
        self.root.geometry("750x1000")

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
        frame2.pack(side='top', fill="x", expand=True, padx= 20, pady=20)

        frame3 = Frame(self.root, relief='solid', bd=2)
        frame3.pack(side='top', fill="x", expand=True, padx= 20, pady=20)

        frame4 = Frame(self.root, relief='solid', bd=2)
        frame4.pack(side='bottom', fill="x", expand=True, padx= 20, pady=20)


        for i in range(12):
            placeTextList.append(Label(frame2))

        placeTextList[0].config(text='시ㆍ도')
        placeTextList[2].config(text='군ㆍ구')
        placeTextList[4].config(text='읍ㆍ면ㆍ동')
        placeTextList[6].config(text='도로명')
        placeTextList[8].config(text='건물번호')
        placeTextList[10].config(text='동ㆍ층ㆍ호')

        for i in range(10):
            timeTextList.append(Label(frame3))

        timeTextList[1].config(text='년')
        timeTextList[3].config(text='월')
        timeTextList[5].config(text='일')
        timeTextList[7].config(text='시')
        timeTextList[9].config(text='분')

        for i in range(3):
            addInfoTextList.append(Label(frame4))

        addInfoTextList[0].config(text='추가정보')

        count = 0
        for i in range(2):
            for j in range(6):
                placeTextList[count].grid(row=i, column=j, padx=3, pady=5)
                count += 1

        count = 0
        j = 0
        for i in range(10):
            timeTextList[count].grid(row=3, column=j, ipadx=3, ipady=10)
            count += 1
            j += 1


        addInfoTextList[0].grid(row=4, column = 0)

        count = 0
        for i in range(len(addInfoTextList)):
            addInfoTextList[count].grid(row=5 + count, column = 1)
            count