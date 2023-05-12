from tkinter import *
from konlpy.tag import Kkma
from PythonSource.Util import LogUtil as logUtil
import PythonSource.Util.DicApi as dicApi
import re
from PythonSource.UI.UIListener import UIEventListener

TAG = "Engine"


class MainEngine:

    def __init__(self,uiManager:UIEventListener):
        self.mUIManager = uiManager
        pass

    def tkinterHandler(self, data):
        Engine1(self.mUIManager).tkinterHandler(data)
        pass

    def jsonHandler(self,data):
        Engine2(self.mUIManager).jsonHandler(data)
        pass

    pass


class Engine1:
    def __init__(self,uiManager : UIEventListener):
        print("Git Update Test")
        
        self.mUIManager = uiManager

        self.PLACE_INDEX = 0
        self.TIME_INDEX = 1
        self.NAME_INDEX = 2

        self.key = [None] * 3
        self.key[self.PLACE_INDEX] = ["건물", "공간", "위치", "장소", "서울", "대전", "대구", "부산", "강원"]
        self.key[self.TIME_INDEX] = ["시간","때","년","월","일","일시",":"]
        self.key[self.NAME_INDEX] = ["이름","장남","장녀","부","모","사람","인물","아들","딸","김"]

        MAX_LINE = 100
        MAX_SCORE_TYPE = 3
        self.scoreTable = [[0 for j in range(MAX_SCORE_TYPE)] for i in range(MAX_LINE)]
        self.currentLine = 0
        pass

    def tkinterHandler(self, data):
        self.mUIManager.onSetDataEvent(1,"HELLO ENGINE1")
        self.currentLine = 0

        for i in range(0, self.getLineCount(data) + 1): # 전체 라인을 반복합니다.
            self.currentLine = i # 현재 라인을 전역변수에 저장
            self.lineHandler(self.getLine(data, i))

        self.resultPrint(self.currentLine,data)


    def lineHandler(self,data:str): # Line -> NounList
        nounList = self.getNounList(data) # 각 라인의 명사 리스트를 얻습니다. (Use KoNlPy)
        for j in nounList: # 명사를 리스트를 반복합니다.
            self.nounHandler(self.currentLine,j)


    def nounHandler(self,currentLine,noun:str): # Noun -> Search
        scarchResult = dicApi.wordSearch(noun) # 명사 검색시작

        if(scarchResult != -1):
            logUtil.Log(TAG, "-------------------")
            logUtil.Log(TAG, "라인 수 : " + str(currentLine))
            logUtil.Log(TAG, "검색한 단어 : " + scarchResult.word)
            logUtil.Log(TAG, "단어의 뜻 : " + scarchResult.definition)
            logUtil.Log(TAG, "-------------------")
            self.setScore(currentLine, scarchResult)
        else:
            logUtil.Log(TAG, "사전에서 단어를 찾을 수 없습니다!")

    def setScore(self,line, data): # 한 줄에 대한 점수를 채점합니다.
        for j in range(0,3):
            for i in self.key[j]:
                if data.word.find(i) != -1:
                    self.scoreTable[line][j] +=1

                if data.definition.find(i) != -1:
                    self.scoreTable[line][j] +=1

    def resultPrint(self,currentLine,data):
        for i in range(0,currentLine+1):
            print("LineCount : ", i, self.scoreTable[i]," || ", self.getLine(data, i))
        for i in range (0,3):
            maxScore = 0
            resultIndex = 0
            for j in range(currentLine +1):
                if maxScore < self.scoreTable[j][i]:
                    maxScore = self.scoreTable[j][i]
                    resultIndex = j

            print(i," | 최고점 : %d" %maxScore, end ='')
            print(" | index : %d" %resultIndex, end ='')
            print(" | 데이터 : ", self.getLine(data, resultIndex))

    def getLineCount(self,text):
        return int(text.index(END).split(".")[0])-1

    def getLine(self,text, line_number):
        line_start = f"{line_number}.0"
        line_end = f"{line_number}.end"
        line_content = text.get(line_start, line_end)
        return line_content

    kkma = Kkma()

    def getNounList(self,data):
        return self.kkma.nouns(data)
    pass


class Engine2:
    def __init__(self,uiManager : UIEventListener):
        self.mUIManager = uiManager
        prin
        pass

    def jsonHandler(self,data):
        self.mUIManager.onSetDataEvent(1,"HELLO ENGINE2")
        logUtil.Log(TAG,"dataIN!!")
        # data is json File
        # json 파일 내에 text 키의 값들만 읽어서 하나의 리스트로 만들기
        text_list = data["task_result"]["text"]
        combined_text = "".join(text_list)
        text = [combined_text]

        text_list=str(text).split('\\n')
        text_str=str(text).replace("\\n"," ")
        print(text_list)
        print()
        print()

        placeKey = ["서울","부산","대구","인천","광주","대전","울산","경기","강원","충청","전라","경상","제주","세종","홀","웨딩","층"]
        place_list=[]

        nameKey = ['남','녀',"아들","딸",'의']
        name_list=[]

        for i in range(len(text_list)):
            for j in placeKey:
                if text_list[i].find(j) != -1:
                    place_list.append(text_list[i])
                    break

            for j in nameKey:
                if text_list[i].find(j) != -1:
                    name_list.append(text_list[i+1])
                    break

        #초기화
        year,month,day,week,hour,minute=0,0,0,0,0,0

        # 년도 추출
        year_str = re.search(r'\d+년', text_str)[0]
        year = int(re.search(r'\d+', year_str)[0])

        # 월 추출
        month_str = re.search(r'\d+월', text_str)[0]
        month = int(re.search(r'\d+', month_str)[0])

        # 일 추출
        day_str = re.search(r'\d+일', text_str)[0]
        day = int(re.search(r'\d+', day_str)[0])

        # 요일 추출
        week = re.search(r'\d+년 \d+월 \d+일 (일|월|화|수|목|금|토)요일 (?:오후|오전|낮)?\s?(\d{1,2})\s?[시:]\s?(\d{0,2})\s?(?:분)?', text_str)

        # 시간 추출
        time_matches = re.findall(r'(?:오후|오전|낮)?\s?(\d{1,2})\s?[시:]\s?(\d{0,2})\s?(?:분)?', text_str)[0]
        hour = int(time_matches[0])
        if '오후' in text_list:
            hour += 12
        minute = int(time_matches[1]) if time_matches[1] else 0



        print(place_list)
        print(name_list)
        print("----------")
        print("년:", year, type(year))
        print("월:", month, type(month))
        print("일:", day, type(day))
        print("요일:", week, type(week))
        print(hour,":",minute)

        pass


