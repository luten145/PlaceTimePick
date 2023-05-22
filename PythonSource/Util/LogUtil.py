def Log(tag,log="NULL",end =None):
    if end != None:
        print("TAG : ",tag, " | LOG : ",str(log),end = end)
    else:
        print("TAG : ",tag, " | LOG : ",str(log))
