import Util,UI
import DicApi as dicAPI
from tkinter import *
from konlpy.tag import Kkma

TAG = "TestLabMain"

kkma = Kkma()
uiManager = UI.UIManager()

MAX_LINE = 100
MAX_SCORE_TYPE = 3
scoreTable = [[0 for j in range(MAX_SCORE_TYPE)] for i in range(MAX_LINE)]

def main():
    uiInit()
    pass

def uiInit():
    uiManager.uiInit()
    root = uiManager.getRoot()
    text = Text(root, wrap=WORD)
    text.place(x= 50,y=50,height=100,width=400)
    text.pack()

    btn = Button(root, text="검색", command = lambda : startAnalyze(text))
    btn.place(x= 200,y=200,height=10,width=50)
    btn.pack()

    uiManager.startLoop()
    pass


def startAnalyze(data):
    currentLine = 0

    for i in range(0, getLineCount(data) + 1): # 라인별로 반복합니다.
        currentLine = i # 현재 라인을 전역변수에 저장
        lineData = getLine(data, i) # 각 라인의 텍스트 데이터를 얻습니다.
        nounList = getNounList(lineData) # 각 라인의 명사 리스트를 얻습니다. (Use KoNlPy)
        for j in nounList: # 명사를 리스트를 반복합니다.
            scarchResult = dicAPI.wordSearch(j) # 명사 검색시작

            if(scarchResult != -1):
                Util.Log(TAG,"-------------------")
                Util.Log(TAG,"라인 수 : "+str(currentLine))
                Util.Log(TAG,"검색한 단어 : " + scarchResult.word)
                Util.Log(TAG,"단어의 뜻 : " + scarchResult.definition)
                Util.Log(TAG,"-------------------")
                setScore(currentLine, scarchResult)
            else:
                Util.Log(TAG,"사전에서 단어를 찾을 수 없습니다!")

    for i in range(0,currentLine+1):
        print("LineCount : ", i, scoreTable[i]," || ", getLine(data, i))



    for i in range (0,3):
        maxScore = 0
        resultIndex = 0
        for j in range(currentLine +1):
            if maxScore < scoreTable[j][i]:
                maxScore = scoreTable[j][i]
                resultIndex = j

        print(i," | 최고점 : %d" %maxScore, end ='')
        print(" | index : %d" %resultIndex, end ='')
        print(" | 데이터 : ", getLine(data, resultIndex))



PLACE_INDEX = 0
TIME_INDEX = 1
NAME_INDEX = 2

key = [None] * 3
key[PLACE_INDEX] = ["건물", "공간", "위치", "장소", "서울", "대전", "대구", "부산", "강원"]
key[TIME_INDEX] = ["시간","때","년","월","일","일시",":"]
key[NAME_INDEX] = ["이름","장남","장녀","부","모","사람","인물","아들","딸","김"]


def setScore(line, data): # 한 줄에 대한 점수를 채점합니다.
    for j in range(0,3):
        for i in key[j]:
            if data.word.find(i) != -1:
                scoreTable[line][j] +=1

            if data.definition.find(i) != -1:
                scoreTable[line][j] +=1
    return 0


def getLineCount(text):
    return int(text.index(END).split(".")[0])-1


def getLine(text, line_number):
    line_start = f"{line_number}.0"
    line_end = f"{line_number}.end"
    line_content = text.get(line_start, line_end)
    return line_content


def getNounList(data):
    return kkma.nouns(data)


main()