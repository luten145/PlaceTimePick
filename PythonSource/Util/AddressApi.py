import requests
from PythonSource.Util.LogUtil import *

TAG = "AddressApi"


apikey = 'devU01TX0FVVEgyMDIzMDUyMDE5NDcyNjExMzc5MTU='

class SearchResult:
    def __init__(self):
        self.word = ""
        self.addr = []
        self.addrOld = []
        self.postNum = []
        self.resultCount = 0



class AddressApi():

    #지정한 두 개의 요소 사이의 값을 리스트화 하여 리턴하는 함수
    #string에서 XML 등의 요소를 분석할때 사용됩니다
    def getDataList(self,data, s, e):
        if s in data:
            tmp = data.split(s)
            data = []
            for i in range(0, len(tmp)):
                if e in tmp[i]:
                    data.append(tmp[i][:tmp[i].find(e)])
        else:
            data = []
        return data


    def getDataItem(self,data, s, e):
        if s in data:
            data = data[data.find(s) + len(s):]
            if e in data: data = data[:data.find(e)]
        return data

    def remove_cdata(self,string):
        return string.replace('<![CDATA[', '').replace(']]>', '')

    def wordSearch(self,data): # 단어의 뜻과 설명을 반환
        result = SearchResult()
        Log(TAG,"In data : "+data)
        url = 'https://business.juso.go.kr/addrlink/addrLinkApi.do?currentPage=1&countPerPage%20=10&keyword='+ data + '&confmKey=' + apikey + '&hstryYn=Y'
        Log(TAG,url)
        response = requests.get(url,verify=True)
        ans = ''

        words = self.getDataList(response.text, '<juso>', '</juso>') #단어 목록을 불러오기

        result.word = data
        for w in words: #print("검색한 데이터의 쿼리 목록입니다.")
            word = self.getDataItem(w, '<roadAddr>', '</roadAddr>') #리스트의 아이템 갖고오기
            word = self.remove_cdata(word)
            word2 = self.getDataItem(w, '<jibunAddr>', '</jibunAddr>') #리스트의 아이템 갖고오기
            word2 = self.remove_cdata(word2)
            word3 = self.getDataItem(w, '<zipNo>', '</zipNo>') #리스트의 아이템 갖고오기
            word3 = self.remove_cdata(word3)
            if len(word) > 0:
                result.addr.append(word)
                result.addrOld.append(word2)
                result.postNum.append(word3)
                result.resultCount +=1
        return result