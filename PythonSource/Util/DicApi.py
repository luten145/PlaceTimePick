import requests
from PythonSource.Util import Log
from PythonSource.Util import XmlUtil

TAG = "DicApi"

# 키 발급은 https://krdict.korean.go.kr/openApi/openApiInfo
apikey = '89CEE1F97C97DDB57C4279AA8FFB6F38'


class SearchResult:
    def __init__(self):
        self.word = ""
        self.definition = ""


def wordSearch(data): # 단어의 뜻과 설명을 반환
    result = SearchResult()
    Log.d(TAG, "In data : " + data)
    url = 'https://krdict.korean.go.kr/api/search?key=' + apikey + '&part=word&sort=popular&num=100&pos=1&q=' + data
    response = requests.get(url,verify=False)
    ans = ''
    words = XmlUtil.getDataList(response.text, '<item>', '</item>') #단어 목록을 불러오기
    result.word = data
    for w in words:
        word = XmlUtil.getDataItem(w, '<word>', '</word>') #리스트의 아이템 갖고오기
        pos = XmlUtil.getDataItem(w, '<pos>', '</pos>') #형태소 데이터
        if pos == '명사' and word == data: #명사만 검색
            ans = w
    if len(ans) > 0:
        result.definition = XmlUtil.getDataItem(ans, '<definition>', '</definition>')
    return result