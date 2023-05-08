#pip install requests hgtk
import Util
import requests, hgtk, random
import re
import json
from konlpy.tag import Kkma
import DicApi as dicapi
import Util as util
import os

from tkinter import filedialog
from tkinter import messagebox


TAG = "TestLabMain"


#시간
#장소
#이름

place_score=[0 for i in range(100)]
currentLine = 0

def main():
    # txt 파일을 json파일로 읽기
    list_file = []                                          #파일 목록 담을 리스트 생성
    files = filedialog.askopenfilenames(initialdir="/", \
                                    title = "파일을 선택 해 주세요", \
                                    filetypes = (("*.txt","*txt"),("*.xls","*xls"),("*.csv","*csv")))
    #files 변수에 선택 파일 경로 넣기

    if files == '':
        messagebox.showwarning("경고", "파일을 추가 하세요")    #파일 선택 안했을 때 메세지 출력

    print(files)    #files 리스트 값 출력

    with open(files[0], 'r', encoding='utf-8') as f:
        data3 = json.load(f)

    # json 파일 내에 text 키의 값들만 읽어서 하나의 리스트로 만들기
    text_list= data3["task_result"]["text"]
    combined_text = "".join(text_list)
    text = [combined_text]

    print(text)
    analyze(str(text))

    return 0




def analyze(text):
    line_list = count_lines(text) # 라인 리스트
    currentLine = line_list # 현재 라인을 전역변수에 저장
    Np = 0

    for i in line_list: # 라인을 i에 넣습니다.
        data = i

        spp = split(data) # 각 라인의 명사 리스트를 얻습니다. (Use KonlPy)
        for j in spp: # 명사를 리스트를 반복합니다.
            dd = dicapi.search(j) # 명사 검색시작

            if(dd != -1):
                Util.Log(TAG,"-------------------")
                Util.Log(TAG,"검색한 단어 : "+dd[0])
                Util.Log(TAG,"단어의 뜻 : "+dd[1])
                Util.Log(TAG,"-------------------")
                place_score[Np] += scoring(dd)


            else:
                Util.Log(TAG,"사전에서 단어를 찾을 수 없습니다!")
        Np += 1

    for i in range(Np):
        print("LineCount : ",i,place_score[i]," || ",get_line(text,i))

    max_place_score = 0
    for i in range(Np):
        if max_place_score < place_score[i]:
            max_place_score = place_score[i]
            index = i


    print("장소 | 최고점 : %d" %max_place_score,end = '')
    print(" | index : %d" %index,end = '')
    print(" | 데이터 : ", get_line(text,index))


global placeKey
placeKey = ['건물','공간','위치','장소','홀','예식장']
#지명

# 한 줄에 대한 점수를 채점합니다.
def scoring(data):
    place = 0
    # 장소 판별

    for i in placeKey:
        if data[0].find(i) != -1:
            place +=1

        if data[1].find(i) != -1:
            place +=1

    return place

def count_lines(text):
    return text.split('\\n')

def get_line(text,line_number):
    line_content = text.split("\\n")
    return line_content[line_number]

def split(data):
    kkma = Kkma()
    return kkma.nouns(data)





# 1.줄 분리
# 2.줄 평가
# 3.순위 쿼리
# 4.















main()

exit()
