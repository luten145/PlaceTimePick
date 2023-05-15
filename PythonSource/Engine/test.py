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

FIND_CITY="경상북도"
FIND_DISTRICT="영천시"
FIND_TOWN="화산면"
FIND_ROAD="신정길"
FIND_NUM="60"

f = open("Address.txt", "r", encoding="utf-8")
AddressList=[i.split("|") for i in f.readlines()]
f.close()

CityList=SearchAdress(AddressList,FIND_CITY)
print(CityList)
DistrictList=SearchAdress(CityList,FIND_DISTRICT,1)
print(DistrictList)
TownList=SearchAdress(DistrictList,FIND_TOWN,2)
print(TownList)
RoadList=SearchAdress(TownList,FIND_ROAD,3)
print(RoadList)
NumList=SearchAdress(RoadList,FIND_NUM,4)
print(NumList)

print("test")
print("tesst2")
