import json
from tkinter import filedialog
from tkinter import messagebox

class JsonManager:
    def showFileManager(self):
        list_file = []      #파일 목록 담을 리스트 생성
        files = filedialog.askopenfilenames(initialdir="/", \
                                            title = "파일을 선택 해 주세요", \
                                            filetypes = (("*.txt","*txt"),("*.xls","*xls"),("*.csv","*csv")))
        #files 변수에 선택 파일 경로 넣기
        if files == '':
            messagebox.showwarning("경고", "파일을 추가 하세요")    #파일 선택 안했을 때 메세지 출력

        print(files)    #files 리스트 값 출력
        with open(files[0], 'r', encoding='utf-8') as f:
            data3 = json.load(f)

        return data3