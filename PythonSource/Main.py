from PythonSource.UI import UIMain
from PythonSource.UI.UIListener import FrameworkListener
from PythonSource.Util import JsonUtil
from PythonSource.Engine import EngineManager

TAG = "TestLabMain"

jsonManager = JsonUtil.JsonManager()


class UIListener(FrameworkListener):
    def onTkinterEvent(self, text) -> bool:
        mainEngine.tkinterHandler(text)
        return False

    def onJsonOpenEvent(self) -> bool:
        data = jsonManager.showFileManager()
        mainEngine.jsonHandler(data)
        return False


uiManager = UIMain.UIManager(UIListener())
mainEngine = EngineManager.MainEngine(uiManager.getDataEventListener())


def main():
    index = 5
    listener = uiManager.getDataEventListener()
    listener.onSetDataEvent(index, "This is UI Event Index " + str(index))  # UI 이벤트 테스트 코드
    uiManager.root.mainloop()


main()
