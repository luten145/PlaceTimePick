import requests
from PythonSource.Util.LogUtil import *

TAG = "AddressApi"


apikey = 'devU01TX0FVVEgyMDIzMDUyMDE5NDcyNjExMzc5MTU='

class SearchResult:
    word = ""
    addr = []
    resultCount = 0

#지정한 두 개의 요소 사이의 값을 리스트화 하여 리턴하는 함수
#string에서 XML 등의 요소를 분석할때 사용됩니다
def getDataList(data, s, e):
    if s in data:
        tmp = data.split(s)
        data = []
        for i in range(0, len(tmp)):
            if e in tmp[i]:
                data.append(tmp[i][:tmp[i].find(e)])
    else:
        data = []
    return data


def getDataItem(data, s, e):
    if s in data:
        data = data[data.find(s) + len(s):]
        if e in data: data = data[:data.find(e)]
    return data


def wordSearch(data): # 단어의 뜻과 설명을 반환
    result = SearchResult()
    Log(TAG,"In data : "+data)
    url = 'https://business.juso.go.kr/addrlink/addrLinkApi.do?currentPage=1&countPerPage%20=10&keyword='+ data + '&confmKey=' + apikey + '&hstryYn=Y'
    Log(TAG,url)
    response = requests.get(url,verify=True)
    ans = ''

    words = getDataList(response.text, '<juso>', '</juso>') #단어 목록을 불러오기

    result.word = data
    for w in words: #print("검색한 데이터의 쿼리 목록입니다.")
        word = getDataItem(w, '<roadAddr>', '</roadAddr>') #리스트의 아이템 갖고오기
        if len(word) > 3:
            result.addr.append(word)
            result.resultCount +=1

            return result

    return result