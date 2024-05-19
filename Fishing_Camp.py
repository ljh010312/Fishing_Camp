from tkinter import *
import tkinter.ttk
import requests
import xml.etree.ElementTree as ET
from PIL import Image, ImageTk

# 공공데이터 API 키
api_key = "74fa492cdb04499b94a9f323b07ccecf"
# 경기도 낚시터 정보 API
url = "https://openapi.gg.go.kr/FishingPlaceStatus"

class MainGUI:
    def getFishingCampList(self, SIGUN):
        params = {
            "Key": api_key,
            "pIndex": 1,
            "pSize": 50,
            "SIGUN_NM": SIGUN,
        }
        response = requests.get(url, params=params)

        root = ET.fromstring(response.content)
        rows = root.findall(".//row")

        self.fishingCamps = []
        for row in rows:
            fishingCamp = {
                "name": row.findtext("FISHPLC_NM"),  # 낚시터 이름
                "address": row.findtext("REFINE_ROADNM_ADDR"),  # 낚시터 도로명 주소
                "lat": row.findtext("REFINE_WGS84_LAT"),  # 위도
                "lng": row.findtext("REFINE_WGS84_LOGT"),  # 경도
                "area": row.findtext("FISHPLC_AR"),     # 낚시터 면적
                "price": row.findtext("UTLZ_CHRG"),  # 가격
        }
            self.fishingCamps.append(fishingCamp)

    def on_combobox_select(self, event):
        selected_gu = self.selected_gu.get()
        print(f"Selected: {selected_gu}")
        self.getFishingCampList(selected_gu)
        self.update_fishing_camp_listbox()

    def update_fishing_camp_listbox(self):
        self.fishingCampListBox.delete(0, END)
        for camp in self.fishingCamps:
            self.fishingCampListBox.insert(END, camp["name"])

    def on_star_listbox_select(self, event):            # 즐겨찾기 리스트 정보 표시
        selected_index = self.starFishingCampListBox.curselection()
        if selected_index:
            selected_camp = self.starredCamps[selected_index[0]]
            info_text = (
                f"이름: {selected_camp['name']}\n"
                f"면적(ha): {selected_camp['area']}\n"
                f"가격(원): {selected_camp['price']}\n"
                f"주소: {selected_camp['address']}\n"
                f"위도: {selected_camp['lat']}\n"
                f"경도: {selected_camp['lng']}\n"
            )
            self.starFishingCampInfo.config(text=info_text)

    def pressdStar(self):
        selected_index = self.fishingCampListBox.curselection()
        if selected_index:
            selected_camp = self.fishingCamps[selected_index[0]]
            if selected_camp not in self.starredCamps:
                self.starredCamps.append(selected_camp)
                camp_name = selected_camp["name"]
                self.starFishingCampListBox.insert(END, camp_name)

    def pressdMail(self):
        pass

    def pressdInfo(self):
        pass

    def pressdDelete(self):
        selected_index = self.starFishingCampListBox.curselection()
        if selected_index:
            # 선택된 낚시터의 인덱스 가져오기
            index_to_delete = selected_index[0]
            # 즐겨찾기 리스트에서 해당 인덱스의 낚시터 정보 삭제
            del self.starredCamps[index_to_delete]
            # 즐겨찾기 리스트 박스에서도 해당 항목 삭제
            self.starFishingCampListBox.delete(index_to_delete)
            # 삭제 후 라벨에 표시된 정보 초기화
            self.starFishingCampInfo.config(text="낚시터 정보를 선택하세요")

    def setNoteOne(self):
        frame1 = Frame(self.window, bg='#E0FFFF')
        self.notebook.add(frame1, text='홈')

        original_image = Image.open('resource/logo.gif')
        resized_image = original_image.resize((285, 100), Image.LANCZOS)
        self.gif_image = ImageTk.PhotoImage(resized_image)

        label_with_image = Label(frame1, image=self.gif_image)
        label_with_image.place(x=50, y=10)

        # 시군 선택 콤보박스 생성

        self.gu_combo = tkinter.ttk.Combobox(frame1, textvariable=self.selected_gu, values=list(self.gu_options))
        self.gu_combo.place(x=50, y=120)
        self.gu_combo.bind("<<ComboboxSelected>>", self.on_combobox_select)

        # 낚시터 리스트 박스
        self.fishingCampListBox = Listbox(frame1, width=26, height=17, font=("Consolas", 15),bg='#FFFFFF')
        self.fishingCampListBox.place(x=50, y=150)


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
        frame2 = Frame(self.window, bg='#E0FFFF')
        self.notebook.add(frame2, text='즐겨찾기')

        label_with_image = Label(frame2, image=self.gif_image)
        label_with_image.place(x=50, y=10)

        # 낚시터 리스트 박스
        self.starFishingCampListBox = Listbox(frame2, width=26, height=15, font=("Consolas", 15), bg='#FFFFFF')
        self.starFishingCampListBox.place(x=50, y=120)
        self.starFishingCampListBox.bind("<<ListboxSelect>>", self.on_star_listbox_select)


        # 낚시터 정보 라벨
        self.starFishingCampInfo = Label(frame2, font=("Consolas", 15), bg='#E0FFFF', fg='#2F4F4F', wraplength=250)
        self.starFishingCampInfo.place(x=475, y=350)
        self.starFishingCampInfo.config(text="낚시터 정보를 선택하세요")

        # 즐겨찾기 삭제 버튼
        self.Delete = Button(frame2, text="Delete", width=40, height=3, command=self.pressdDelete)
        self.Delete.place(x=50, y=500)

    def setNoteThree(self):
        frame3 = Frame(self.window, bg='#E0FFFF')
        self.notebook.add(frame3, text='면적 그래프')
        Label(frame3, text='면적 그래프', fg='#2F4F4F', font=('Consolas', 30), bg='#E0FFFF').pack()  # 짙은 남색 텍스트

        # 시군 콤보 박스 생성
        self.gu_combo = tkinter.ttk.Combobox(frame3, textvariable=self.selected_gu, values=list(self.gu_options))
        self.gu_combo.pack()

        # 그래프 canvas 생성
        self.areaCanvas = Canvas(frame3, width=700, height=400, bg='#FFFFFF')
        self.areaCanvas.pack()

        self.areaCanvas.create_rectangle(2,2, 700, 400)

    def show_main_screen(self):
        self.splash_frame.destroy()
        self.notebook.pack()

    def show_splash_screen(self):
        self.splash_frame = Frame(self.window)
        self.splash_frame.pack(fill='both', expand=True)
        original_image = Image.open('resource/logo.gif')
        resized_image = original_image.resize((800, 600), Image.LANCZOS)
        self.splash_image = ImageTk.PhotoImage(resized_image)

        splash_label = Label(self.splash_frame, image=self.splash_image,width=800, height=600)
        splash_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # ms뒤에 홈화면
        self.window.after(1, self.show_main_screen)

    def __init__(self):
        self.window = Tk()
        self.window.title('Fishing Camp')
        self.window.geometry("800x600")
        self.window.configure(bg='#E0FFFF')  # 밝은 청록색 배경
        self.selected_gu = StringVar()
        self.selected_gu.set("가평군")  # 초기값 설정
        self.gu_options = ['가평군', '고양시', '광명시', '광주시', '구리시', '군포시', '김포시', '남양주시', '부천시', '수원시', '시흥시', '안산시', '안성시',
                           '안양시',
                           '양주시', '양평군', '여주시', '연천군', '오산시', '용인시', '의왕시', '의정부시', '이천시', '파주시', '평택시', '포천시', '하남시',
                           '화성시']
        self.notebook = tkinter.ttk.Notebook(self.window, width=800, height=600)

        self.fishingCamps = []
        self.starredCamps = []

        self.setNoteOne()
        self.setNoteTwo()
        self.setNoteThree()

        self.show_splash_screen()

        self.window.mainloop()


MainGUI()