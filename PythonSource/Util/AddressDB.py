import re

#리스트로 얻고자 하는 데이터의 종류 (출력대상)
FIND_CITY=1
FIND_DISTRICT=3
FIND_TOWN=5
FIND_ROAD=7
FIND_ROAD_NUM=8
FIND_NUM=10

class AddressDB:
    def __init__(self):
        self.f = open("./Util/Address.txt", "r", encoding="utf-8")
        self.AddressList=[i.split("|") for i in self.f.readlines()]
        self.f.close()
        pass


    def getAdressList(self,Find=0, AddressNum=1, AddressGet=1):
        l = self.SearchAddress(self.AddressList,Find,AddressNum,AddressGet)
        return l


    def SearchAddress(self,AddressList, Find=0, AddressNum=1, AddressGet=1):
        Address=[[]for i in range(2)]
        if(Find == '전북'):
            Find = '전라북도'
        if Find != 0:
            if AddressGet == FIND_CITY:
                for i in AddressList:
                    if Find in i[AddressNum]:
                        Address[0].append(i[AddressGet][0:2]); Address[1].append(i[AddressGet])
                Address[0]=list(set(Address[0])); Address[1]=list(set(Address[1]))
                Address[0].append('전북')
                Address[0].append('전남')
                return Address
            
            elif AddressGet == FIND_DISTRICT or AddressGet == FIND_TOWN:
                for i in AddressList:
                    if Find in i[AddressNum]:
                        if i[AddressGet].find(" ") != -1:
                            if len(i[AddressGet].split(" ")[0][:-1]) == 1:
                                Address[0].append(i[AddressGet].split(" ")[0])
                            else:
                                Address[0].append(i[AddressGet].split(" ")[0][:-1])
                            
                            if len(i[AddressGet].split(" ")[1][:-1]) == 1:
                                Address[0].append(i[AddressGet].split(" ")[1])
                            else:
                                Address[0].append(i[AddressGet].split(" ")[1][:-1])
                            
                            Address[1].extend(i[AddressGet].split(" "))
                        
                        else:
                            if len(i[AddressGet][:-1]) == 1:
                                Address[0].append(i[AddressGet])
                            else:
                                Address[0].append(i[AddressGet][:-1])
                            Address[1].append(i[AddressGet])

                Address[0]=list(set(Address[0])); Address[1]=list(set(Address[1]))
                return Address
            
            elif AddressGet == FIND_ROAD:
                for i in AddressList:
                    if Find in i[AddressNum]:
                        m = re.search('\d+',i[AddressGet])
                        if m != None:
                            if m.start():
                                Address[0].append(i[AddressGet][:m.start()])
                        else:
                            Address[0].append(i[AddressGet])
                        Address[1].append(i[AddressGet])
                Address[0]=list(set(Address[0])); Address[1]=list(set(Address[1]))
                return Address

            elif AddressGet == FIND_NUM:
                Address[0]=list(set([i[AddressGet] for i in AddressList if Find in i[AddressNum]]))
                return Address
            
            elif AddressGet == FIND_ROAD_NUM:
                for i in AddressList:
                    if Find in i[AddressNum]:
                        m = re.search('\d+',i[FIND_ROAD])
                        if m != None:
                            if m.start():
                                Address[0].append(i[FIND_ROAD][m.start():m.end()])
                                Address[1].append(i[FIND_ROAD][m.start():])
                Address[0]=list(set(Address[0])); Address[1]=list(set(Address[1]))
                return Address
            
            

        elif Find == 0:
            if AddressGet == FIND_CITY:
                for i in AddressList:
                    Address[0].append(i[AddressGet][0:2]); Address[1].append(i[AddressGet])
                Address[0]=list(set(Address[0])); Address[1]=list(set(Address[1]))
                Address[0].append('전북')
                Address[0].append('전남')
                return Address
            
            elif AddressGet == FIND_DISTRICT or AddressGet == FIND_TOWN:
                for i in AddressList:
                    if i[AddressGet].find(" ") != -1:
                        if len(i[AddressGet].split(" ")[0][:-1]) == 1:
                            Address[0].append(i[AddressGet].split(" ")[0])
                        else:
                            Address[0].append(i[AddressGet].split(" ")[0][:-1])
                        
                        if len(i[AddressGet].split(" ")[1][:-1]) == 1:
                            Address[0].append(i[AddressGet].split(" ")[1])
                        else:
                            Address[0].append(i[AddressGet].split(" ")[1][:-1])
                        
                        Address[1].extend(i[AddressGet].split(" "))
                        
                    else:
                        if len(i[AddressGet][:-1]) == 1:
                            Address[0].append(i[AddressGet])
                        else:
                            Address[0].append(i[AddressGet][:-1])
                        Address[1].append(i[AddressGet])

                Address[0]=list(set(Address[0])); Address[1]=list(set(Address[1]))
                return Address
            
            elif AddressGet == FIND_ROAD:
                for i in AddressList:
                    m = re.search('\d+',i[AddressGet])
                    if m != None:
                        if m.start():
                            Address[0].append(i[AddressGet][:m.start()])
                    else:
                        Address[0].append(i[AddressGet])
                    Address[1].append(i[AddressGet])
                Address[0]=list(set(Address[0])); Address[1]=list(set(Address[1]))
                return Address

            elif AddressGet == FIND_NUM:
                Address[0]=list(set([i[AddressGet] for i in AddressList]))
                return Address
            
            elif AddressGet == FIND_ROAD_NUM:
                for i in AddressList:
                    if Find in i[AddressNum]:
                        m = re.search('\d+',i[FIND_ROAD])
                        if m != None:
                            if m.start():
                                Address[0].append(i[FIND_ROAD][m.start():m.end()])
                                Address[1].append(i[FIND_ROAD][m.start():])
                Address[0]=list(set(Address[0])); Address[1]=list(set(Address[1]))
                return Address



    # ODO 1 : 핵심 단어만 리스트화하는 함수 만들기 OK
    #  EX)서울 특별시 -> 서울 ,강원도 -> 강원
    #  방식은 서울 특별시와 같은 리스트를 넣으면 변환된 리스트가 나오게 하는 함수를 새로 만들거나
    #  기존 함수에 플래그 인수 추가 중 선택
    #  SearchAdress(AddressList,"경상북도",0)  # 출력 : 서울 특별시 , 강원도, 제주특별자치도
    #  SearchAdress(AddressList,"경상북도",1)  # 출력 : 서울,강원,대구

    # ODO 2 : 한글자인거는 뒤까지 툴력 하도록  변경 ex) 중구 -> 중 (X)  , 중구 -> 중구
    # ODO 3 : 시 군구 에서 '성남시 수정', '성남시 분당' 같은 경우 성남, 분당 , 성남, 수정으로 나누어서 리스트 만들기
    # ODO 4 : 도로명의 경우 뒷 숫자 빼고 리스트 말들고 숫자는 따로 리스트 얻는함수 만들기
    # ODO 5 : 서울입력 -> 서울특별시 출력되는 함수 만들기
    # TODO 5 : 전북 전남 경북 경남 안됨 => 전북,전남 입력시 전라북도,전라남도 나와야 하고 CITY 출력 시 전라북도 => 전라,전북 모두 나오도록 하기
    # TODO 6 : 지번정보 검색 불가 => 지번도 사용 가능하도록 하기 + 지번과 도로명주소는 동시에 검색되면 안됨 인수로 이를 구분하도록 하기




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
print(a.getAdressList(Find="강동구",AddressNum=FIND_DISTRICT,AddressGet=FIND_ROAD))
print(a.getAdressList(Find="강동구",AddressNum=FIND_DISTRICT,AddressGet=FIND_ROAD_NUM))
print(a.getAdressList(Find="서구",AddressNum=FIND_DISTRICT,AddressGet=FIND_ROAD)[0])