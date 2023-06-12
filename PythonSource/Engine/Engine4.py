import time
from PythonSource.UI.UIListener import UIEventListener
from PythonSource.Util import Log
from PythonSource.Util import AddressDB
from PythonSource.Util import StringUtil
from PythonSource.Util import AddressApi

PLACE_KEYWORD = ["홀", "웨딩", "장례", "병원", "층"]

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
        self.nodes = []  # City 노드

    def addNode(self,node):
        self.nodes.append(node)

    def getTree(self) -> []:
        return self.nodes


class Window:
    def __init__(self,str,line,count):
        self.str = str
        self.line = line
        self.count = count


class ScoreTable():
    def __init__(self,address,score,road = "",old ="",postNum = ""):
        self.address = address
        self.score = score
        self.result = road
        self.resultOld = old
        self.postNum = postNum


class SendData:
    def __init__(self):
        self.addressTable = []
        self.otherInfo = []


TAG = "Engine4"


class Engine4:

    def __init__(self, uiManager: UIEventListener):
        Log.i(TAG, "Engine4 Start")
        self.textList = None
        self.mUIManager = uiManager
        self.tree = Address("root",1)
        self.addressDB = AddressDB.AddressDB()
        self.addrScore = []
        self.additionalList = Address("Additional", 1)
        self.addressApi = AddressApi.AddressApi()
        self.ENABLE_HARD_SEARCH = False

    def jsonHandler(self, data):  # Data is json File
        Log.d(TAG, "JsonHandler")
        self.textList = StringUtil.getTextList(data)
        self.dataHandler(self.textList)

    def dataHandler(self, textList):
        startTime = time.time()
        self.additionalInfoHandler(textList)  # Get additional information
        self.cityHandler(textList)
        self.districtHandler(textList)
        self.roadHandler(textList)
        self.numberHandler(textList)
        treeSearchTime = time.time() - startTime
        self.sortTree()
        self.addrScore = sorted(self.addrScore,key= lambda  ad :ad.score,reverse= True)
        hard = True
        for i in self.addrScore:
            Log.d(TAG,str(i.__dict__))
            if i.result != '':
                hard = False
        if hard:
            self.ENABLE_HARD_SEARCH = True
            Log.i(TAG,"Hard Search Enabled")
            self.sortTree()
            self.addrScore = sorted(self.addrScore,key= lambda  ad :ad.score,reverse= True)
            for i in self.addrScore:
                Log.d(TAG,str(i.__dict__))
        treeAnalyzeTime = time.time() - startTime
        l = 0
        for i in self.addrScore:
            Log.i(TAG,str(i.__dict__))
            if l > 5:
                break
            l += 1
        Log.i(TAG,"결과 \n뽑아낸 주소 : "+str(self.addrScore[0].address)+"\n도로명주소 : "+str(self.addrScore[0].result)+"\n지번주소 : "+str(self.addrScore[0].resultOld)+"\n우편번호 : "+str(self.addrScore[0].postNum))
        print("추가정보 : ",end = "")
        for i in self.additionalList.getTree():
            for j in i.line:
                print(str(textList[j]),end = " ")
        print()
        Log.i(TAG, str("트리 탐색 시간 : " + str(treeSearchTime) + "초"))
        Log.i(TAG, str("트리 분석 시간 : " + str(treeAnalyzeTime) + "초"))

    def additionalInfoHandler(self, textList):
        currentLine = 0
        for textLine in textList:
            words = []
            for key in PLACE_KEYWORD:
                words += StringUtil.extractWords(textLine, key)
            for word in words:
                self.addressTreeHandler(self.additionalList, word, currentLine, 1)
            currentLine += 1
        pass

    def addressTreeHandler(self, tree: Address, key, line, count):
        nodeComplete = False
        for node in tree.getTree():  # 기존 City 리스트 탐색
            if node.name == key:  # 현재 비교하는 지역이 이미 있는경우
                node.count += count  # 카운트 증가 (Scoring)
                node.line.append(line)  # 발견된 라인 저장 (윈도우 탐색용)
                nodeComplete = True
                break
        if not nodeComplete:
            node = Address(key, count)
            node.line.append(line)
            tree.addNode(node)
        return nodeComplete

    def cityHandler(self, textList):
        regionList = self.addressDB.getAddressList()[0]  # Get all city list
        currentLine = 0
        for textLine in textList:
            for key in regionList:
                num = StringUtil.countPattern(textLine, key)
                if num > 0:
                    key = self.addressDB.getAddressList(Find=key, AddressNum=AddressDB.ROAD_FIND_CITY, AddressGet=AddressDB.ROAD_FIND_CITY)[1][0]
                    self.addressTreeHandler(self.tree, key, currentLine, num)
            currentLine += 1

        if len(self.tree.getTree()) == 0:  # 키를 찾지 못한 경우 전체 City 키를 트리에 추가합니다.
            for key in regionList:
                self.tree.addNode(Address(key, 0))

    def districtHandler(self, textList):
        for city in self.tree.getTree():
            regionList = self.addressDB.getAddressList(city.name, AddressDB.ROAD_FIND_CITY, AddressDB.ROAD_FIND_DISTRICT)[0]
            Log.d(TAG,regionList)
            currentLine = 0
            for textLine in textList:
                for regionKey in regionList:
                    num = StringUtil.countPattern(textLine, regionKey)
                    if num > 0:
                        if not self.addressTreeHandler(city, regionKey, currentLine, num):
                            dist = Address(regionKey, num)
                            dist.line.append(currentLine)
                            for additional in self.additionalList.getTree():
                                for line in additional.line:
                                    additionalList = StringUtil.generateCombinations(textList[line])  # 모든 조합
                                    for case in additionalList: # 추가정보에 시군구 단어가 없는 경우의 수만
                                        if not StringUtil.containsSubstring(case, dist.name) and not StringUtil.containsSubstring(case, city.name):
                                            n = Address(case, 1)
                                            n.end = True
                                            dist.addNode(n)
                            city.addNode(dist)  # 현재 City 트리에 Dist 리스트에 추가
                currentLine += 1

    def roadHandler(self, textList):
        for city in self.tree.getTree():
            for dist in city.getTree():
                if dist.end:
                    continue
                lineList = []
                lineList += city.line
                lineList += dist.line

                regionList = self.addressDB.getAddressList(dist.name, AddressDB.ROAD_FIND_DISTRICT, AddressDB.ROAD_FIND_ROAD)[0]
                regionList += self.addressDB.getAddressList(dist.name, AddressDB.OLD_FIND_DISTRICT, AddressDB.OLD_FIND_TOWN, AddressDB.OLD_ADDRESS)[0]

                currentLine = 0
                for textLine in self.getWinList(textList,lineList):  # 윈도우에서 두번 나와야 함
                    for regionKey in regionList:
                        num = StringUtil.countPattern(textLine.str, regionKey)
                        if num > 0:
                            if not self.addressTreeHandler(dist, regionKey, textLine.line, 1):
                                road = Address(regionKey, num)  # 새 객체 생성
                                road.line.append(textLine.line)
                                for i in self.additionalList.getTree():
                                    for j in i.line:
                                        a = StringUtil.generateCombinations(textList[j])
                                        for b in a:
                                            n = Address(b, 1)
                                            n.end = True
                                            road.addNode(n)
                                dist.addNode(road)  # 현재 City 트리에 Dist 리스트에 추가
                    currentLine += 1

    def getWinList(self,textList,lineList):
        winList = []
        for line in lineList:
            winComplete = False
            for win in winList:  # Win List 탐색
                if win.line == line:
                    win.count += 1
                    winComplete = True
            if not winComplete:
                win = Window(textList[line], line, 1)
                winList.append(win)
        return winList

    def numberHandler(self, textList):
        for city in self.tree.getTree():
            for dist in city.getTree():
                for road in dist.getTree():
                    if road.end:
                        continue
                    lineList = []
                    lineList += city.line
                    lineList += dist.line
                    lineList += road.line
                    searchLine = sorted(self.getWinList(textList,lineList),key = lambda  win : win.count,reverse=True)[0].line
                    for line in StringUtil.extractNumbers(textList[searchLine]):
                        self.addressTreeHandler(road, line, searchLine, 1)

    def printTree(self):
        Log.d(TAG,"---  Start  ---")
        for city in self.tree.getTree():
            Log.d(TAG, city.__dict__)

            for dist in city.getTree():
                Log.d(TAG, "   "+city.name+str(dist.__dict__))

                for road in dist.getTree():
                    Log.d(TAG, "   "+"   "+dist.name+str(road.__dict__))

                    for num in road.getTree():
                        Log.d(TAG, "   "+"   "+"   "+road.name+str(num.__dict__))
        Log.d(TAG, "---   End   ---")
        pass

    def getSecrchResult(self,node,address,table):
        r = self.addressApi.wordSearch(address)
        resScore = 0
        resAddr = ""
        resAddrOld = ""
        resPos = 0

        for i in range(0,r.resultCount):
            lScore = 0
            a = StringUtil.getSimilarity(r.word, r.addr[i]) * SEARCH_SIMILARITY_MULTIPLE
            b = StringUtil.getSimilarity(r.word, r.addrOld[i]) * SEARCH_SIMILARITY_MULTIPLE

            for j in SEARCH_BONUS_KEYWORD:  # 특정 키워드 추가점수
                if StringUtil.containsSubstring(r.addr[i],j) or StringUtil.containsSubstring(r.addrOld[i],j):
                    lScore += SEARCH_BONUS_SCORE

            lScore = a
            if a<b:
                lScore = b

            if lScore > resScore:
                resScore = lScore
                resAddr = r.addr[i]
                resAddrOld = r.addrOld[i]
                resPos = r.postNum[i]

        node.score += resScore
        node.result = resAddr
        node.resultOld = resAddrOld
        node.postNum = resPos
        node.score += SEARCH_COMPLETE_SCORE
        table.score = resScore
        table.result = resAddr
        table.resultOld = resAddrOld
        table.postNum = resPos

    def sortTree(self):
        for city in self.tree.getTree():
            city.score = city.count + CITY_NODE_SCORE
            cS = ScoreTable(str(city.name), city.score)
            self.addrScore.append(cS)

            for dist in city.getTree():
                dist.score = city.score + dist.count + DIST_NODE_SCORE
                distName = dist.name
                dAddrStr = str(city.name) + " " + str(distName)

                dS = ScoreTable(dAddrStr,dist.score)
                if dist.end and self.ENABLE_HARD_SEARCH:
                    self.getSecrchResult(dist,dAddrStr,dS)
                self.addrScore.append(dS)

                for road in dist.getTree():
                    roadName = road.name
                    road.score = city.score+dist.score+road.count + ROAD_NODE_SCORE
                    rAddrStr = str(city.name) + " " + str(distName) + " " +str(roadName)

                    rS = ScoreTable(rAddrStr,road.score)
                    if road.end and self.ENABLE_HARD_SEARCH:
                        self.getSecrchResult(road,rAddrStr,rS)
                    self.addrScore.append(rS)

                    for num in road.getTree():
                        if self.ENABLE_HARD_SEARCH == False and num.end == True:
                            break
                        num.score = city.score+dist.score+road.score+num.count + NUM_NODE_SCORE
                        nAddrStr = str(city.name) + " " + str(distName) + " " +str(roadName) +" " + num.name

                        nS = ScoreTable(nAddrStr,num.score)
                        self.getSecrchResult(num,nAddrStr,nS)
                        self.addrScore.append(nS)