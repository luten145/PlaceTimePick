import re
from PythonSource.Util import Log
from PythonSource.Util import StringUtil
from PythonSource.UI.UIListener import UIEventListener
from PythonSource.UI import UIMain


TAG = "Engine2"

class  TimeData:
    def __init__(self, year = 0, month = 0, day = 0, hour = 0, minute = 0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute


def extractDataData(text_str):
    # 년월일 추출 - 2021년 10월 21일 or 2021.10.21 or 2021/10/21 or 2021-10-21
    ymdPattern = r'(\d{4})(?:년|\.|/|-)(\d{1,2})(?:월|\.|/|-)(\d{1,2})?일?'
    ymdStr = re.search(ymdPattern, text_str)
    if ymdStr:
        year = int(ymdStr.group(1))
        month = int(ymdStr.group(2))
        day = int(ymdStr.group(3))
        return year, month, day, ymdStr.end()
    else:
        return

def extractWeekData(text_str,stratIndex):
    weekPattern = r"\(?(월요일|화요일|수요일|목요일|금요일|토요일|일요일|월|화|수|목|금|토|일)\)?"
    ymdNextText = text_str[stratIndex:]
    try:
        weekStr = re.search(weekPattern, ymdNextText)
        if weekStr:
            weekEndIndex = weekStr.end()
            week = weekStr.group(1)[0]
            return week, weekEndIndex
    except UnboundLocalError:
        Log.e(TAG, "UnboundLocalError")
        return

def extractTimeData(text_str,stratIndex):
    weekNextText = text_str[stratIndex:]
    try: # 시간 추출 - (오전 or 오후 or 낮) + 10시 20분 or 10:20
        timePattern = r"(?:오후|오전|낮)?(\d{1,2})(?::|시)(\d{1,2})?(?:분)?"
        timeStr = re.search(timePattern, weekNextText)
        if timeStr:
            hour = int(timeStr.group(1))
            if '오후' in str(timeStr):
                hour += 12
            minute = int(timeStr.group(2) or 0)
            return hour , minute
    except UnboundLocalError:
        Log.e(TAG, "UnboundLocalError")

class Engine2:
    def __init__(self,uiManager : UIEventListener):
        self.mUIManager = uiManager
        self.textList;
        pass

    def jsonHandler(self,data):
        Log.i(TAG, "Engine2 Start!")
        text_str = StringUtil.getTextString(data)

        print(text_str)

        year, month, day, end = extractDataData(text_str)
        week, end = extractWeekData(text_str,end)
        hour, minute, end = extractTimeData(text_str,end)

        result = TimeData(year,month,week,hour,minute)
        print("----------")
        print("년:", year, type(year))
        print("월:", month, type(month))
        print("일:", day, type(day))
        print("요일:", week, type(week))
        print("시: ", hour, type(hour))
        print("분: ", minute, type(minute))

        self.mUIManager.onSetDataEvent(UIMain.TIME_YEAR,str(year))
        self.mUIManager.onSetDataEvent(UIMain.TIME_MONTH,str(month))
        self.mUIManager.onSetDataEvent(UIMain.TIME_DATE,str(day))
        self.mUIManager.onSetDataEvent(UIMain.TIME_WEEK,str(week))
        self.mUIManager.onSetDataEvent(UIMain.TIME_HOUR,str(hour))
        self.mUIManager.onSetDataEvent(UIMain.TIME_MIN,str(minute))


