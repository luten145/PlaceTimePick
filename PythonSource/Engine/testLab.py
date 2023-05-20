import operator
import re
from tkinter import *
from konlpy.tag import Kkma
import PythonSource.Util.DicApi as dicApi
from PythonSource.Util import LogUtil as logUtil
from PythonSource.UI.UIListener import UIEventListener
from PythonSource.UI import UIMain
from PythonSource.Util import AddressDB
from PythonSource.Util import StringUtil
from PythonSource.Engine import Engine3
from PythonSource.Engine import Engine4


class Address:
    def __init__(self):
        self.name = "NAME"
        self.line = []
        self.count = 0


def getCity(textList): # 데이터에서 시를 찾습니다.
    tag = "getCity"


    b = AddressDB.AddressDB()

    regionPattern = b.getAdressList()[0]  # All city list

    res = []
    c = 0
    for i in textList:
        for j in regionPattern:
            num = StringUtil.countPattern(i, j)
            if num > 0:
                a = Address()
                a.name = j
                a.count += 1
                a.line.append(c)
                res.append(a)
        c+=1
    print(res[0].__dict__)


a = []

a.append("['서리간생")
a.append(".기다")
a.append("음y")
a.append("주우소9")
a.append("63소")
a.append("평생올 같이하고 싶은 사람올 만남습니다 .")
a.append("0주9 G29")
a.append("서로률 아꺼주고 사랑하다 살고 싶습니다,")
a.append("우리 약속 위에 따뜻한 격러로 축복해 주서서")
a.append("야리럼")
a.append("힘찬 출발의 디풀이 되어주심시오")
a.append("다기리")
a.append("십별")
a.append("다오1사7 _")
a.append("갈은 곳올 바라보력")
a.append("\'언제나 함씨 하젊습니다")
a.append("운현서  의")
a.append("아들")
a.append("박성민")
a.append("지하;")
a.append("수원역 4번출구 앞 720-2 730 831 10-2 10 5 3 451 9 2 하71")
a.append("이용 추 \'수원고용센터 동수원병원. 라마다호텔 앞\' 하차")
a.append("박용규")
a.append("약 4.4kI, ?분 소요)")
a.append("의")
a.append("박다인")
a.append("배미영")
a.append("광의버스")
a.append("강남역 신문당선 도번출구 반대방함으로 보도 이용하여 더무도씨예빛")
a.append("오피스템 지나서 커피반 앞 정류장네서 승차")
a.append("3007번 이용 추 \'아주대병원입구\' 하차")
a.append("3002번 이용 탑 \'정소년문화센터\' 하차")
a.append("사당역 4번출구 반대방항으로 도보 이동하여 GS25편의점 앞 정류장")
a.append("7000/7001번 이용 후 \'아주머병원입구")
a.append("하차")
a.append("2021년 10월 24일 일요일 낮 12시")
a.append("잠실역 6번규구 앞 1007-번 이용 후 \'아주대병원입구\' 하차")
a.append("성남시청 또는 야달역 승차시 4000번 이용 후 \'청소년문화센터\' 하차")
a.append("더아리엘 5층 스카이가듣풀")
a.append("아주대병원입구 정거장 암 버스 노선")
a.append("720-2 7D 46 1 9 2 711 62 7 20 이용 부 \'우안신성아파트\' 하차")
a.append("주차장")
a.append("건물내 지하 1 2충 주차장 주차타위 주차장 승림사우나 주차장")
a.append("삼성디지털프라자 뒤 세운주차장 동수왼병원 주차장 - 2간 무료")
a.append("더 아리언")
a.append("031-24-9300")
a.append("경기도 수원시 팔달구 중부대로 161(우만?동 147-7)")
a.append("눈무시계")
a.append("이론다- ?")
a.append("지금처립")
a.append("서도의 스: 탑:")
a.append("']")


b = Engine4.Engine4()
b.dataHandler(a)