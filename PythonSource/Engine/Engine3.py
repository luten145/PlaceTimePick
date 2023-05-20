# TODO : Cleaning...
from tkinter import *
import operator
import re
from konlpy.tag import Kkma
from PythonSource.Util import LogUtil as logUtil
from PythonSource.Util import AddressDB
from PythonSource.Util import StringUtil
import PythonSource.Util.DicApi as dicApi
from PythonSource.UI import UIMain
from PythonSource.UI.UIListener import UIEventListener

TAG = "Engine3"


class Address:
    def __init__(self):
        self.name = "NAME"
        self.line = []
        self.count = 0


class Window:
    def __init__(self):
        self.line = 0
        self.count = 0


class Engine3:

    def __init__(self, uiManager: UIEventListener):
        self.mUIManager = uiManager
        self.addressDB = AddressDB.AddressDB()
        self.windows = []
        pass

    def jsonHandler(self, data):  # data is json File

        self.mUIManager.onSetDataEvent(1, "ENGINE3")  # UI Test
        logUtil.Log(TAG, "JsonHandler")  # Log

        textList = self.getTextList(data)

        logUtil.Log(TAG, "Original Text")
        for i in textList:
            logUtil.Log(TAG, i)

        self.dataHandler(textList)
        pass

    def getTextList(self, raw):
        textList = raw["task_result"]["text"]  # json 파일 내에 text 키의 값 리스트
        combinedText = "".join(textList)  # 하나의 리스트로 만들기
        text = [combinedText]  # 결합된 텍스트
        textList = str(text).split('\\n')  # 한줄씩 나눠서 리스트로 만들기
        textStr = str(text).replace("\\n", " ")  # 줄바꿈문자를 공백으로 변환 (줄바꿈 에러 개선)
        return textList

    def dataHandler(self, textList):

        cityList = self.getCity(textList)  # 시 후보군
        for i in cityList:
            logUtil.Log(TAG,  "CITY : " + str(i.__dict__))




    pass

    def getCity(self, textList:list): # 데이터에서 시를 찾습니다.
        tag = "getCity"

        regionPattern = self.addressDB.getAdressList()[0]  # All city list

        res = []
        c = 0
        for i in textList:
            for j in regionPattern:
                num = StringUtil.countPattern(i, j)
                if num > 0:
                    p = False
                    t = False

                    for g in self.windows:
                        if g.line == c:
                            g.count +=1
                            t = True
                    if t is False:
                        o = Window()
                        o.line = c
                        o.count +=1
                        self.windows.append(o)



                    for k in res:
                        if(k.name == j):
                            k.line.append(c)
                            k.count += 1
                            p = True

                    if p is False :
                        a = Address()
                        a.name = j
                        a.count += 1
                        a.line.append(c)
                        res.append(a)

            c+=1
        la = sorted(res,key=lambda res : res.count,reverse=True)

        districtList = self.getDistrict(textList, la)  # 시,군,구를 후보군
        for i in districtList:
            logUtil.Log(TAG,  "DISTRICT : " + str(i.__dict__))

        townList = self.getTown(textList, districtList)  # 동 후보군
        for i in townList:
            logUtil.Log(TAG,  "TOWN : " + str(i.__dict__))

        roadList = self.getRoad(textList, districtList)  # 도로명 후보군
        for i in roadList:
            logUtil.Log(TAG,  "ROAD : " + str(i.__dict__))

        numList = self.getNum_2(textList,roadList)

        for i in numList:
            logUtil.Log(TAG,  "NUM : " + str(i))

        return la



    def getDistrict(self, textList, cityList):
        tag = "getDistrict"

        # 데이터에서 시를 찾습니다.
        if cityList:
            key = cityList[0].name
            logUtil.Log(tag, str(key))
            regionPattern = self.addressDB.getAdressList(key, AddressDB.FIND_CITY, AddressDB.FIND_DISTRICT)[0]
        else:
            a = self.addressDB.getAdressList()[0]  # All city list
            regionPattern = []
            for i in a:
                b= self.addressDB.getAdressList(i, AddressDB.FIND_CITY, AddressDB.FIND_DISTRICT)[0]
                for j in b:
                    regionPattern.append(j)

        #logUtil.Log(tag, regionPattern)

        res = []
        c = 0
        for i in textList:
            if i is '':
                continue
            for j in regionPattern:
                if j == '':
                    continue
                num = StringUtil.countPattern(i, j)
                if num > 0:
                    t = False

                    for g in self.windows:
                        if g.line == c:
                            g.count +=1
                            t = True
                    if t is False:
                        o = Window()
                        o.line = c
                        o.count +=1
                        self.windows.append(o)

                    p = False
                    for k in res:
                        if(k.name == j):
                            k.line.append(c)
                            k.count += 1
                            p = True

                    if p is False :
                        a = Address()
                        a.name = j
                        a.count += 1
                        a.line.append(c)
                        res.append(a)

            c+=1


        return sorted(res,key=lambda res : res.count,reverse=True)

    def getTown(self, textList, cityList):
        tag = " getTown"

        # 데이터에서 시를 찾습니다.
        if cityList:
            key = cityList[0].name
            logUtil.Log(tag, str(key))
            regionPattern = self.addressDB.getAdressList(key, AddressDB.FIND_DISTRICT, AddressDB.FIND_TOWN)[0]
        else:
            a = self.addressDB.getAdressList()[0]  # All city list
            regionPattern = []
            for i in a:
                b= self.addressDB.getAdressList(i, AddressDB.FIND_DISTRICT, AddressDB.FIND_TOWN)[0]
                for j in b:
                    regionPattern.append(j)


        res = []
        c = 0
        for i in textList:
            for j in regionPattern:
                if j == '':
                    continue
                num = StringUtil.countPattern(i, j)
                if num > 0:
                    t = False
                    for g in self.windows:
                        if g.line == c:
                            g.count +=1
                            t = True
                    if t is False:
                        o = Window()
                        o.line = c
                        o.count +=1
                        self.windows.append(o)

                    p = False
                    for k in res:
                        if(k.name == j):
                            k.line.append(c)
                            k.count += 1
                            p = True

                    if p is False :
                        a = Address()
                        a.name = j
                        a.count += 1
                        a.line.append(c)
                        res.append(a)

            c+=1

        return sorted(res,key=lambda res : res.count,reverse=True)

    def getRoad(self, textList, cityList):
        tag = " getRoad"

        # 데이터에서 시를 찾습니다.
        if cityList:
            key = cityList[0].name
            logUtil.Log(tag, str(key))
            regionPattern = self.addressDB.getAdressList(key, AddressDB.FIND_DISTRICT, AddressDB.FIND_ROAD)[1]
        else:
            a = self.addressDB.getAdressList()[0]  # All city list
            regionPattern = []
            for i in a:
                b= self.addressDB.getAdressList(i, AddressDB.FIND_DISTRICT, AddressDB.FIND_ROAD)[1]
                for j in b:
                    regionPattern.append(j)


        res = []
        c = 0
        for i in textList:
            for j in regionPattern:
                num = StringUtil.countPattern(i, j)
                if num > 0:
                    t = False

                    for g in self.windows:
                        if g.line == c:
                            g.count +=1
                            t = True
                    if t is False:
                        o = Window()
                        o.line = c
                        o.count +=1
                        self.windows.append(o)

                    p = False
                    for k in res:
                        if(k.name == j):
                            k.line.append(c)
                            k.count += 1
                            p = True

                    if p is False :
                        a = Address()
                        a.name = j
                        a.count += 1
                        a.line.append(c)
                        res.append(a)

            c+=1

        return sorted(res,key=lambda res : res.count,reverse=True)

    def extract_numbers(self,text):
        return re.findall(r'\d+(?:-\d+)?', text)

    def getNum_2(self, textList, cityList):

        tag = "getNum_2"

        self.windows = sorted(self.windows,key= lambda windows : windows.count , reverse = True)


        res = []
        c = 0
        l = self.windows[0].line
        numbers = self.extract_numbers(textList[l])
        print(numbers)
        return numbers

    def getRoadNum(self, textList, cityList):
        tag = "getRoadNum"

        # 데이터에서 시를 찾습니다.
        if cityList:
            key = cityList[0].name
            logUtil.Log(tag, str(key))
            regionPattern = self.addressDB.getAdressList(key, AddressDB.FIND_ROAD, AddressDB.FIND_ROAD_NUM)[0]
        else:
            a = self.addressDB.getAdressList()[0]  # All city list
            regionPattern = []
            for i in a:
                b= self.addressDB.getAdressList(i, AddressDB.FIND_ROAD, AddressDB.FIND_ROAD_NUM)[0]
                for j in b:
                    regionPattern.append(j)




        res = []
        c = 0
        for i in textList:
            for j in regionPattern:
                num = StringUtil.countPattern(i, j)
                if num > 0 and c == self.windows[0].line:
                    p = False
                    for k in res:
                        if(k.name == j):
                            k.line.append(c)
                            k.count += 1
                            p = True

                    if p is False :
                        a = Address()
                        a.name = j
                        a.count += 1
                        a.line.append(c)
                        res.append(a)

            c+=1


        return sorted(res,key=lambda res : res.count,reverse=True)

    def getNum(self, textList, cityList):

        tag = "getNum"
        self.windows = sorted(self.windows,key= lambda windows : windows.count , reverse = True)
        for o in self.windows:
            logUtil.Log(tag,o.__dict__)

        # 데이터에서 시를 찾습니다.
        if cityList:
            key = cityList[0].name
            logUtil.Log(tag, str(key))
            regionPattern = self.addressDB.getAdressList(key, AddressDB.FIND_ROAD, AddressDB.FIND_NUM)[0]

        else :
            a = self.addressDB.getAdressList()[0]  # All city list
            regionPattern = []
            for i in a:
                b = self.addressDB.getAdressList(i, AddressDB.FIND_ROAD, AddressDB.FIND_NUM)[0]
                for j in b:
                    regionPattern.append(j)



        res = []
        c = 0
        for i in textList:
            for j in regionPattern:
                num = StringUtil.countPattern(i, j)
                if num > 0 and c == self.windows[0].line:
                    p = False
                    for k in res:
                        if(k.name == j):
                            k.line.append(c)
                            k.count += 1
                            p = True

                    if p is False :
                        a = Address()
                        a.name = j
                        a.count += 1
                        a.line.append(c)
                        res.append(a)

            c+=1

        return sorted(res,key=lambda res : res.count,reverse=True)