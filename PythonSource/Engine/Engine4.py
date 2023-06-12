import re
from PythonSource.Util.LogUtil import *
from PythonSource.Util import AddressDB
from PythonSource.Util import StringUtil
from PythonSource.Util import AddressApi
from PythonSource.UI.UIListener import UIEventListener

# 가중치 정보
CITY_NODE_SCORE = 8
DIST_NODE_SCORE = 8
ROAD_NODE_SCORE = 8
NUM_NODE_SCORE = 8
SEARCH_BONUS_KEYWORD = ["홀", "웨딩", "장례", "병원","호텔"]
SEARCH_BONUS_SCORE = 50
SEARCH_COMPLETE_SCORE = 16
SEARCH_SIMILARITY_MULTIPLE = 100

class Address:
    def __init__(self,name,count):
        self.name = name  # 키워드
        self.line = []  # 발견된 라인 위치
        self.count = count  # 중복 횟수
        self.score = 0  # 점수
        self.result = ""  # 도로명주소
        self.resultOld = ""  # 지번주소
        self.postNum = ""  # 우편번호
        self.end = False  # 트리의 노트가 End일 경우 노드의 끝을 의미함


class Addr():
    def __init__(self):
        self.cities = []  # City 노드

class City(Address):
    def __init__(self,name,count):
        super().__init__(name,count)
        self.dists = []  # Dist 노드

class Dist(Address): #시 군 구
    def __init__(self, name, count):
        super().__init__(name,count)
        self.roads = []  # Road 노드

class Road(Address):
    def __init__(self,name,count):
        super().__init__(name,count)
        self.nums = []  # 숫자 노드

class Num(Address):
    def __init__(self,name,count):
        super().__init__(name,count)

class Build(Address):
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
        self.count = 0

class ScoreTable():
    def __init__(self,address,score,road = "",old ="",postNum = ""):
        self.address = address
        self.score = score
        self.result = road
        self.resultOld = old
        self.postNum = postNum

class SendData():
    def __init__(self):
        self.addressTable = []
        self.otherInfo = []



TAG = "Engine4"

class Engine4:

    def __init__(self, uiManager: UIEventListener):
        self.mUIManager = uiManager
        self.tree = Addr()
        self.addressDB = AddressDB.AddressDB()
        self.addrScore = []
        self.buildList = []
        self.addressApi = AddressApi.AddressApi()
        self.ENABLE_HARD_SEARCH = False

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

        for i in textList:
            print(i)

        self.getBuilding(textList)

        for i in self.buildList:
            Log(TAG,i.__dict__)

        # 각각의 함수는 트리를 처리합니다.
        self.cityHandler(textList)
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

        self.sortTree(textList)

        self.addrScore = sorted(self.addrScore,key= lambda  ad :ad.score,reverse= True)
        hard = True
        for i in self.addrScore:
            Log(TAG,str(i.__dict__))
            if i.result != '':
                hard = False

        if hard:
            self.ENABLE_HARD_SEARCH = True
            Log(TAG,"Hard Search Enabled")
            self.sortTree(textList)
            self.addrScore = sorted(self.addrScore,key= lambda  ad :ad.score,reverse= True)
            for i in self.addrScore:
                Log(TAG,str(i.__dict__))


        o = SendData()
        o.addressTable = self.addrScore

        for i in self.buildList:
            for j in i.line:
                o.otherInfo.append(textList[j])
                Log(TAG,"추가정보 : "+str(textList[j]))
        self.mUIManager.onSetDataEvent(0,o)

        # 상위 5개만
        l = 0
        for i in self.addrScore:
            Log(TAG,str(i.__dict__))
            if l > 5:
                break
            l+=1

        # 결과 출력
        Log(TAG,"결과 \n뽑아낸 주소 : "+str(self.addrScore[0].address)+"\n도로명주소 : "+str(self.addrScore[0].result)+"\n지번주소 : "+str(self.addrScore[0].resultOld)+"\n우편번호 : "+str(self.addrScore[0].postNum))
        print("추가정보 : ",end = "")
        for i in self.buildList:
            for j in i.line:
                print(str(textList[j]),end = " ")


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

    def sortTree(self,textList):
        # 점수 산정 방식
        # 일반 점수 : count 순 , 트리 존재 함 : 8점

        # 모든 경우의 수를 출력합니다.
        for city in self.tree.cities:
            city.score = city.count + CITY_NODE_SCORE

            if(city.name != "None"):
                cityName = self.addressDB.getAdressList(Find=city.name, AddressNum=AddressDB.ROAD_FIND_CITY, AddressGet=AddressDB.ROAD_FIND_CITY)[1][0]
            else :
                cityName = ""

            cAddrStr = str(cityName)
            Log(TAG,cAddrStr+" Score : "+ str(city.score))
            cS = ScoreTable(cAddrStr,city.score)
            self.addrScore.append(cS)

            for dist in city.dists:
                dist.score = city.score + dist.count + DIST_NODE_SCORE

                distName = dist.name
                dAddrStr = str(cityName) + " " + str(distName)
                Log(TAG,"   " + dAddrStr+" Score : "+ str(dist.score))

                if dist.end and self.ENABLE_HARD_SEARCH:
                    r = self.addressApi.wordSearch(dAddrStr)
                    resScore = 0
                    resAddr = ""
                    resAddrOld = ""
                    resPos = 0

                    for i in range (0,r.resultCount):
                        lScore = 0
                        a = StringUtil.similarity(r.word,r.addr[i])*SEARCH_SIMILARITY_MULTIPLE
                        b = StringUtil.similarity(r.word,r.addrOld[i])*SEARCH_SIMILARITY_MULTIPLE

                        # 특정 키워드 추가점수
                        for j in SEARCH_BONUS_KEYWORD:
                            if StringUtil.containsSubstring(r.addr[i],j) or StringUtil.containsSubstring(r.addrOld[i],j):
                                lScore += SEARCH_BONUS_SCORE

                        if a>b:
                            lScore = a
                        else:
                            lScore = b

                        if lScore > resScore:
                            resScore = lScore
                            resAddr = r.addr[i]
                            resAddrOld = r.addrOld[i]
                            resPos = r.postNum[i]

                    dist.score += resScore
                    dist.result = resAddr
                    dist.resultOld = resAddrOld
                    dist.postNum = resPos

                    dist.score += SEARCH_COMPLETE_SCORE


                dS = ScoreTable(dAddrStr,dist.score)
                dS.result = dist.result
                dS.resultOld = dist.resultOld
                dS.postNum = dist.postNum
                self.addrScore.append(dS)



                for road in dist.roads:
                    roadName = road.name
                    road.score = city.score+dist.score+road.count + ROAD_NODE_SCORE
                    rAddrStr = str(cityName) + " " + str(distName) + " " +str(roadName)
                    Log(TAG,"   " +"   " + rAddrStr+" Score : "+ str(road.score))

                    if road.end and self.ENABLE_HARD_SEARCH:
                        r = self.addressApi.wordSearch(rAddrStr)
                        resScore = 0
                        resAddr = ""
                        resAddrOld = ""
                        resPos = 0

                        for i in range (0,r.resultCount):
                            lScore = 0
                            a = StringUtil.similarity(r.word,r.addr[i])*SEARCH_SIMILARITY_MULTIPLE
                            b = StringUtil.similarity(r.word,r.addrOld[i])*SEARCH_SIMILARITY_MULTIPLE

                            # 특정 키워드 추가점수
                            for j in SEARCH_BONUS_KEYWORD:
                                if StringUtil.containsSubstring(r.addr[i],j) or StringUtil.containsSubstring(r.addrOld[i],j):
                                    lScore += SEARCH_BONUS_SCORE

                            if a>b:
                                lScore = a
                            else:
                                lScore = b

                            if lScore > resScore:
                                resScore = lScore
                                resAddr = r.addr[i]
                                resAddrOld = r.addrOld[i]
                                resPos = r.postNum[i]

                        road.score += resScore
                        road.result = resAddr
                        road.resultOld = resAddrOld
                        road.postNum = resPos

                        road.score += SEARCH_COMPLETE_SCORE


                    rS = ScoreTable(dAddrStr,dist.score)
                    rS.result = dist.result
                    rS.resultOld = dist.resultOld
                    rS.postNum = dist.postNum
                    self.addrScore.append(rS)

                    for num in road.nums:
                        if self.ENABLE_HARD_SEARCH == False and num.end == True:
                            # 고급검색이 꺼져있으면 엔드 플래그가 있는것을 검색하지 않고 넘깁니다.
                            break
                        num.score = city.score+dist.score+road.score+num.count + NUM_NODE_SCORE
                        nAddrStr = str(cityName) + " " + str(distName) + " " +str(roadName) +" " + num.name
                        r = self.addressApi.wordSearch(nAddrStr)
                        resScore = 0
                        resAddr = ""
                        resAddrOld = ""
                        resPos = 0

                        for i in range(0,r.resultCount):
                            lScore = 0
                            a = StringUtil.similarity(r.word,r.addr[i])*SEARCH_SIMILARITY_MULTIPLE
                            b = StringUtil.similarity(r.word,r.addrOld[i])*SEARCH_SIMILARITY_MULTIPLE

                            # 특정 키워드 추가점수
                            for j in SEARCH_BONUS_KEYWORD:
                                if StringUtil.containsSubstring(r.addr[i],j) or StringUtil.containsSubstring(r.addrOld[i],j):
                                    lScore += SEARCH_BONUS_SCORE

                            if a>b:
                                lScore = a
                            else:
                                lScore = b

                            if lScore > resScore:
                                resScore = lScore
                                resAddr = r.addr[i]
                                resAddrOld = r.addrOld[i]
                                resPos = r.postNum[i]

                        num.score += resScore
                        num.result = resAddr
                        num.resultOld = resAddrOld
                        num.postNum = resPos

                        num.score += SEARCH_COMPLETE_SCORE

                        Log(TAG,"   " +"   " +"   " + nAddrStr+" Score : "+ str(num.score)+" S Result : "+str(num.result))
                        nS = ScoreTable(nAddrStr,num.score)
                        nS.result = num.result
                        nS.resultOld = num.resultOld
                        nS.postNum = num.postNum
                        self.addrScore.append(nS)
        pass

    def extract_words(self,text, keyword):
        words = text.split()
        result = []
        for word in words:
            if keyword in word:
                result.append(word)
        return result

    def getBuilding(self, textList):
        placePattern = ["홀", "웨딩", "장례", "병원", "층"]

        currentLine = 0
        for textLine in textList:
            wo = []
            for i in placePattern:
                wo+=self.extract_words(textLine,i)

            wordComplete = False
            for word in wo:
                for s in self.buildList:
                    if(word == s.name):
                        s.count+=1
                        s.line.append(currentLine)
                        wordComplete = True
                if not wordComplete:
                    b = Build(word,1)
                    b.line.append(currentLine)
                    self.buildList.append(b)

            currentLine+=1

        pass

    def cityHandler(self, textList):
        tag = "getCity"

        regionList = self.addressDB.getAdressList()[0]  # Get all city list
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
                            break

                    if not cityComplete:
                        city = City(regionKey,num) # 새 객체 생성
                        city.line.append(currentLine)
                        self.tree.cities.append(city) # 트리에 City 리스트에 추가
            currentLine+=1

        if len (self.tree.cities) == 0:  # 키를 찾지 못한 경우 전체 City키를 트리에 추가합니다.
            for regionKey in regionList:
                city = City(regionKey,0) # 새 객체 생성
                self.tree.cities.append(city) # 트리에 City 리스트에 추가

        # 트리self.tree.cities.append(city) # 트리에 City 리스트에 추가
        # 를 정렬합니다. (기준 : 카운트)
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
            if(city.name != "None"):
                key = self.addressDB.getAdressList(Find=city.name, AddressNum=AddressDB.ROAD_FIND_CITY, AddressGet=AddressDB.ROAD_FIND_CITY)[1][0]
            else:
                key = "None"
            regionList = self.addressDB.getAdressList(key, AddressDB.ROAD_FIND_CITY, AddressDB.ROAD_FIND_DISTRICT)[0]
            currentLine = 0

            if(city.name == "None"):
                Log(tag,"Error! : Cannot find city -> Use all city list")
                a = self.addressDB.getAdressList()[0]  # All city list
                for i in a:
                    b= self.addressDB.getAdressList(i, AddressDB.ROAD_FIND_CITY, AddressDB.ROAD_FIND_DISTRICT)[0]
                    for j in b:
                        regionList.append(j)


            # 윈도우에서 두번 나와야 함
            for textLine in textList:
                for regionKey in regionList:
                    num = StringUtil.countPattern(textLine, regionKey)
                    if num > 0:  # 같은것이 있습니다.

                        distComplete = False
                        for dist in city.dists: # 트리 안에 있는 Dist 리스트 탐색
                            if(dist.name == regionKey):  # 현재 비교하는 지역이 이미 있는경우
                                dist.count += num  # 카운트 증가 (Scoring)
                                dist.line.append(currentLine)  # 발견된 라인 저장 (윈도우 탐색용)
                                distComplete = True

                        if not distComplete:
                            mDist = Dist(regionKey,num) # 새 객체 생성
                            mDist.line.append(currentLine)
                            dist = Dist(regionKey,num) # 새 객체 생성
                            dist.line.append(currentLine)
                            for i in self.buildList:
                                for j in i.line:
                                    a = StringUtil.generateCombinations(textList[j])
                                    for b in a:

                                        if not StringUtil.containsSubstring(b,dist.name) and not StringUtil.containsSubstring(b,city.name):
                                            n = Road(b,1)
                                            n.end = True
                                            dist.roads.append(n)
                                    pass
                            city.dists.append(dist) # 현재 City 트리에 Dist 리스트에 추가
                            city.dists.append(mDist) # 현재 City 트리에 Dist 리스트에 추가

                currentLine+=1

                # 트리를 정렬합니다. (기준 : 카운트)
            city.dists = sorted(city.dists, key = lambda dist: dist.count,reverse=True)
    pass


    def getRoad(self, textList):
        tag = "getRoad"

        # 모든 트리에 대하여 탐색을 시도합니다.
        # 도로명 먼저 탐색합니다.
        for city in self.tree.cities: # city 트리입니다.
            for dist in city.dists: # dict 트리입니다.

                if dist.end:
                    continue

                # 줄 리스트를 만들고 정렬 합니다. (줄 대상 트리 내 윈도우)
                winList = []

                lineList = []
                lineList += city.line
                lineList += dist.line

                Log(TAG,lineList)


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
                    Log(tag,i.line)
                    s = StrData(textList[i.line],i.line)
                    mText.append(s)



                key = dist.name
                Log(tag,key)

                regionList = self.addressDB.getAdressList(key, AddressDB.ROAD_FIND_DISTRICT, AddressDB.ROAD_FIND_ROAD)[0]
                regionList += self.addressDB.getAdressList(key, AddressDB.OLD_FIND_DISTRICT, AddressDB.OLD_FIND_TOWN,AddressDB.OLD_ADDRESS)[0]

                currentLine = 0

                # 윈도우에서 두번 나와야 함

                for textLine in mText:
                    mStack = []
                    for regionKey in regionList:
                        num = StringUtil.countPattern(textLine.str, regionKey)
                        if num > 0:  # 같은것이 있습니다.

                            # 트리 내에 정보와 겹칩니까?
                            if regionKey == dist.name or regionKey == city.name:
                                # 일단 내부 스택에 넣습니다.
                                stackCom = False
                                for stack in mStack:
                                    if stack.str == regionKey and stack.count > 0:
                                        stackCom = True # 통과
                                        pass

                                if not stackCom:
                                    s = StrData(regionKey,textLine.line)
                                    s.count = 1
                                    mStack.append(s)
                                    break


                            roadComplete = False
                            for road in dist.roads: # 트리 안에 있는 Dist 리스트 탐색
                                if(road.name == regionKey):  # 현재 비교하는 지역이 이미 있는경우
                                    road.count += num  # 카운트 증가 (Scoring)
                                    road.line.append(textLine.line)  # 발견된 라인 저장 (윈도우 탐색용)
                                    roadComplete = True;

                            if not roadComplete:
                                mRoad = Road(regionKey,num) # 새 객체 생성
                                mRoad.line.append(textLine.line)
                                road = Road(regionKey,num) # 새 객체 생성
                                road.line.append(textLine.line)
                                for i in self.buildList:
                                    for j in i.line:
                                        a = StringUtil.generateCombinations(textList[j])
                                        for b in a:
                                            n = Num(b,1)
                                            n.end = True
                                            road.nums.append(n)
                                        pass
                                dist.roads.append(road) # 현재 City 트리에 Dist 리스트에 추가
                                dist.roads.append(mRoad) # 현재 City 트리에 Dist 리스트에 추가



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
                    if road.end:
                        continue

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