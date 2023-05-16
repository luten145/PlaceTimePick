
def SearchAdress(AddressList,Find,AdressNum=0):
    if AdressNum == 0:
        City=[i for i in AddressList if Find in i[1]]
        return City

    elif AdressNum == 1:
        District=[i for i in AddressList if Find in i[3]]
        return District

    elif AdressNum == 2:
        Town=[i for i in AddressList if Find in i[5]]
        return Town

    elif AdressNum == 3:
        Road=[i for i in AddressList if Find in i[7]]
        return Road

    elif AdressNum == 4:
        Num=[i for i in AddressList if Find in i[10]]
        return Num

FIND_CITY=0
FIND_DISTRICT=1
FIND_TOWN=2
FIND_ROAD=3
FIND_NUM=4

# TODO 1 : 핵심 단어만 리스트화하는 함수 만들기
#  EX)서울 특별시 -> 서울 ,강원도 -> 강원
#  방식은 서울 특별시와 같은 리스트를 넣으면 변환된 리스트가 나오게 하는 함수를 새로 만들거나
#  기존 함수에 플래그 인수 추가 중 선택
#  SearchAdress(AddressList,"경상북도",0)  # 출력 : 서울 특별시 , 강원도, 제주특별자치도
#  SearchAdress(AddressList,"경상북도",1)  # 출력 : 서울,강원,대구

f = open("./Util/Address.txt", "r", encoding="utf-8")
AddressList=[i.split("|") for i in f.readlines()]
f.close()

'''
Scarch Example
CityList=SearchAdress(AddressList,"경상북도")
print(CityList)
DistrictList=SearchAdress(CityList,"영천시",FIND_DISTRICT)
print(DistrictList)
TownList=SearchAdress(DistrictList,"화산면",FIND_TOWN)
print(TownList)
RoadList=SearchAdress(TownList,"신정길",FIND_ROAD)
print(RoadList)
NumList=SearchAdress(RoadList,"60",FIND_NUM)
print(NumList)
'''