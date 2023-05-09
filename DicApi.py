import requests
import Util as util

TAG = "DicApi"

#키 발급은 https://krdict.korean.go.kr/openApi/openApiInfo
apikey = '89CEE1F97C97DDB57C4279AA8FFB6F38'

class SearchResult:
    word = ""
    definition = ""

#지정한 두 개의 요소 사이의 값을 리스트화 하여 리턴하는 함수
#string에서 XML 등의 요소를 분석할때 사용됩니다
def getDataList(data, s, e):
    if s in data:
        tmp = data.split(s)
        data = []
        for i in range(0, len(tmp)):
            if e in tmp[i]: data.append(tmp[i][:tmp[i].find(e)])
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
    util.Log(TAG,"In data : "+data)
    url = 'https://krdict.korean.go.kr/api/search?key=' + apikey + '&part=word&sort=popular&num=100&pos=1&q=' + data
    response = requests.get(url,verify=False)
    ans = ''

    words = getDataList(response.text, '<item>', '</item>') #단어 목록을 불러오기

    result.word = data
    for w in words: #print("검색한 데이터의 쿼리 목록입니다.")
        word = getDataItem(w, '<word>', '</word>') #리스트의 아이템 갖고오기
        pos = getDataItem(w, '<pos>', '</pos>') #형태소 데이터
        if pos == '명사' and word == data: #명사만 검색
            ans = w

    if len(ans)>0: # 품사가 명사일
        result.definition = getDataItem(ans, '<definition>', '</definition>')

    return result