import requests, hgtk, random
import Util as util

#키 발급은 https://krdict.korean.go.kr/openApi/openApiInfo
apikey = '89CEE1F97C97DDB57C4279AA8FFB6F38'
#지정한 두 개의 요소 사이의 값을 리스트화 하여 리턴하는 함수
#string에서 XML 등의 요소를 분석할때 사용됩니다

TAG = "DicApi"
def midReturn_all(val, s, e):
    if s in val:
        tmp = val.split(s)
        val = []
        for i in range(0, len(tmp)):
            if e in tmp[i]: val.append(tmp[i][:tmp[i].find(e)])
    else:
        val = []
    return val

def defInfo(val, s, e):
    if s in val:
        val = val[val.find(s)+len(s):]
        if e in val: val = val[:val.find(e)]
    return val

def search(data): # 단어의 뜻과 설명을 반환
    info = [""]*2

    util.Log(TAG,"들어온 데이터 "+data)


    url = 'https://krdict.korean.go.kr/api/search?key=' + apikey + '&part=word&sort=popular&num=100&pos=1&q=' + data
    response = requests.get(url,verify=False)
    ans = ''

    #단어 목록을 불러오기
    words = midReturn_all(response.text,'<item>','</item>')

    #print("검색한 데이터의 쿼리 목록입니다.")
    for w in words:

        word = defInfo(w,'<word>','</word>')
        #print("결과 : ",word)
        #print('(' + defInfo(w, '<definition>', '</definition>') + ')\n')
        pos = defInfo(w,'<pos>','</pos>')

        if pos == '명사' and word == data:
            ans = w


        # 품사가 명사일때
    if len(ans)>0:
        #print('(' + defInfo(ans, '<definition>', '</definition>') + ')\n')
        info[0] = defInfo(ans,'<word>','</word>')
        info[1] = defInfo(ans, '<definition>', '</definition>')
    else:
        return -1

    return info
