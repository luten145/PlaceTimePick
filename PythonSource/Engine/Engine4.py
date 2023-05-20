import re
from PythonSource.Util.LogUtil import *
from PythonSource.Util import AddressDB
from PythonSource.Util import StringUtil
from PythonSource.Util import AddressApi

class Address:
    def __init__(self,name,count):
        self.name = name
        self.line = []
        self.count = count
        self.score = 0

class Addr():
    def __init__(self):
        self.cities = []

class City(Address):
    def __init__(self,name,count):
        super().__init__(name,count)
        self.dists = []

class Dist(Address):
    def __init__(self, name, count):
        super().__init__(name,count)
        self.roads = []

class Road(Address):
    def __init__(self,name,count):
        super().__init__(name,count)
        self.nums = []

class Num(Address):
    def __init__(self,name,count):
        super().__init__(name,count)

class Window:
    def __init__(self,line,count):
        self.line = line
        self.count = count

class StrData:
    def __init__(self,str,line):
        self.str = str
        self.line = line

class ScoreTable():
    def __init__(self,address,score):
        self.address = address
        self.score = score


TAG = "Engine4"

class Engine4:

    def __init__(self):
        self.tree = Addr()
        self.addressDB = AddressDB.AddressDB()
        self.addrScore = []

    def jsonHandler(self, data):  # data is json File
        Log(TAG, "JsonHandler")  # Log
        self.dataHandler(self.getTextList(data))
        pass

    def getTextList(self, raw):
        textList = raw["task_result"]["text"]  # json 파일 내에 text 키의 값 리스트
        combinedText = "".join(textList)  # 하나의 리스트로 만들기
        text = [combinedText]  # 결합된 텍스트
        return str(text).split('\\n')  # 한줄씩 나눠서 리스트로 만들기

    def dataHandler(self, textList):
        self.getCity(textList)
        Log(TAG,"Start")
        self.printTree()
        Log(TAG,"End")
        self.getDistrict(textList)

        Log(TAG,"Start")
        self.printTree()
        Log(TAG,"End")

        self.getRoad(textList)

        Log(TAG,"Start")
        self.printTree()
        Log(TAG,"End")

        self.getNum_2(textList)

        Log(TAG,"Start")
        self.printTree()
        Log(TAG,"End")

        self.sortTree()

        self.addrScore = sorted(self.addrScore,key= lambda  ad :ad.score,reverse= True)
        for i in self.addrScore:
            Log(TAG,str(i.__dict__))


    pass

    def printTree(self):
        for city in self.tree.cities:
            Log(TAG,city.__dict__)

            for dist in city.dists:
                Log(TAG,"   "+city.name+str(dist.__dict__))

                for road in dist.roads:
                    Log(TAG,"   "+"   "+dist.name+str(road.__dict__))

                    for num in road.nums:
                        Log(TAG,"   "+"   "+"   "+road.name+str(num.__dict__))

        pass

    def sortTree(self):
        # 점수 산정 방식
        # 일반 점수 : count 순 , 트리 존재 함 : 8점

        # 모든 경우의 수를 출력합니다.
        for city in self.tree.cities:


            city.score = city.count + 8*1

            if(city.name != "None"):
                cityName = self.addressDB.getAdressList(Find=city.name, AddressNum=AddressDB.FIND_CITY, AddressGet=AddressDB.FIND_CITY)[1][0]
            else :
                cityName = ""

            cAddrStr = str(cityName)
            Log(TAG,cAddrStr+" Score : "+ str(city.score))
            cS = ScoreTable(cAddrStr,city.score)
            self.addrScore.append(cS)

            for dist in city.dists:
                dist.score = city.score+dist.count+ 8*1

                distName = dist.name
                dAddrStr = str(cityName) + " " + str(distName)
                Log(TAG,"   " + dAddrStr+" Score : "+ str(dist.score))
                dS = ScoreTable(dAddrStr,dist.score)
                self.addrScore.append(dS)

                for road in dist.roads:
                    roadName = road.name
                    road.score = city.score+dist.score+road.count + 8*2
                    rAddrStr = str(cityName) + " " + str(distName) + " " +str(roadName)
                    Log(TAG,"   " +"   " + rAddrStr+" Score : "+ str(road.score))
                    rS = ScoreTable(rAddrStr,road.score)
                    self.addrScore.append(rS)

                    for num in road.nums:
                        num.score = city.score+dist.score+road.score+num.count + 8*3
                        nAddrStr = str(cityName) + " " + str(distName) + " " +str(roadName) +" " + num.name
                        r = AddressApi.wordSearch(nAddrStr)
                        if r.resultCount > 0:
                            num.score += 16
                            pass

                        Log(TAG,"   " +"   " +"   " + nAddrStr+" Score : "+ str(num.score))
                        nS = ScoreTable(nAddrStr,num.score)
                        self.addrScore.append(nS)




        pass


    def getCity(self, textList):
        tag = "getCity"

        regionList = self.addressDB.getAdressList()[0]  # All City List
        currentLine = 0
        for textLine in textList:
            for regionKey in regionList:
                num = StringUtil.countPattern(textLine, regionKey)
                if num > 0:  # 같은것이 있습니다.
                    cityComplete = False;
                    for city in self.tree.cities: # 기존 City 리스트 탐색
                        if(city.name == regionKey):  # 현재 비교하는 지역이 이미 있는경우
                            city.count += num  # 카운트 증가 (Scoring)
                            city.line.append(currentLine)  # 발견괸 라인 저장 (윈도우 탐색용)
                            cityComplete = True;

                    if not cityComplete:
                        city = City(regionKey,num) # 새 객체 생성
                        city.line.append(currentLine)
                        self.tree.cities.append(city) # 트리에 City 리스트에 추가
            currentLine+=1

        # 트리를 정렬합니다. (기준 : 카운트)
        self.tree.cities = sorted(self.tree.cities, key = lambda city : city.count,reverse=True)

        pass

    def getDistrict(self, textList):
        tag = "getDistrict"

        # 모든 트리에 대하여 탐색을 시도합니다.

        if len(self.tree.cities) == 0:
            a = City("None",0)
            self.tree.cities.append(a)
            pass

        for city in self.tree.cities:
            regionList = []
            key = city.name
            regionList = self.addressDB.getAdressList(key, AddressDB.FIND_CITY, AddressDB.FIND_DISTRICT)[0]
            currentLine = 0

            if(city.name == "None"):
                Log(tag,"Error! : Cannot find city -> Use all city list")
                a = self.addressDB.getAdressList()[0]  # All city list
                for i in a:
                    b= self.addressDB.getAdressList(i, AddressDB.FIND_CITY, AddressDB.FIND_DISTRICT)[0]
                    for j in b:
                        regionList.append(j)



            for textLine in textList:
                for regionKey in regionList:
                    num = StringUtil.countPattern(textLine, regionKey)
                    if num > 0:  # 같은것이 있습니다.

                        distComplete = False
                        for dist in city.dists: # 트리 안에 있는 Dist 리스트 탐색
                            if(dist.name == regionKey):  # 현재 비교하는 지역이 이미 있는경우
                                dist.count += num  # 카운트 증가 (Scoring)
                                dist.line.append(currentLine)  # 발견된 라인 저장 (윈도우 탐색용)
                                distComplete = True;

                        if not distComplete:
                            dist = Dist(regionKey,num) # 새 객체 생성
                            dist.line.append(currentLine)
                            city.dists.append(dist) # 현재 City 트리에 Dist 리스트에 추가
                currentLine+=1

                # 트리를 정렬합니다. (기준 : 카운트)
            city.dists = sorted(city.dists, key = lambda dist: dist.count,reverse=True)
    pass


    def getRoad(self, textList):
        tag = "getRoad"

        # 모든 트리에 대하여 탐색을 시도합니다.
        for city in self.tree.cities: # city 트리입니다.
            for dist in city.dists: # dict 트리입니다.

                # 줄 리스트를 만들고 정렬 합니다. (줄 대상 트리 내 윈도우)
                winList = []

                lineList = []
                lineList += city.line
                lineList += dist.line


                for line in lineList:
                    winComplete = False
                    for win in winList: # Win List 탐색
                        if win.line == line:
                            win.count +=1
                            winComplete = True

                    if not winComplete:
                        win = Window(line,1)
                        winList.append(win)

                winList = sorted(winList,key = lambda  win : win.count,reverse=True)

                mText = []

                for i in winList:
                    s = StrData(textList[i.line],i.line)
                    mText.append(s)

                key = dist.name
                Log(tag,key)
                regionList = self.addressDB.getAdressList(key, AddressDB.FIND_DISTRICT, AddressDB.FIND_ROAD)[0]

                currentLine = 0

                for textLine in mText:
                    for regionKey in regionList:
                        num = StringUtil.countPattern(textLine.str, regionKey)
                        if num > 0:  # 같은것이 있습니다.


                            roadComplete = False
                            for road in dist.roads: # 트리 안에 있는 Dist 리스트 탐색
                                if(road.name == regionKey):  # 현재 비교하는 지역이 이미 있는경우
                                    road.count += num  # 카운트 증가 (Scoring)
                                    road.line.append(textLine.line)  # 발견된 라인 저장 (윈도우 탐색용)
                                    roadComplete = True;

                            if not roadComplete:
                                road = Road(regionKey,num) # 새 객체 생성
                                road.line.append(textLine.line)
                                dist.roads.append(road) # 현재 City 트리에 Dist 리스트에 추가

                    currentLine+=1

                    # 트리를 정렬합니다. (기준 : 카운트)
                dist.roads = sorted(dist.roads, key = lambda road: road.count,reverse=True)

    def extract_numbers(self,text):
        return re.findall(r'\d+(?:-\d+)?', text)

    def getNum_2(self, textList):
        tag = "getNum_2"


        # 모든 트리에 대하여 탐색을 시도합니다.
        for city in self.tree.cities: # city 트리입니다.
            for dist in city.dists: # dist 트리입니다.
                for road in dist.roads: # road 트리입니다.

                    # 줄 리스트를 만들고 정렬 합니다. (줄 대상 트리 내 윈도우)
                    winList = []

                    lineList = []
                    lineList += city.line
                    lineList += dist.line
                    lineList += road.line

                    for line in lineList:
                        winComplete = False
                        for win in winList: # Win List 탐색
                            if win.line == line:
                                win.count +=1
                                winComplete = True

                        if not winComplete:
                            win = Window(line,1)
                            winList.append(win)

                    winList = sorted(winList,key = lambda  win : win.count,reverse=True)
                    searchLine = winList[0].line
                    numbers = self.extract_numbers(textList[searchLine])


                    for line in numbers:
                        numComplete = False
                        for num in road.nums:
                            if num == line:
                                num.count += 1
                                num.line = searchLine
                                numComplete = True

                        if not numComplete:
                            n = Num(line,1)
                            n.line = searchLine
                            road.nums.append(n)


                    road.nums = sorted(road.nums, key = lambda num: num.count,reverse=True)