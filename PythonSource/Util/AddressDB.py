import re

#지번주소 도로명 주소 구분
ROAD_ADDRESS=0
OLD_ADDRESS=1

#리스트로 찾고자,얻고자 하는 도로명 데이터의 종류
ROAD_FIND_CITY=1
ROAD_FIND_DISTRICT=3
ROAD_FIND_TOWN=5
ROAD_FIND_ROAD=7
ROAD_FIND_ROAD_NUM=8
ROAD_FIND_NUM=10

#리스트로 찾고자,얻고자 하는 지번 데이터의 종류
OLD_FIND_CITY=1
OLD_FIND_DISTRICT=3
OLD_FIND_TOWN=5
OLD_FIND_VILLAGE=7

class AddressDB:
    def __init__(self):
        self.f = open("PythonSource/Util/RoadAddress.txt", "r", encoding="utf-8")
        self.RoadAddressList=[i.split("|") for i in self.f.readlines()]
        self.f.close()
        self.f = open("PythonSource/Util/OldAddress.txt", "r", encoding="utf-8")
        self.OldAddressList=[i.split("|") for i in self.f.readlines()]
        self.f.close()
        pass


    def getAdressList(self,Type=0,Find=0, AddressNum=1, AddressGet=1):
        if Type == ROAD_ADDRESS:
            l = self.SearchAddress(self.RoadAddressList,Type,Find,AddressNum,AddressGet)
        elif Type == OLD_ADDRESS:
            l = self.SearchAddress(self.OldAddressList,Type,Find,AddressNum,AddressGet)
        return l


    def SearchAddress(self,AddressList, Type=0, Find=0, AddressNum=1, AddressGet=1):
        Address=[[]for i in range(2)]
        #도로명 주소 찾기
        if Type == ROAD_ADDRESS:
            if Find != 0:
                if AddressGet == ROAD_FIND_CITY:
                    for i in AddressList:
                        if Find in i[AddressNum]:
                            Address[0].append(i[AddressGet][0:2]); Address[1].append(i[AddressGet])
                            if len(i[AddressNum]) == 4:
                                Address[0].append(i[AddressNum][0:1]+i[AddressNum][2:3]); Address[1].append(i[AddressGet])
                        elif Find in i[AddressNum][0:1]+i[AddressNum][2:3]:
                            Address[0].append(i[AddressGet][0:2]); Address[1].append(i[AddressGet])
                            Address[0].append(i[AddressNum][0:1]+i[AddressNum][2:3]); Address[1].append(i[AddressGet])
                    Address[0]=list(set(Address[0])); Address[1]=list(set(Address[1]))
                    return Address
            
                elif AddressGet == ROAD_FIND_DISTRICT or AddressGet == ROAD_FIND_TOWN:
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
            
                elif AddressGet == ROAD_FIND_ROAD:
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

                elif AddressGet == ROAD_FIND_NUM:
                    Address[0]=list(set([i[AddressGet] for i in AddressList if Find in i[AddressNum]]))
                    return Address
            
                elif AddressGet == ROAD_FIND_ROAD_NUM:
                    for i in AddressList:
                        if Find in i[AddressNum]:
                            m = re.search('\d+',i[ROAD_FIND_ROAD])
                            if m != None:
                                if m.start():
                                    Address[0].append(i[ROAD_FIND_ROAD][m.start():m.end()])
                                    Address[1].append(i[ROAD_FIND_ROAD][m.start():])
                    Address[0]=list(set(Address[0])); Address[1]=list(set(Address[1]))
                    return Address
            
            

            elif Find == 0:
                if AddressGet == ROAD_FIND_CITY:
                    for i in AddressList:
                        if len(i[AddressNum]) == 4:
                            Address[0].append(i[AddressNum][0:1]+i[AddressNum][2:3])
                        Address[0].append(i[AddressGet][0:2]); Address[1].append(i[AddressGet])
                    Address[0]=list(set(Address[0])); Address[1]=list(set(Address[1]))
                    return Address
            
                elif AddressGet == ROAD_FIND_DISTRICT or AddressGet == ROAD_FIND_TOWN:
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
            
                elif AddressGet == ROAD_FIND_ROAD:
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

                elif AddressGet == ROAD_FIND_NUM:
                    Address[0]=list(set([i[AddressGet] for i in AddressList]))
                    return Address
            
                elif AddressGet == ROAD_FIND_ROAD_NUM:
                    for i in AddressList:
                        if Find in i[AddressNum]:
                            m = re.search('\d+',i[ROAD_FIND_ROAD])
                            if m != None:
                                if m.start():
                                    Address[0].append(i[ROAD_FIND_ROAD][m.start():m.end()])
                                    Address[1].append(i[ROAD_FIND_ROAD][m.start():])
                    Address[0]=list(set(Address[0])); Address[1]=list(set(Address[1]))
                    return Address
        
        #지번주소 찾기
        elif Type == OLD_ADDRESS:
            if Find != 0:
                if AddressGet == OLD_FIND_CITY:
                    for i in AddressList:
                        if Find in i[AddressNum]:
                            Address[0].append(i[AddressGet][0:2]); Address[1].append(i[AddressGet])
                            if len(i[AddressNum]) == 4:
                                Address[0].append(i[AddressNum][0:1]+i[AddressNum][2:3]); Address[1].append(i[AddressGet])
                        elif Find in i[AddressNum][0:1]+i[AddressNum][2:3]:
                            Address[0].append(i[AddressGet][0:2]); Address[1].append(i[AddressGet])
                            Address[0].append(i[AddressNum][0:1]+i[AddressNum][2:3]); Address[1].append(i[AddressGet])
                    Address[0]=list(set(Address[0])); Address[1]=list(set(Address[1]))
                    return Address
            
                elif AddressGet == OLD_FIND_DISTRICT or AddressGet == OLD_FIND_TOWN:
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
                
                elif AddressGet == OLD_FIND_VILLAGE:
                    for i in AddressList:
                        if Find in i[AddressNum]:
                            if len(i[AddressGet][:i[AddressGet].rfind("리")]) == 1:
                                Address[0].append(i[AddressGet])
                            else:
                                Address[0].append(i[AddressGet][:i[AddressGet].rfind("리")])
                            Address[1].append(i[AddressGet])
                    
                        Address[0]=list(set(Address[0])); Address[1]=list(set(Address[1]))
                    return Address


            elif Find == 0:
                if AddressGet == OLD_FIND_CITY:
                    for i in AddressList:
                        if len(i[AddressNum]) == 4:
                            Address[0].append(i[AddressNum][0:1]+i[AddressNum][2:3])
                        Address[0].append(i[AddressGet][0:2]); Address[1].append(i[AddressGet])
                    Address[0]=list(set(Address[0])); Address[1]=list(set(Address[1]))
                    return Address
            
                elif AddressGet == OLD_FIND_DISTRICT or AddressGet == OLD_FIND_TOWN:
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
                
                elif AddressGet == OLD_FIND_VILLAGE:
                    for i in AddressList:
                        if len(i[AddressGet][:i[AddressGet].rfind("리")]) == 1:
                            Address[0].append(i[AddressGet])
                        else:
                            Address[0].append(i[AddressGet][:i[AddressGet].rfind("리")])
                        Address[1].append(i[AddressGet])
                    
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
    # ODO 5 : 전북 전남 경북 경남 안됨 => 전북,전남 입력시 전라북도,전라남도 나와야 하고 CITY 출력 시 전라북도 => 전라,전북 모두 나오도록 하기
    # ODO 6 : 지번정보 검색 불가 => 지번도 사용 가능하도록 하기 + 지번과 도로명주소는 동시에 검색되면 안됨 인수로 이를 구분하도록 하기




    '''
    Scarch Example
    CityList=SearchAdress(AddressList,"경상북도")
    >>>>>>> Stashed changes
    print(CityList)
    
    CityList=SearchAdress(AddressList,Find="강서구",AddressNum=ROAD_FIND_DISTRICT,AddressGet=ROAD_FIND_CITY)
    print(CityList)
    
    DistrictList=SearchAdress(AddressList,AddressGet=ROAD_FIND_DISTRICT)
    print(DistrictList)
    
    DistrictList=SearchAdress(AddressList,Find="서울",AddressNum=FIND2CITY,AddressGet=ROAD_FIND_DISTRICT)
    print(DistrictList)
    
    TownList=SearchAdress(AddressList,AddressGet=ROAD_FIND_TOWN)
    print(TownList)
    
    TownList=SearchAdress(AddressList,Find="금산군",AddressNum=FIND2DISTRICT,AddressGet=ROAD_FIND_TOWN)
    print(TownList)
    
    RoadList=SearchAdress(AddressList,AddressGet=ROAD_FIND_ROAD)
    print(RoadList)
    
    RoadList=SearchAdress(AddressList,Find="강동구",AddressNum=FIND2DISTRICT,AddressGet=ROAD_FIND_ROAD)
    print(RoadList)
    
    # NumList=SearchAdress(AddressList,AddressGet=ROAD_FIND_NUM)
    # print(NumList)
    
    NumList=SearchAdress(AddressList,Find="금산군",AddressNum=FIND2DISTRICT,AddressGet=ROAD_FIND_NUM)
    print(NumList)
    '''

a = AddressDB()
print(a.getAdressList(Type=ROAD_ADDRESS,Find="전라",AddressNum=ROAD_FIND_CITY,AddressGet=ROAD_FIND_CITY))
print(a.getAdressList(Type=ROAD_ADDRESS,AddressGet=ROAD_FIND_CITY))
print(a.getAdressList(Type=OLD_ADDRESS,Find="전라",AddressNum=OLD_FIND_CITY,AddressGet=OLD_FIND_CITY))
print(a.getAdressList(Type=OLD_ADDRESS,AddressGet=OLD_FIND_VILLAGE))