import re
from tkinter import *
from konlpy.tag import Kkma
import PythonSource.Util.DicApi as dicApi
from PythonSource.Util import LogUtil as logUtil
from PythonSource.UI.UIListener import UIEventListener
from PythonSource.UI import UIMain
from PythonSource.Engine.Engine1 import Engine1
from PythonSource.Engine.Engine3 import Engine3
TAG = "MainManager"

class MainEngine:

    TAG = "MainEngine"

    def __init__(self,uiManager:UIEventListener):
        self.mUIManager = uiManager
        pass

    def tkinterHandler(self, data):
        Engine1(self.mUIManager).tkinterHandler(data)
        pass

    def jsonHandler(self,data):
        #j = Engine1(self.mUIManager)
        #j.jsonHandler(data)
        #Engine2(self.mUIManager).jsonHandler(data)
        Engine3(self.mUIManager).jsonHandler(data)
        pass

    pass


class Engine2:
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

        text_list=str(text).split('\\n')
        text_str=str(text).replace("\\n"," ")
        print(text_list)
        print(text_str)
        print()
        print()

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

        regionPattern = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "경기", "강원", "충청", "충북", "충남", "전라","전북", "전남", "경상", "경북", "경남", "제주", "세종"]
        region = [item for item in text_list if any(re.search(p, item) for p in regionPattern)]
        regionList = region[0].split()
        region0 = regionList[0]
        region1 = regionList[1]
        region2 = regionList[2]
        region3 = str(' '.join(regionList[3:5]))

        placePattern = ["홀", "웨딩", "층", "장례"]
        place = [item for item in text_list if any(re.search(p, item) for p in placePattern)]

        #초기화
        year, month, day, week, hour, minute = 0, 0, 0, 0, 0, 0

        # 년월일 추출 - 2021년 10월 21일 or 2021.10.21 or 2021/10/21 or 2021-10-21
        ymdPattern = r'(\d{4})(?:년|\.|/|-)\s?(\d{1,2})(?:월|\.|/|-)\s?(\d{1,2})?일?'
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
        timePattern = r"(?:오후|오전|낮)?\s?(\d{1,2})(?::|시\s*)(\d{1,2})?(?:분)?"
        timeStr = re.search(timePattern, weekNextText)
        if timeStr:
            hour = int(timeStr.group(1))
            if '오후' in str(timeStr):
                hour += 12
            minute = int(timeStr.group(2) or 0)

        #print("장소: ", place_list)

        print("지역: ", region, type(region))
        print("시/도: ", region0, type(region0))
        print("시/군/구: ", region1, type(region1))
        print("읍/면: ", region2, type(region2))
        print("도로명: ", region3, type(region3))
        #print(name_list)
        print("장소: ", place)
        print("----------")
        print("년:", year, type(year))
        print("월:", month, type(month))
        print("일:", day, type(day))
        print("요일:", week, type(week))
        print("시: ", hour, type(hour))
        print("분: ", minute, type(minute))

        self.mUIManager.onSetDataEvent(UIMain.PLACE_SI,region0)
        self.mUIManager.onSetDataEvent(UIMain.PLACE_GU,region1)
        self.mUIManager.onSetDataEvent(UIMain.PLACE_DONG,region2)
        self.mUIManager.onSetDataEvent(UIMain.PLACE_STREET,region3)
        self.mUIManager.onSetDataEvent(UIMain.TIME_YEAR,str(year))
        self.mUIManager.onSetDataEvent(UIMain.TIME_MONTH,str(month))
        self.mUIManager.onSetDataEvent(UIMain.TIME_DATE,str(day))
        self.mUIManager.onSetDataEvent(UIMain.TIME_HOUR,str(hour))
        self.mUIManager.onSetDataEvent(UIMain.TIME_MIN,str(minute))

        pass