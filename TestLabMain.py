import re
import json
import os
from tkinter import filedialog
from tkinter import messagebox

# txt 파일을 json파일로 읽기
list_file = []      #파일 목록 담을 리스트 생성
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

text_list=str(text).split('\\n')
text_str=str(text).replace("\\n"," ")

rows = 100
cols = 3
scoreTable = [[0 for j in range(cols)] for i in range(rows)]

print(text_list)
print()
print()

placeKey = ["서울","부산","대구","인천","광주","대전","울산","경기","강원","충청","전라","경상","제주","세종","홀","웨딩","층"]
place_list=[]

nameKey = ['남','녀',"아들","딸",'의']
name_list=[]

for i in range(len(text_list)):
    for j in placeKey:
        if text_list[i].find(j) != -1:
            place_list.append(text_list[i])
            break

    for j in nameKey:
        if text_list[i].find(j) != -1:
            name_list.append(text_list[i+1])
            break

#초기화
year,month,day,week,hour,minute=0,0,0,0,0,0

# 년도 추출
year_str = re.search(r'\d+년', text_str)[0]
year = int(re.search(r'\d+', year_str)[0])

# 월 추출
month_str = re.search(r'\d+월', text_str)[0]
month = int(re.search(r'\d+', month_str)[0])

# 일 추출
day_str = re.search(r'\d+일', text_str)[0]
day = int(re.search(r'\d+', day_str)[0])

# 요일 추출
week = re.search(r'\d+년 \d+월 \d+일 (일|월|화|수|목|금|토)요일 (?:오후|오전|낮)?\s?(\d{1,2})\s?[시:]\s?(\d{0,2})\s?(?:분)?', text_str)

# 시간 추출
time_matches = re.findall(r'(?:오후|오전|낮)?\s?(\d{1,2})\s?[시:]\s?(\d{0,2})\s?(?:분)?', text_str)[0]
hour = int(time_matches[0])
if '오후' in text_list:
    hour += 12
minute = int(time_matches[1]) if time_matches[1] else 0



print(place_list)
print(name_list)
print("----------")
print("년:", year, type(year))
print("월:", month, type(month))
print("일:", day, type(day))
print("요일:", week, type(week))
print(hour,":",minute)

"""
정규표현 방식을 배열화 시켜서
place_key,name_key랑 유사하게 동작하여
날짜에 대한 배열 추출
"""