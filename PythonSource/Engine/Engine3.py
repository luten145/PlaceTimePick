# TODO : Cleaning...
from tkinter import *
import operator
import re
from konlpy.tag import Kkma
from PythonSource.Util import Log as logUtil
from PythonSource.Util import AddressDB
from PythonSource.Util import StringUtil
import PythonSource.Util.DicApi as dicApi
from PythonSource.UI import UIMain
from PythonSource.UI.UIListener import UIEventListener
from PythonSource.Util import AddressApi

TAG = "Engine3"


class Address:
    def __init__(self):
        self.city = "CITY"
        self.dist = "DIST"
        self.road = "ROAD"
        self.num = "NUM"

class AddressPiece:
    def __init__(self,name,count):
        self.name = name
        self.line = []
        self.count = count


class Window:
    def __init__(self,line,count):
        self.line = line
        self.count = 0



class Engine3:

    def __init__(self, uiManager: UIEventListener):
        self.mUIManager = uiManager
        self.addressDB = AddressDB.AddressDB()
        self.windows = []

        self.address = Address()
        self.city = []
        self.district = []
        self.road = []


        pass

    def jsonHandler(self, data):  # data is json File

        self.mUIManager.onSetDataEvent(1, "ENGINE3")  # UI Test
        logUtil.LogUtil_old(TAG, "JsonHandler")  # Log

        textList = self.getTextList(data)

        logUtil.LogUtil_old(TAG, "Original Text")
        for i in textList:
            logUtil.LogUtil_old(TAG, i)

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

        self.city = self.getCity(textList)

        for i in self.city:
            logUtil.LogUtil_old(TAG, "CITY : " + str(i.__dict__))



        districtList = self.getDistrict(textList, self.city)  # 시,군,구를 후보군
        for i in districtList:
            logUtil.LogUtil_old(TAG, "DISTRICT : " + str(i.__dict__))

        #townList = self.getTown(textList, districtList)  # 동 후보군
        #for i in townList:
        #    logUtil.Log(TAG,  "TOWN : " + str(i.__dict__))

        roadList = self.getRoad(textList, districtList)  # 도로명 후보군
        for i in roadList:
            logUtil.LogUtil_old(TAG, "ROAD : " + str(i.__dict__))

        numList = self.getNum_2(textList,roadList)

        for i in numList:
            logUtil.LogUtil_old(TAG, "NUM : " + str(i))




    pass

    def getValidation(self):
        sc = ""
        sc += str(self.address.city)
        sc += " "
        sc += str(self.address.dist)
        sc += " "
        sc += str(self.address.road)
        sc += " "
        sc += str(self.address.num)

        r = AddressApi.wordSearch(sc)
        logUtil.LogUtil_old(TAG, str(r.__dict__))
        return r.addr != ""





    def getCity(self, textList:list):
        tag = "getCity"
        regionPattern = self.addressDB.getAddressList()[0]  # All City List
        res = []; c = 0
        for i in textList:
            for j in regionPattern:
                num = StringUtil.countPattern(i, j)
                if num > 0:
                    p,t = False , False

                    for g in self.windows:
                        if g.line == c:
                            g.count += num
                            t = True

                    if t is False:
                        self.windows.append(Window(c,num))

                    for k in res:
                        if(k.name == j):
                            k.line.append(c)
                            k.count += num
                            p = True

                    if p is False :
                        a = AddressPiece(j, num)
                        a.line.append(c)
                        res.append(a)
            c+=1
        return sorted(res,key=lambda res : res.count,reverse=True)



    def getDistrict(self, textList, cityList):
        tag = "getDistrict"

        # 데이터에서 시를 찾습니다.
        q = 0
        key = ""
        t = len(cityList)
        if t == 1:
            key = cityList[q].name
            logUtil.LogUtil_old(tag, str(key))
            regionPattern = self.addressDB.getAddressList(key, AddressDB.FIND_CITY, AddressDB.FIND_DISTRICT)[0]
            logUtil.LogUtil_old(tag, "Info : 1 city was found.")
        elif t > 1:
            key = cityList[q].name
            logUtil.LogUtil_old(tag, str(key))
            regionPattern = self.addressDB.getAddressList(key, AddressDB.FIND_CITY, AddressDB.FIND_DISTRICT)[0]
            logUtil.LogUtil_old(tag, "Info : Multiple cities were searched.")
        else:
            logUtil.LogUtil_old(tag, "Error! : Cannot find city -> Use all city list")
            a = self.addressDB.getAddressList()[0]  # All city list
            regionPattern = []
            for i in a:
                b= self.addressDB.getAddressList(i, AddressDB.FIND_CITY, AddressDB.FIND_DISTRICT)[0]
                for j in b:
                    regionPattern.append(j)

        self.address.city = key

        #logUtil.Log(tag, regionPattern)

        while True:
            res = []; c = 0
            for i in textList:
                for j in regionPattern:
                    num = StringUtil.countPattern(i, j)
                    if num > 0:
                        p,t = False , False

                        for g in self.windows:
                            if g.line == c:
                                g.count += num
                                t = True

                        if t is False:
                            self.windows.append(Window(c,num))

                        for k in res:
                            if(k.name == j):
                                k.line.append(c)
                                k.count += num
                                p = True

                        if p is False :
                            a = AddressPiece(j, num)
                            a.line.append(c)
                            res.append(a)
                c+=1
            if len(res) < 0 and t > q:
                q+=1
                key = cityList[q].name
                logUtil.LogUtil_old(tag, str(key))
                regionPattern = self.addressDB.getAddressList(key, AddressDB.FIND_CITY, AddressDB.FIND_DISTRICT)[0]
                logUtil.LogUtil_old(tag, "Info : Multiple cities were searched.")

            else:
                break;
        return sorted(res,key=lambda res : res.count,reverse=True)

    def getTown(self, textList, cityList):
        tag = " getTown"

        # 데이터에서 시를 찾습니다.
        key = ""
        t = len(cityList)
        if t == 1:
            key = cityList[0].name
            logUtil.LogUtil_old(tag, str(key))
            regionPattern = self.addressDB.getAddressList(key, AddressDB.FIND_DISTRICT, AddressDB.FIND_TOWN)[0]
            logUtil.LogUtil_old(tag, "Info : 1 district was found.")
        elif t > 1:
            logUtil.LogUtil_old(tag, "Info : Multiple district were searched.")
        else:
            logUtil.LogUtil_old(tag, "Error! : Cannot find district -> Use all district list")
            a = self.addressDB.getAddressList()[0]  # All city list
            regionPattern = []
            for i in a:
                b= self.addressDB.getAddressList(i, AddressDB.FIND_DISTRICT, AddressDB.FIND_TOWN)[0]
                for j in b:
                    regionPattern.append(j)

        self.address.dist = key

        res = []; c = 0
        for i in textList:
            for j in regionPattern:
                num = StringUtil.countPattern(i, j)
                if num > 0:
                    p,t = False , False

                    for g in self.windows:
                        if g.line == c:
                            g.count += num
                            t = True

                    if t is False:
                        self.windows.append(Window(c,num))

                    for k in res:
                        if(k.name == j):
                            k.line.append(c)
                            k.count += num
                            p = True

                    if p is False :
                        a = AddressPiece(j, num)
                        a.line.append(c)
                        res.append(a)
            c+=1
        return sorted(res,key=lambda res : res.count,reverse=True)

    def getRoad(self, textList, cityList):
        tag = " getRoad"


        # 데이터에서 시를 찾습니다.
        key = ""
        t = len(cityList)
        if t == 1:
            key = cityList[0].name
            logUtil.LogUtil_old(tag, str(key))
            regionPattern = self.addressDB.getAddressList(key, AddressDB.FIND_DISTRICT, AddressDB.FIND_ROAD)[0]
            logUtil.LogUtil_old(tag, "Info : 1 district was found.")
        elif t > 1:
            key = cityList[0].name
            logUtil.LogUtil_old(tag, str(key))
            regionPattern = self.addressDB.getAddressList(key, AddressDB.FIND_DISTRICT, AddressDB.FIND_ROAD)[0]
            logUtil.LogUtil_old(tag, "Info : Multiple district were searched.")
        else:
            logUtil.LogUtil_old(tag, "Error! : Cannot find district -> Use all district list")
            a = self.addressDB.getAddressList()[0]  # All city list
            regionPattern = []
            for i in a:
                b= self.addressDB.getAddressList(i, AddressDB.FIND_DISTRICT, AddressDB.FIND_ROAD)[0]
                for j in b:
                    regionPattern.append(j)

        self.address.dist = key

        res = []; c = 0
        for i in textList:
            for j in regionPattern:
                num = StringUtil.countPattern(i, j)
                if num > 0:
                    p,t = False , False

                    for g in self.windows:
                        if g.line == c:
                            g.count += num
                            t = True

                    if t is False:
                        self.windows.append(Window(c,num))

                    for k in res:
                        if(k.name == j):
                            k.line.append(c)
                            k.count += num
                            p = True

                    if p is False :
                        a = AddressPiece(j, num)
                        a.line.append(c)
                        res.append(a)
            c+=1
        return sorted(res,key=lambda res : res.count,reverse=True)

    def extract_numbers(self,text):
        return re.findall(r'\d+(?:-\d+)?', text)

    def getNum_2(self, textList, cityList):
        tag = "getNum_2"

        key = ""
        t = len(cityList)
        # 데이터에서 시를 찾습니다.
        if t == 1:
            key = cityList[0].name
            logUtil.LogUtil_old(tag, str(key))
            logUtil.LogUtil_old(tag, "Info : 1 road was found.")
        elif t > 1:
            key = cityList[0].name
            logUtil.LogUtil_old(tag, "Info : Multiple road were searched.")
        else:
            logUtil.LogUtil_old(tag, "Error! : Cannot find road -> Search End")

        self.address.road = key
        self.windows = sorted(self.windows,key= lambda windows : windows.count , reverse = True)


        l = self.windows[0].line
        numbers = self.extract_numbers(textList[l])
        print(numbers)


        key = ""
        # 데이터에서 시를 찾습니다.
        if numList:
            key = str(numList[0])

        self.address.num = key

        logUtil.LogUtil_old(TAG, str(self.address.__dict__))
        print(self.getValidation())

        return numbers