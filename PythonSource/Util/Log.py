DEBUG_MODE = False


def i(tag,log="NULL",end = None):
    if end != None:
        print("[INFO] TAG : ",tag, " | LOG : ",str(log),end = end)
    else:
        print("[INFO] TAG : ",tag, " | LOG : ",str(log))


def d(tag,log="NULL",end = None):
    if not DEBUG_MODE:
        return
    if end != None:
        print("[DEBUG] TAG : ",tag, " | LOG : ",str(log),end = end)
    else:
        print("[DEBUG] TAG : ",tag, " | LOG : ",str(log))


def e(tag,log="NULL",end = None):
    if not DEBUG_MODE:
        return
    if end != None:
        print("[ERROR] TAG : ",tag, " | LOG : ",str(log),end = end)
    else:
        print("[ERROR] TAG : ",tag, " | LOG : ",str(log))


def LogUtil_old(tag, log="NULL", end =None):
    if end != None:
        print("TAG : ",tag, " | LOG : ",str(log),end = end)
    else:
        print("TAG : ",tag, " | LOG : ",str(log))
