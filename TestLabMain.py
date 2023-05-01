#pip install requests hgtk
import Util
import requests, hgtk, random
from tkinter import *
from konlpy.tag import Kkma
import DicApi as dicapi
import Util as util

TAG = "TestLabMain"





# 변수 선언
global root
root = Tk()
global name
name = ""
global text
text = Text(root, wrap=WORD)
global btn
btn = Button(root,text="검색")
global kkma
kkma = Kkma()
global scoreTable


#시간
#장소
#이름

rows = 100
cols = 3
scoreTable = [[0 for j in range(cols)] for i in range(rows)]


currentLine = 0;

def main():

    loadUI()

    return 0

def loadUI():
    root.title("Test Lab")
    root.geometry("500x500")

    text.place(x= 50,y=50,height=100,width=400)
    text.pack()

    btn.config(command = analyze)
    btn.place(x= 200,y=200,height=10,width=50)
    btn.pack()

    root.mainloop()


def analyze():
    line_count = count_lines(text) # 라인 수를 셉니다.

    for i in range(1,line_count+1): # 라인별로 반복합니다.

        currentLine = i # 현재 라인을 전역변수에 저장

        data = get_line(text,i) # 각 라인의 텍스트 데이터를 얻습니다.

        spp = split(data) # 각 라인의 명사 리스트를 얻습니다. (Use KonlPy)
        for j in spp: # 명사를 리스트를 반복합니다.
            dd = dicapi.search(j) # 명사 검색시작

            if(dd != -1):
                Util.Log(TAG,"-------------------")

                Util.Log(TAG,"라인 수 : "+str(currentLine))
                Util.Log(TAG,"검색한 단어 : "+dd[0])
                Util.Log(TAG,"단어의 뜻 : "+dd[1])
                Util.Log(TAG,"-------------------")
                scoring(currentLine,dd)


            else:
                Util.Log(TAG,"사전에서 단어를 찾을 수 없습니다!")


    for i in range(0,currentLine):
        print("LineCount : ",i,scoreTable[i]," || ",get_line(text,i))

    max_place_score = 0
    for i in range(0, currentLine):
        if max_place_score < scoreTable[i][0]:
            max_place_score = scoreTable[i][0]
            index = i


    print("장소 | 최고점 : %d" %max_place_score,end = '')
    print(" | index : %d" %index,end = '')
    print(" | 데이터 : ", get_line(text,index))

    max_place_score_1 = 0
    for i in range(0, currentLine):
        if max_place_score_1 < scoreTable[i][1]:
            max_place_score_1 = scoreTable[i][1]
            index_1 = i


    print("시간 | 최고점 : %d" %max_place_score_1,end = '')
    print(" | index : %d" %index_1,end = '')
    print(" | 데이터 : ", get_line(text,index_1))


    max_place_score_2 = 0
    for i in range(0, currentLine):
        if max_place_score_2 < scoreTable[i][2]:
            max_place_score_2 = scoreTable[i][2]
            index_2 = i


    print("이름 | 최고점 : %d" %max_place_score_2,end = '')
    print(" | index : %d" %index_2,end = '')
    print(" | 데이터 : ", get_line(text,index_2))


global placeKey
placeKey = ['건물','공간','위치','장소','서울','대전','대구','부산','강원']
#지명

global timeKey
timeKey = ['시간','때','년','월','일','일시',':']

global nameKey
nameKey = ['이름','장남','장녀','부','모','사람','인물',"아들","딸",'김']


# 한 줄에 대한 점수를 채점합니다.
def scoring(line,data):
    # 장소 판별

    for i in placeKey:
        if data[0].find(i) != -1:
            scoreTable[line][0] +=1

        if data[1].find(i) != -1:
            scoreTable[line][0] +=1

    for i in timeKey:
        if data[0].find(i) != -1:
            scoreTable[line][1] +=1

        if data[1].find(i) != -1:
            scoreTable[line][1] +=1

    for i in nameKey:
        if data[0].find(i) != -1:
            scoreTable[line][2] +=1

        if data[1].find(i) != -1:
            scoreTable[line][2] +=1

    return 0

def count_lines(text):
    return int(text.index(END).split(".")[0])-1

def get_line(text,line_number):
    line_start = f"{line_number}.0"
    line_end = f"{line_number}.end"
    line_content = text.get(line_start, line_end)
    return line_content

def split(data):
    return kkma.nouns(data)





# 1.줄 분리
# 2.줄 평가
# 3.순위 쿼리
# 4.















main()

exit()









#이미 있는 단어 알기위해 단어목록 저장
history = []
playing = True


#좀 치사한 한방단어 방지 목록
blacklist = ['즘', '틱', '늄', '슘', '퓸', '늬', '뺌', '섯', '숍', '튼', '름', '늠', '쁨']

#지정한 두 개의 문자열 사이의 문자열을 리턴하는 함수
#string list에서 단어, 품사와 같은 요소들을 추출할때 사용됩니다
def midReturn(val, s, e):
    if s in val:
        val = val[val.find(s)+len(s):]
        if e in val: val = val[:val.find(e)]
    return val

#지정한 두 개의 문자열 사이의 문자열 여러개를 리턴하는 함수
#string에서 XML 등의 요소를 분석할때 사용됩니다
def midReturn_all(val, s, e):
    if s in val:
        tmp = val.split(s)
        val = []
        for i in range(0, len(tmp)):
            if e in tmp[i]: val.append(tmp[i][:tmp[i].find(e)])
    else:
        val = []
    return val

def findword(query):
    url = 'https://krdict.korean.go.kr/api/search?key=' + apikey + '&part=word&pos=1&q=' + query
    response = requests.get(url,verify=False)
    ans = []

    #단어 목록을 불러오기
    words = midReturn_all(response.text,'<item>','</item>')
    for w in words:
        #이미 쓴 단어가 아닐때
        if not (w in history):
            #한글자가 아니고 품사가 명사일때
            word = midReturn(w,'<word>','</word>')
            pos = midReturn(w,'<pos>','</pos>')
            if len(word) > 1 and pos == '명사' and not word in history and not word[len(word)-1] in blacklist:
                ans.append(w)
    if len(ans)>0:
        return random.choice(ans)
    else:
        return ''


def checkexists(query):
    url = 'https://krdict.korean.go.kr/api/search?key=' + apikey + '&part=word&sort=popular&num=100&pos=1&q=' + query
    response = requests.get(url,verify=False)
    ans = ''

    #단어 목록을 불러오기
    words = midReturn_all(response.text,'<item>','</item>')
    for w in words:
        #이미 쓴 단어가 아닐때
        if not (w in history):
            #한글자가 아니고 품사가 명사일때
            word = midReturn(w,'<word>','</word>')
            pos = midReturn(w,'<pos>','</pos>')
            if len(word) > 1 and pos == '명사' and word == query: ans = w

    if len(ans)>0:
        return ans
    else:
        return ''


print('''
=============파이썬 끝말잇기===============
사전 데이터 제공: 국립국어원 한국어기초사전
- - - 게임 방법 - - -
가장 처음 단어를 제시하면 끝말잇기가 시작됩니다
'/그만'을 입력하면 게임이 종료되며, '/다시'를 입력하여 게임을 다시 시작할 수 있습니다.
- - - 게임 규칙 - - -
1. 사전에 등재된 명사여야 합니다
2. 적어도 단어의 길이가 두 글자 이상이어야 합니다
3. 이미 사용한 단어를 다시 사용할 수 없습니다
4. 두음법칙 적용 가능합니다 (ex. 리->니)
==========================================
''')

answord = ''
sword = ''

while(playing):

    wordOK = False

    while(not wordOK):
        query = input(answord + ' > ')
        wordOK = True

        if query == '/그만':
            playing = False
            print('컴퓨터의 승리!')
            break
        elif query == '/다시':
            history = []
            answord = ''
            print('게임을 다시 시작합니다.')
            wordOK = False
        else:
            if query == '':
                wordOK = False

                if len(history)==0:
                    print('단어를 입력하여 끝말잇기를 시작합니다.')
                else:
                    print(sword + '(으)로 시작하는 단어를 입력해 주십시오.')

            else:
                #첫 글자의 초성 분석하여 두음법칙 적용 -> 규칙에 아직 완벽하게 맞지 않으므로 차후 수정 필요
                if not len(history)==0 and not query[0] == sword and not query=='':
                    sdis = hgtk.letter.decompose(sword)
                    qdis = hgtk.letter.decompose(query[0])
                    if sdis[0] == 'ㄹ' and qdis[0] == 'ㄴ': print('두음법칙 적용됨')
                    elif (sdis[0] == 'ㄹ' or sdis[0] == 'ㄴ') and qdis[0] == 'ㅇ' and qdis[1] in ('ㅣ', 'ㅑ', 'ㅕ', 'ㅛ', 'ㅠ', 'ㅒ', 'ㅖ'): print('두음법칙 적용됨')
                    else:
                        wordOK = False
                        print(sword + '(으)로 시작하는 단어여야 합니다.')

                if len(query) == 1:
                    wordOK = False
                    print('적어도 두 글자가 되어야 합니다')

                if query in history:
                    wordOK = False
                    print('이미 입력한 단어입니다')

                if query[len(query)-1] in blacklist:
                    print('아.. 좀 치사한데요..')

                if wordOK:
                    #단어의 유효성을 체크
                    ans = checkexists(query)
                    if ans == '':
                        wordOK = False
                        print('유효한 단어를 입력해 주십시오')
                    else:
                        print('(' + midReturn(ans, '<definition>', '</definition>') + ')\n')

    history.append(query)

    if playing:
        start = query[len(query)-1]

        ans = findword(start + '*')

        if ans=='':
            #ㄹ -> ㄴ 검색
            sdis = hgtk.letter.decompose(start)
            if sdis[0] == 'ㄹ':
                newq = hgtk.letter.compose('ㄴ', sdis[1], sdis[2])
                print(start, '->', newq)
                start = newq
                ans = findword(newq + '*')

        if ans=='':
            #(ㄹ->)ㄴ -> ㅇ 검색
            sdis = hgtk.letter.decompose(start)
            if sdis[0] == 'ㄴ' and sdis[1] in ('ㅣ', 'ㅑ', 'ㅕ', 'ㅛ', 'ㅠ', 'ㅒ', 'ㅖ'):
                newq = hgtk.letter.compose('ㅇ', sdis[1], sdis[2])
                print(start, '->', newq)
                ans = findword(newq + '*')

        if ans=='':
            print('당신의 승리!')
            break
        else:
            answord = midReturn(ans, '<word>', '</word>') #단어 불러오기
            ansdef = midReturn(ans, '<definition>', '</definition>') # 품사 불러오기
            history.append(answord)

            print(query, '>', answord, '\n('+ansdef+')\n')
            sword = answord[len(answord)-1]

            #컴퓨터 승리여부 체크
            #if findword(sword) == '':
            #    print('tip: \'/다시\'를 입력하여 게임을 다시 시작할 수 있습니다')
