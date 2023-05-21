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

a = 0
f = open("./Util/RoadAddress.txt", "r", encoding="utf-8")

RoadAddressL = [i.split("|") for i in f.readlines()]
f.close()
f = open("./Util/RoadAddress.txt", "r", encoding="utf-8")
OldAddressL = [i.split("|") for i in f.readlines()]
f.close()

class AddressDB:

    def __init__(self):
        self.RoadAddressList=RoadAddressL
        self.OldAddressList=OldAddressL
        pass


    def getAdressList(self,Find=0, AddressNum=1, AddressGet=1,Type=0):
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

a = AddressDB()
print(a.getAdressList(Type=ROAD_ADDRESS,Find="전남",AddressNum=ROAD_FIND_CITY,AddressGet=ROAD_FIND_DISTRICT))
