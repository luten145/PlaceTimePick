import re
from tkinter import *
from konlpy.tag import Kkma
import PythonSource.Util.DicApi as dicApi
from PythonSource.Util import Log as logUtil
from PythonSource.UI.UIListener import UIEventListener
from PythonSource.UI import UIMain

TAG = "Engine1"

PLACE_INDEX = 0
TIME_INDEX = 1
NAME_INDEX = 2

key = [None] * 3
key[PLACE_INDEX] = ["건물", "공간", "위치", "장소", "서울", "대전", "대구", "부산", "강원"]
key[TIME_INDEX] = ["시간","때","년","월","일","일시",":"]
key[NAME_INDEX] = ["이름","장남","장녀","부","모","사람","인물","아들","딸","김"]


MAX_LINE = 100
MAX_SCORE_TYPE = 3
scoreTable = [[0 for j in range(MAX_SCORE_TYPE)] for i in range(MAX_LINE)]

class Engine1:

    def __init__(self,uiManager : UIEventListener):
        print("Git Update Test")

        self.mUIManager = uiManager


        self.currentLine = 0
        pass

    def tkinterHandler(self, data):
        self.mUIManager.onSetDataEvent(1,"HELLO ENGINE1")
        self.currentLine = 0

        for i in range(0, self.getLineCount(data) + 1): # 전체 라인을 반복합니다.
            self.currentLine = i # 현재 라인을 전역변수에 저장
            self.lineHandler(self.getLine(data, i))

        self.resultPrint(self.currentLine,data)

    def __init__(self,uiManager : UIEventListener):
        self.mUIManager = uiManager
        pass

    def jsonHandler(self,data):
        self.mUIManager.onSetDataEvent(1,"HELLO ENGINE2")
        logUtil.LogUtil_old(TAG, "dataIN!!")
        # data is json File
        # json 파일 내에 text 키의 값들만 읽어서 하나의 리스트로 만들기
        text_list = data["task_result"]["text"]
        combined_text = "".join(text_list)
        text = [combined_text]

        text_list=str(text).split('\\n')
        text_str=str(text).replace("\\n"," ")
        print(text_list)
        print(text_str)

        self.mUIManager.onSetDataEvent(1,"HELLO ENGINE1")
        self.currentLine = 0

        k = 0
        for i in text_list: # 전체 라인을 반복합니다.
            self.currentLine = k # 현재 라인을 전역변수에 저장
            self.lineHandler(i)
            k+=1

        self.resultPrint(self.currentLine,text_list)


        pass

    def lineHandler(self,data:str): # Line -> NounList
        nounList = self.getNounList(data) # 각 라인의 명사 리스트를 얻습니다. (Use KoNlPy)
        for j in nounList: # 명사를 리스트를 반복합니다.
            self.nounHandler(self.currentLine,j)


    def nounHandler(self,currentLine,noun:str): # Noun -> Search
        scarchResult = dicApi.wordSearch(noun) # 명사 검색시작

        if(scarchResult != -1):
            logUtil.LogUtil_old(TAG, "-------------------")
            logUtil.LogUtil_old(TAG, "라인 수 : " + str(currentLine))
            logUtil.LogUtil_old(TAG, "검색한 단어 : " + scarchResult.word)
            logUtil.LogUtil_old(TAG, "단어의 뜻 : " + scarchResult.addr)
            logUtil.LogUtil_old(TAG, "-------------------")
            self.setScore(currentLine, scarchResult)
        else:
            logUtil.LogUtil_old(TAG, "사전에서 단어를 찾을 수 없습니다!")

    def setScore(self,line, data): # 한 줄에 대한 점수를 채점합니다.
        for j in range(0,3):
            for i in key[j]:
                if data.word.find(i) != -1:
                    scoreTable[line][j] +=1

                if data.addr.find(i) != -1:
                    scoreTable[line][j] +=1

    def resultPrint(self,currentLine,data):
        for i in range(0,currentLine+1):
            print("LineCount : ", i, scoreTable[i]," || ", self.getLine(data, i))
        for i in range (0,3):
            maxScore = 0
            resultIndex = 0
            for j in range(currentLine +1):
                if maxScore < scoreTable[j][i]:
                    maxScore = scoreTable[j][i]
                    resultIndex = j

            print(i," | 최고점 : %d" %maxScore, end ='')
            print(" | index : %d" %resultIndex, end ='')
            print(" | 데이터 : ", self.getLine(data, resultIndex))

    def getLineCount(self,text):
        return int(text.index(END).split(".")[0])-1

    def getLine(self,text, line_number):
        return text[line_number]

    kkma = Kkma()

    def getNounList(self,data):
        return self.kkma.nouns(data)
    pass