

#탐색하는 데이터의 위치 (판별대상)
FIND2CITY=1
FIND2DISTRICT=3
FIND2TOWN=5
FIND2ROAD=7
FIND2NUM=10

#리스트로 얻고자 하는 데이터의 종류 (출력대상)
FIND_CITY=1
FIND_DISTRICT=3
FIND_TOWN=5
FIND_ROAD=7
FIND_NUM=10

class AddressDB:
    def __init__(self):
        self.f = open("../PythonSource/Util/Address.txt", "r", encoding="utf-8")
        self.AddressList=[i.split("|") for i in self.f.readlines()]
        self.f.close()

        pass

    def getAdressList(self,Find=0, AddressNum=1, AddressGet=1):
        l = self.SearchAddress(self.AddressList,Find,AddressNum,AddressGet)
        return l


    def SearchAddress(self,AddressList, Find=0, AddressNum=1, AddressGet=1):
        if Find != 0:
            if AddressGet == FIND_CITY:
                Address=[list(set([i[AddressGet] for i in AddressList if Find in i[AddressNum]])) if j == 1 else list(set([i[AddressGet][0:2] for i in AddressList if Find in i[AddressNum]])) for j in range(2)]
                return Address
            elif AddressGet == FIND_DISTRICT or AddressGet == 5:
                Address=[list(set([i[AddressGet] for i in AddressList if Find in i[AddressNum]])) if j == 1 else list(set([i[AddressGet][:-1] for i in AddressList if Find in i[AddressNum]])) for j in range(2)]
                return Address
            else:
                Address=list(set([i[AddressGet] for i in AddressList if Find in i[AddressNum]]))
                return Address

        elif Find == 0:
            if AddressGet == 1:
                CityList=[list(set([i[AddressGet] for i in AddressList])) if j == 1 else list(set([i[AddressGet][0:2] for i in AddressList])) for j in range(2)]
                return CityList
            elif AddressGet == 3 or AddressGet == 5:
                DorTList=[list(set([i[AddressGet] for i in AddressList])) if j == 1 else list(set([i[AddressGet][:-1] for i in AddressList])) for j in range(2)]
                return DorTList
            else:
                RorNList=list(set([i[AddressGet] for i in AddressList]))
                return RorNList



    # TODO 1 : 핵심 단어만 리스트화하는 함수 만들기
    #  EX)서울 특별시 -> 서울 ,강원도 -> 강원
    #  방식은 서울 특별시와 같은 리스트를 넣으면 변환된 리스트가 나오게 하는 함수를 새로 만들거나
    #  기존 함수에 플래그 인수 추가 중 선택
    #  SearchAdress(AddressList,"경상북도",0)  # 출력 : 서울 특별시 , 강원도, 제주특별자치도
    #  SearchAdress(AddressList,"경상북도",1)  # 출력 : 서울,강원,대구

    # TODO 2 : 한글자인거는 뒤까지 툴력 하도록  변경 ex) 중구 -> 중 (X)  , 중구 -> 중구
    # TODO 3 : 시 군구 에서 '성남시 수정', '성남시 분당' 같은 경우 성남, 분당 , 성남, 수정으로 나누어서 리스트 만들기
    # TODO 4 : 도로명의 경우 뒷 숫자 빼고 리스트 말들고 숫자는 따로 리스트 얻는함수 만들기
    # TODO 5 : 서울입력 -> 서울특별시 출력되는 함수 만들기




    '''
    Scarch Example
    CityList=SearchAdress(AddressList,"경상북도")
    >>>>>>> Stashed changes
    print(CityList)
    
    CityList=SearchAdress(AddressList,Find="강서구",AddressNum=FIND_DISTRICT,AddressGet=FIND_CITY)
    print(CityList)
    
    DistrictList=SearchAdress(AddressList,AddressGet=FIND_DISTRICT)
    print(DistrictList)
    
    DistrictList=SearchAdress(AddressList,Find="서울",AddressNum=FIND2CITY,AddressGet=FIND_DISTRICT)
    print(DistrictList)
    
    TownList=SearchAdress(AddressList,AddressGet=FIND_TOWN)
    print(TownList)
    
    TownList=SearchAdress(AddressList,Find="금산군",AddressNum=FIND2DISTRICT,AddressGet=FIND_TOWN)
    print(TownList)
    
    RoadList=SearchAdress(AddressList,AddressGet=FIND_ROAD)
    print(RoadList)
    
    RoadList=SearchAdress(AddressList,Find="강동구",AddressNum=FIND2DISTRICT,AddressGet=FIND_ROAD)
    print(RoadList)
    
    # NumList=SearchAdress(AddressList,AddressGet=FIND_NUM)
    # print(NumList)
    
    NumList=SearchAdress(AddressList,Find="금산군",AddressNum=FIND2DISTRICT,AddressGet=FIND_NUM)
    print(NumList)
    '''

a = AddressDB()
print(a.getAdressList())