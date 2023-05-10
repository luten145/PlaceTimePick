from tkinter import *
from konlpy.tag import Kkma
from PythonSource.Util import LogUtil as logUtil
import PythonSource.Util.DicApi as dicApi

TAG = "Engine"

PLACE_INDEX = 0
TIME_INDEX = 1
NAME_INDEX = 2

key = [None] * 3
key[PLACE_INDEX] = ["건물", "공간", "위치", "장소", "서울", "대전", "대구", "부산", "강원"]
key[TIME_INDEX] = ["시간","때","년","월","일","일시",":"]
key[NAME_INDEX] = ["이름","장남","장녀","부","모","사람","인물","아들","딸","김"]



class MainEngine:

    def __init__(self):
        MAX_LINE = 100
        MAX_SCORE_TYPE = 3
        self.scoreTable = [[0 for j in range(MAX_SCORE_TYPE)] for i in range(MAX_LINE)]

        pass


    def getAnalyzeData(self,data):
        currentLine = 0

        for i in range(0, getLineCount(data) + 1): # 라인별로 반복합니다.
            currentLine = i # 현재 라인을 전역변수에 저장
            lineData = getLine(data, i) # 각 라인의 텍스트 데이터를 얻습니다.
            nounList = getNounList(lineData) # 각 라인의 명사 리스트를 얻습니다. (Use KoNlPy)
            for j in nounList: # 명사를 리스트를 반복합니다.
                scarchResult = dicApi.wordSearch(j) # 명사 검색시작

                if(scarchResult != -1):
                    logUtil.Log(TAG, "-------------------")
                    logUtil.Log(TAG, "라인 수 : " + str(currentLine))
                    logUtil.Log(TAG, "검색한 단어 : " + scarchResult.word)
                    logUtil.Log(TAG, "단어의 뜻 : " + scarchResult.definition)
                    logUtil.Log(TAG, "-------------------")
                    self.setScore(currentLine, scarchResult)
                else:
                    logUtil.Log(TAG, "사전에서 단어를 찾을 수 없습니다!")

        for i in range(0,currentLine+1):
            print("LineCount : ", i, self.scoreTable[i]," || ", getLine(data, i))



        for i in range (0,3):
            maxScore = 0
            resultIndex = 0
            for j in range(currentLine +1):
                if maxScore < self.scoreTable[j][i]:
                    maxScore = self.scoreTable[j][i]
                    resultIndex = j

            print(i," | 최고점 : %d" %maxScore, end ='')
            print(" | index : %d" %resultIndex, end ='')
            print(" | 데이터 : ", getLine(data, resultIndex))

    def setScore(self,line, data): # 한 줄에 대한 점수를 채점합니다.
        for j in range(0,3):
            for i in key[j]:
                if data.word.find(i) != -1:
                    self.scoreTable[line][j] +=1

                if data.definition.find(i) != -1:
                    self.scoreTable[line][j] +=1

    pass

def getLineCount(text):
    return int(text.index(END).split(".")[0])-1


def getLine(text, line_number):
    line_start = f"{line_number}.0"
    line_end = f"{line_number}.end"
    line_content = text.get(line_start, line_end)
    return line_content

kkma = Kkma()

def getNounList(data):
    return kkma.nouns(data)
