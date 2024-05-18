from tkinter import *
import tkinter.ttk
import requests
import xml.etree.ElementTree as ET


#
# # 공공데이터 API 키
# api_key = "74fa492cdb04499b94a9f323b07ccecf"
#
# # 경기도 낚시터 정보 API
# url = "https://openapi.gg.go.kr/FishingPlaceStatus"
# params = {
#     "Key": api_key,
#     "pIndex": 1,
#     "pSize": 50,
#     "SIGUN_NM": '가평군',
# }
# response = requests.get(url, params=params)
#
# root = ET.fromstring(response.content)
# rows = root.findall(".//row")
#
# fishingCamps = []
# for row in rows:
#     fishingCamp = {
#         "name": row.findtext("FISHPLC_NM"),  # 낚시터 이름
#         "address": row.findtext("REFINE_ROADNM_ADDR"),  # 낚시터 도로명 주소
#         "lat": row.findtext("REFINE_WGS84_LAT"),  # 위도
#         "lng": row.findtext("REFINE_WGS84_LOGT"),  # 경도
#         "area": row.findtext("FISHPLC_AR"),     # 낚시터 면적
#         "price": row.findtext("UTLZ_CHRG"),  # 가격
# }
#     fishingCamps.append(fishingCamp)

class MainGUI:

    def pressdStar(self):
        pass

    def pressdMail(self):
        pass

    def pressdInfo(self):
        pass

    def setNoteOne(self):
        frame1 = Frame(self.window)
        self.notebook.add(frame1, text='홈')
        Label(self.window, text='Fishing Camp', fg='black', font='helvetica 20').place(x=50, y=50)

        # 시군 선택 콤보박스 생성
        self.selected_gu = StringVar()
        self.selected_gu.set("가평군")  # 초기값 설정
        self.gu_options = ['가평군', '고양시', '광명시', '광주시', '구리시', '군포시', '김포시', '남양주시', '부천시', '수원시', '시흥시', '안산시', '안성시', '안양시',
                      '양주시', '양평군', '여주시', '연천군', '오산시', '용인시', '의왕시', '의정부시', '이천시', '파주시', '평택시', '포천시', '하남시', '화성시']
        self.gu_combo = tkinter.ttk.Combobox(frame1, textvariable=self.selected_gu, values=list(self.gu_options))
        self.gu_combo.place(x=50, y=150)

        # 낚시터 리스트 박스
        self.fishingCampListBox = Listbox(frame1, width=40, height=23)
        self.fishingCampListBox.place(x=50, y=200)


        # 지도
        #추가 해야함

        # 즐겨 찾기 버튼
        self.Star = Button(frame1, text="Star", width=15, height=7, command=self.pressdStar)
        self.Star.place(x=370, y=450)

        # 메일 버튼
        self.Mail = Button(frame1, text="Mail", width=15, height=7, command=self.pressdMail)
        self.Mail.place(x=520, y=450)

        # 돋보기 버튼
        self.Info = Button(frame1, text="Info", width=15, height=7, command=self.pressdInfo)
        self.Info.place(x=670, y=450)

    def setNoteTwo(self):
        frame2 = Frame(self.window)
        self.notebook.add(frame2, text='즐겨찾기')
        Label(frame2, text='Fishing Camp', fg='black', font='helvetica 20').place(x=50, y=30)

        # 낚시터 리스트 박스
        self.starFishingCampListBox = Listbox(frame2, width=45, height=30)
        self.starFishingCampListBox.place(x=50, y=100)

        # 낚시터 정보 라벨
        self.starFishingCampInfo = Label(frame2, font=("Consolas", 20))
        self.starFishingCampInfo.place(x=400, y=100)
        self.starFishingCampInfo.config(text=f"낚시터 이름: \n"
                               f"면적: \n"
                               f"가격: \n"
                               f"위치: \n"
                               f"날씨: ")

    def __init__(self):
        self.window = Tk()
        self.window.title('Fishing Camp')
        self.notebook = tkinter.ttk.Notebook(self.window, width=800, height=600)
        self.notebook.pack()

        self.setNoteOne()
        self.setNoteTwo()




        frame3 = Frame(self.window)
        self.notebook.add(frame3, text='면적 그래프')
        Label(frame3, text='페이지3의 내용', fg='orange', font='helvetica 48').pack()

        self.window.mainloop()


MainGUI()