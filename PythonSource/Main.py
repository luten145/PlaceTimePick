import PythonSource.Engine.EngineManager as engineManager
import PythonSource.UI.UIMain as ui
from PythonSource.UI.UIListener import FrameworkListener
import PythonSource.Util.JsonUtil as jsonUtil

TAG = "TestLabMain"

jsonManager = jsonUtil.JsonManager()



class ListenerSampleImpl(FrameworkListener):
    def onTkinterEvent(self, text) -> bool:
        mainEngine.tkinterHandler(text)
        return False
    def onJsonOpenEvent(self) -> bool:
        data = jsonManager.showFileManager()
        mainEngine.jsonHandler(data)
        return False

uiManager = ui.UIManager(ListenerSampleImpl())
mainEngine = engineManager.MainEngine(uiManager.getDataEventListener())

def main():
    index = 5
    listener = uiManager.getDataEventListener()
    listener.onSetDataEvent(index, "This is UI Event Index " + str(index)) # UI 이벤트 테스트 코드
    uiManager.root.mainloop()
    pass

main()