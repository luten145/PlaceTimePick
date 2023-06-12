import requests
from PythonSource.Util import Log
from PythonSource.Util import XmlUtil

TAG = "AddressApi"

apikey = 'devU01TX0FVVEgyMDIzMDUyMDE5NDcyNjExMzc5MTU='

class SearchResult:
    def __init__(self):
        self.word = ""
        self.addr = []
        self.addrOld = []
        self.postNum = []
        self.resultCount = 0


def removeCdata( string):
    return string.replace('<![CDATA[', '').replace(']]>', '')

class AddressApi():
    def wordSearch(self,data): # 단어의 뜻과 설명을 반환
        result = SearchResult()
        Log.d(TAG, "In data : " + data)
        url = 'https://business.juso.go.kr/addrlink/addrLinkApi.do?currentPage=1&countPerPage%20=10&keyword='+ data + '&confmKey=' + apikey + '&hstryYn=Y'
        Log.d(TAG, url)
        response = requests.get(url,verify=True)
        words = XmlUtil.getDataList(response.text, '<juso>', '</juso>') #단어 목록을 불러오기
        result.word = data
        for w in words:
            word = XmlUtil.getDataItem(w, '<roadAddr>', '</roadAddr>') #리스트의 아이템 갖고오기
            word = removeCdata(word)
            word2 = XmlUtil.getDataItem(w, '<jibunAddr>', '</jibunAddr>') #리스트의 아이템 갖고오기
            word2 = removeCdata(word2)
            word3 = XmlUtil.getDataItem(w, '<zipNo>', '</zipNo>') #리스트의 아이템 갖고오기
            word3 = removeCdata(word3)
            if len(word) > 0:
                result.addr.append(word)
                result.addrOld.append(word2)
                result.postNum.append(word3)
                result.resultCount +=1
        return result