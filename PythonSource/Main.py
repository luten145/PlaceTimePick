import PythonSource.MainFramework
import PythonSource.UI.UIMain as ui
from PythonSource.UI.UIListener import FrameworkListener

TAG = "TestLabMain"

class ListenerSampleImpl(FrameworkListener):
    def onAnalyzeEvent(self,text) -> bool:
        mainEngine.getAnalyzeData(text)
        return False


uiManager = ui.UIManager(ListenerSampleImpl())
mainEngine = PythonSource.MainFramework.MainEngine()

def main():
    index = 5
    uiManager.onSetDataEvent(index,"This is UI Event Index "+str(index)) # UI 이벤트 테스트 코드
    uiManager.root.mainloop()

    pass

main()