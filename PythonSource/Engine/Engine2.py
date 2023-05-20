import re
from tkinter import *
from konlpy.tag import Kkma
import PythonSource.Util.DicApi as dicApi
from PythonSource.Util import LogUtil as logUtil
from PythonSource.UI.UIListener import UIEventListener
from PythonSource.UI import UIMain
from PythonSource.Util import AddressDB
from PythonSource.Util import StringUtil

TAG = "Engine2"

class Engine2:
    # TODO : migration to individual file
    def __init__(self,uiManager : UIEventListener):
        self.mUIManager = uiManager
        pass

    def jsonHandler(self,data):
        self.mUIManager.onSetDataEvent(1,"HELLO ENGINE2")
        logUtil.Log(TAG,"dataIN!!")
        # data is json File
        # json 파일 내에 text 키의 값들만 읽어서 하나의 리스트로 만들기
        text_list = data["task_result"]["text"]
        combined_text = "".join(text_list)
        text = [combined_text]

        text_list=str(text).split('\\n')
        text_str=str(text).replace("\\n"," ")
        print(text_list)
        print(text_str)
        print()
        print()

        placePattern = ["홀", "웨딩", "장례"]
        place = [item for item in text_list if any(re.search(p, item) for p in placePattern)]
        print(place)


