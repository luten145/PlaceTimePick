import operator
import re
from tkinter import *
from konlpy.tag import Kkma
import PythonSource.Util.DicApi as dicApi
from PythonSource.Util import LogUtil as logUtil
from PythonSource.UI.UIListener import UIEventListener
from PythonSource.UI import UIMain
from PythonSource.Util import AddressDB
from PythonSource.Util import StringUtil

TAG = "Engine3"

class Address:
    def __init__(self):
        self.name = "NAME"
        self.line = []
        self.count = 0

class Engine3:

    def __init__(self, uiManager: UIEventListener):
        self.mUIManager = uiManager
        self.addressDB = AddressDB.AddressDB()
        pass

    def jsonHandler(self, data):  # data is json File

        self.mUIManager.onSetDataEvent(1, "ENGINE3")
        logUtil.Log(TAG, "JsonHandler")

        textList = data["task_result"]["text"]  # json 파일 내에 text 키의 값 리스트
        combinedText = "".join(textList)  # 하나의 리스트로 만들기

        logUtil.Log(TAG, "Original Text")


        text = [combinedText]  # 결합된 텍스트
        textList = str(text).split('\\n')  # 한줄씩 나눠서 리스트로 만들기
        textStr = str(text).replace("\\n", " ")  # 줄바꿈문자를 공백으로 변환 (줄바꿈 에러 개선)

        for i in textList:
            logUtil.Log(TAG, i)
        logUtil.Log(TAG, textStr)

        # -----------------------

        cityList = self.getCity(textList)  # 시 후보군
        logUtil.Log(TAG,  "CITY : " + str(cityList))

        districtList = self.getDistrict(textList, cityList)  # 시,군,구를 후보군
        logUtil.Log(TAG, "DISTRICT : " +str(districtList))

        townList = self.getTown(textList, districtList)  # 도로명 후보군
        logUtil.Log(TAG, "TOWN : " +str(townList))

        roadNumList = self.getRoadNum(textList, townList)  # 건물번호 후보군
        logUtil.Log(TAG, "RoadNum : " +str(roadNumList))

        numList = self.getNum(textList,roadNumList)  # 건물번호 후보군
        logUtil.Log(TAG, "Num : " +str(numList))



        # 경우 나누기
        # 1. 데이터가 없는경우 -> 데이터 없음 뒤에 데이터 찾은 뒤 검색

        # 2. 데이터가 여러개인 경우 -> 정렬 순위별로 검색
        # 2-1 순위가 똑같은 경우 -> 둘다 검색

        # 3. 데이터가 한개인 경우 -> 확정

        #  데이터에서


        placePattern = ["홀", "웨딩", "층", "장례"]
        place = [item for item in textList if any(re.search(p, item) for p in placePattern)]

        # 초기화
        year, month, day, week, hour, minute = 0, 0, 0, 0, 0, 0

        # 년월일 추출 - 2021년 10월 21일 or 2021.10.21 or 2021/10/21 or 2021-10-21
        ymdPattern = r'(\d{4})(?:년|\.|/|-)\s?(\d{1,2})(?:월|\.|/|-)\s?(\d{1,2})?일?'
        ymdStr = re.search(ymdPattern, textStr)
        if ymdStr:
            ymdEndIndex = ymdStr.end()
            ymdNextText = textStr[ymdEndIndex:]
            year = int(ymdStr.group(1))
            month = int(ymdStr.group(2))
            day = int(ymdStr.group(3))

        # 요일 추출 - 월요일 or (월) or 월
        # weekPattern = r"(월요일|화요일|수요일|목요일|금요일|토요일|일요일|\((월|화|수|목|금|토|일)\)|월|화|수|목|금|토|일)"
        weekPattern = r"\(?(월요일|화요일|수요일|목요일|금요일|토요일|일요일|월|화|수|목|금|토|일)\)?"
        weekStr = re.search(weekPattern, ymdNextText)
        if weekStr:
            weekEndIndex = weekStr.end()
            weekNextText = textStr[weekEndIndex:]
            week = weekStr.group(1)[0]

        # 시간 추출 - (오전 or 오후 or 낮) + 10시 20분 or 10:20
        timePattern = r"(?:오후|오전|낮)?\s?(\d{1,2})(?::|시\s*)(\d{1,2})?(?:분)?"
        timeStr = re.search(timePattern, weekNextText)
        if timeStr:
            hour = int(timeStr.group(1))
            if '오후' in str(timeStr):
                hour += 12
            minute = int(timeStr.group(2) or 0)

        # logUtil.Log(TAG,"장소: ", place_list)

        '''
        logUtil.Log(TAG,"지역: ", region, type(region))
        logUtil.Log(TAG,"시/도: ", region0, type(region0))
        logUtil.Log(TAG,"시/군/구: ", region1, type(region1))
        logUtil.Log(TAG,"읍/면: ", region2, type(region2))
        logUtil.Log(TAG,"도로명: ", region3, type(region3))
        '''
        # logUtil.Log(TAG,name_list)
        logUtil.Log(TAG,"장소: "+ str(place))
        # logUtil.Log(TAG,"----------")
        # logUtil.Log(TAG,"년:"+ year)
        # logUtil.Log(TAG,"월:"+ month)
        # logUtil.Log(TAG,"일:"+ day)
        # logUtil.Log(TAG,"요일:"+ week)
        # logUtil.Log(TAG,"시: "+hour)
        # logUtil.Log(TAG,"분: "+ minute)

        '''
        self.mUIManager.onSetDataEvent(UIMain.PLACE_SI,region0)
        self.mUIManager.onSetDataEvent(UIMain.PLACE_GU,region1)
        self.mUIManager.onSetDataEvent(UIMain.PLACE_DONG,region2)
        self.mUIManager.onSetDataEvent(UIMain.PLACE_STREET,region3)
        '''
        self.mUIManager.onSetDataEvent(UIMain.TIME_YEAR, str(year))
        self.mUIManager.onSetDataEvent(UIMain.TIME_MONTH, str(month))
        self.mUIManager.onSetDataEvent(UIMain.TIME_DATE, str(day))
        self.mUIManager.onSetDataEvent(UIMain.TIME_HOUR, str(hour))
        # self.mUIManager.onSetDataEvent(UIMain.TIME_MIN,str(minute))

        pass

    def getCity(self, textList): # 데이터에서 시를 찾습니다.
        tag = "getCity"




        regionPattern = self.addressDB.getAdressList()[0]  # All city list

        res = []
        c = 0
        for i in textList:
            for j in regionPattern:
                num = StringUtil.countPattern(i, j)
                if num > 0:
                    a = Address()
                    a.name = j
                    a.count += 1
                    a.line.append(c)
                    res.append(a)
            c+=1

        return k

    def getDistrict(self, textList, cityList):
        tag = "getDistrict"

        # 데이터에서 시를 찾습니다.
        key, value = cityList.__getitem__(0)
        logUtil.Log(tag, str(key))

        ll = self.addressDB.getAdressList(key, AddressDB.FIND_CITY, AddressDB.FIND_DISTRICT)

        logUtil.Log(tag, ll)
        regionPattern = ll[0]




        dd = ['경기', 0, 1]



        for i in textList:
            for j in regionPattern:
                num = StringUtil.countPattern(i, j)
                if num > 0: 
                    if res.get(j)[0] is None:
                        res[j] = 1
                    else:
                        res[j] += 1

        k = sorted(res.items(),key=operator.itemgetter(1), reverse=True)
        logUtil.Log(tag, k)

        mkey, mvalue = k.__getitem__(0)
        self.mUIManager.onSetDataEvent(UIMain.PLACE_GU, mkey)

        return k

    def getTown(self, textList, cityList):
        tag = " getTown"


        key, value = cityList.__getitem__(0)
        logUtil.Log(tag, str(key))

        ll = self.addressDB.getAdressList(key, AddressDB.FIND_DISTRICT, AddressDB.FIND_ROAD)

        logUtil.Log(tag, ll)
        regionPattern = ll[0]

        res = {}
        for i in textList:
            for j in regionPattern:
                num = StringUtil.countPattern(i, j)
                if num > 0:
                    d = res.get(j)
                    if (d is None):
                        res[j] = 1
                    else:
                        res[j] += 1

        k = sorted(res.items(),key=operator.itemgetter(1), reverse=True)
        logUtil.Log(tag, k)
        mkey, mvalue = k.__getitem__(0)
        self.mUIManager.onSetDataEvent(UIMain.PLACE_STREET, mkey)

        return k


    def getRoadNum(self, textList, cityList):
        tag = "getRoadNum"


        key, value = cityList.__getitem__(0)
        logUtil.Log(tag, str(key))

        ll = self.addressDB.getAdressList(key, AddressDB.FIND_ROAD, AddressDB.FIND_ROAD_NUM)

        logUtil.Log(tag, ll)
        regionPattern = ll[0]

        res = {}
        for i in textList:
            for j in regionPattern:
                num = StringUtil.countPattern(i, j)
                if num > 0:
                    d = res.get(j)
                    if (d is None):
                        res[j] = 1
                    else:
                        res[j] += 1

        k = sorted(res.items(),key=operator.itemgetter(1), reverse=True)
        logUtil.Log(tag, k)
        mkey, mvalue = k.__getitem__(0)
        self.mUIManager.onSetDataEvent(UIMain.PLACE_STREET, mkey)

        return k

    def getNum(self, textList, cityList):
        tag = "getNum"


        key, value = cityList.__getitem__(0)
        logUtil.Log(tag, str(key))

        ll = self.addressDB.getAdressList(key, AddressDB.FIND_ROAD, AddressDB.FIND_NUM)

        logUtil.Log(tag, ll)
        regionPattern = ll[0]

        res = {}
        for i in textList:
            for j in regionPattern:
                num = StringUtil.countPattern(i, j)
                if num > 0:
                    d = res.get(j)
                    if (d is None):
                        res[j] = 1
                    else:
                        res[j] += 1

        k = sorted(res.items(),key=operator.itemgetter(1), reverse=True)
        logUtil.Log(tag, k)
        mkey, mvalue = k.__getitem__(0)
        self.mUIManager.onSetDataEvent(UIMain.PLACE_STREET, mkey)

        return k