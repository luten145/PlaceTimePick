import re
from tkinter import *
from konlpy.tag import Kkma
import PythonSource.Util.DicApi as dicApi
from PythonSource.Util import LogUtil as logUtil
from PythonSource.UI.UIListener import UIEventListener
from PythonSource.UI import UIMain
from PythonSource.Util import AddressDB
from PythonSource.Util import StringUtil

TAG = "Engine2"

class Engine2:
    # TODO : migration to individual file
    def __init__(self,uiManager : UIEventListener):
        self.mUIManager = uiManager
        pass

    def jsonHandler(self,data):
        self.mUIManager.onSetDataEvent(1,"HELLO ENGINE2")
        logUtil.Log(TAG,"dataIN!!")
        # data is json File
        # json 파일 내에 text 키의 값들만 읽어서 하나의 리스트로 만들기
        text_list = data["task_result"]["text"]
        combined_text = "".join(text_list)
        text = [combined_text]

        text_list = str(text).split('\\n')
        text_str2 = str(text).replace("\\n","")
        text_str3 = str(text_str2).replace(":","")
        text_str = str(text_str3).replace(" ","")

        print(text_list)
        print(text_str)
        print()
        print()

        """regionStr = "서울 부산 대구 인천 광주 대전 울산 경기 강원 충청 충북 충남 전라 전북 전남 경상 경북 경남 제주 세종"
        textPos = kkma.pos(regionStr)                   # 형태소를 분리하고 품사 부착
        posWord = [word for (word, tag) in textPos]   # textPos 단어들만 추출
        posTag = [tag for (word, tag) in textPos]     # textPos 태그들만 추출
        nouns = [(word, tag) for (word, tag) in textPos if tag.startswith('N')]        # 형태소 분리, 품사 부착 후 명사들만 추출
        nounsWord = [word for (word, tag) in nouns]     # posTag 단어들만 추출
        print('textPos: ', textPos)
        print('posWord: ', posWord[0])
        print('posTag: ', posTag[0])
        print('nouns:', nouns)
        print('nounsWord:', nounsWord)

        for i in nounsWord:
            nounDic = dicApi.wordSearch(i)
            if(nounDic != -1):
                logUtil.Log(TAG, "-------------------")
                logUtil.Log(TAG, "검색한 단어 : " + nounDic.word)
                logUtil.Log(TAG, "단어의 뜻 : " + nounDic.definition)
                logUtil.Log(TAG, "-------------------")
            else:
                logUtil.Log(TAG, "사전에서 단어를 찾을 수 없습니다!")"""


        """placeKey = ["서울","부산","대구","인천","광주","대전","울산","경기","강원","충청","전라","경상","제주","세종","홀","웨딩","장례","층"]
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
                    break"""

        """regionPattern = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "경기", "강원", "충청", "충북", "충남", "전라","전북", "전남", "경상", "경북", "경남", "제주", "세종"]
        region = [item for item in text_list if any(re.search(p, item) for p in regionPattern)]
        regionList = region[0].split()
        region0 = regionList[0]
        region1 = regionList[1]
        region2 = regionList[2]
        region3 = str(' '.join(regionList[3:5]))"""




        """regionPattern1 = r"([가-힣]+(시|도)(\s[가-힣]+(시|도))?\s+[가-힣]+(시|군|구)(\s+[가-힣]+(읍|면|동))?(\s+[가-힣\d]+(로|길))?( \d+(번지|))?)"
        regionTuple = re.findall(regionPattern1, text_str)
        print("regionTuple: ", regionTuple, type(regionTuple))
        regionFind = regionTuple[0]
        print("regionFind: ", regionFind, type(regionFind))
        regionSelect = regionFind[0]
        print("regionSelect: ", regionSelect, type(regionSelect))
        regionList = regionSelect.split()
        print("regionList: ", regionList, type(regionList))

        if('도' in regionList[0]):
            region0 = regionList[0]
            region1 = str(' '.join(regionList[1:3]))
            if((regionList[3])[-1] != '로'):
                region2 = regionList[3]
                region3 = regionList[4]
                region4 = regionList[-1]
            else:
                region2 = 'None'
                region3 = regionList[3]
                region4 = regionList[4]
        else:
            region0 = regionList[0]
            region1 = regionList[1]
            if((regionList[2])[-1] != '로'):
                region2 = regionList[2]
                if((regionList[3])[-1] == '로'):
                    region3 = regionList[3]
                    region4 = regionList[4]
                else:
                    region3 = 'None'
                    region4 = regionList[3]
            else:
                region2 = 'None'
                region3 = regionList[2]
                region4 = regionList[3]

        placePattern = ["홀", "웨딩", "층", "장례"]
        place = [item for item in text_list if any(re.search(p, item) for p in placePattern)]"""

        #초기화
        year, month, day, week, hour, minute = 0, 0, 0, 0, 0, 0

        # 년월일 추출 - 2021년 10월 21일 or 2021.10.21 or 2021/10/21 or 2021-10-21
        ymdPattern = r'(\d{4})(?:년|\.|/|-)(\d{1,2})(?:월|\.|/|-)(\d{1,2})?일?'
        ymdStr = re.search(ymdPattern, text_str)
        if ymdStr:
            ymdEndIndex = ymdStr.end()
            ymdNextText = text_str[ymdEndIndex:]
            year = int(ymdStr.group(1))
            month = int(ymdStr.group(2))
            day = int(ymdStr.group(3))

        # 요일 추출 - 월요일 or (월) or 월
        #weekPattern = r"(월요일|화요일|수요일|목요일|금요일|토요일|일요일|\((월|화|수|목|금|토|일)\)|월|화|수|목|금|토|일)"
        weekPattern = r"\(?(월요일|화요일|수요일|목요일|금요일|토요일|일요일|월|화|수|목|금|토|일)\)?"
        weekStr = re.search(weekPattern, ymdNextText)
        if weekStr:
            weekEndIndex = weekStr.end()
            weekNextText = text_str[weekEndIndex:]
            week = weekStr.group(1)[0]

        # 시간 추출 - (오전 or 오후 or 낮) + 10시 20분 or 10:20
        timePattern = r"(?:오후|오전|낮)?(\d{1,2})(?::|시)(\d{1,2})?(?:분)?"
        timeStr = re.search(timePattern, weekNextText)
        if timeStr:
            hour = int(timeStr.group(1))
            if '오후' in str(timeStr):
                hour += 12
            minute = int(timeStr.group(2) or 0)

        #print("장소: ", place_list)
        """print("시/도: ", region0, type(region0))
        print("시/군/구: ", region1, type(region1))
        print("읍/면: ", region2, type(region2))
        print("도로명: ", region3, type(region3))
        print("건물번호: ", region4, type(region4))
        #print(name_list)
        print("장소: ", place)"""
        print("----------")
        print("년:", year, type(year))
        print("월:", month, type(month))
        print("일:", day, type(day))
        print("요일:", week, type(week))
        print("시: ", hour, type(hour))
        print("분: ", minute, type(minute))

        """self.mUIManager.onSetDataEvent(UIMain.PLACE_SI,region0)
        self.mUIManager.onSetDataEvent(UIMain.PLACE_GU,region1)
        self.mUIManager.onSetDataEvent(UIMain.PLACE_DONG,region2)
        self.mUIManager.onSetDataEvent(UIMain.PLACE_STREET,region3)
        self.mUIManager.onSetDataEvent(UIMain.PLACE_NUM,region4)"""
        self.mUIManager.onSetDataEvent(UIMain.TIME_YEAR,str(year))
        self.mUIManager.onSetDataEvent(UIMain.TIME_MONTH,str(month))
        self.mUIManager.onSetDataEvent(UIMain.TIME_DATE,str(day))
        self.mUIManager.onSetDataEvent(UIMain.TIME_WEEK,str(week))
        self.mUIManager.onSetDataEvent(UIMain.TIME_HOUR,str(hour))
        self.mUIManager.onSetDataEvent(UIMain.TIME_MIN,str(minute))

