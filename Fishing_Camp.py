from tkinter import *
import tkinter.ttk
import requests
import xml.etree.ElementTree as ET
from PIL import Image, ImageTk, ImageSequence
from datetime import datetime
from tkintermapview import TkinterMapView
import mysmtplib
from email.mime.text import MIMEText
from tkinter import messagebox
import spam
import telepot

import noti

# 공공데이터 API 키
api_key = "74fa492cdb04499b94a9f323b07ccecf"
# 경기도 낚시터 정보 API
url = "https://openapi.gg.go.kr/FishingPlaceStatus"

weather_api_key = 'PmlKfXizyTi+o6XMWSpMAxJy4WgAMfRvHWBrxnN49hfkHMjcFPbR0zxx6BT7KqmPMzt3e/fYhBhqJa5OdcWEFQ=='
weather_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'

# global value
host = "smtp.gmail.com"  # Gmail STMP 서버 주소.
port = "587"

senderAddr = "leejunho3288@gmail.com"  # 보내는 사람 email 주소.
passwd = spam.getPasswd()

class MainGUI:

    def open_email_window(self):
        selected_index = self.fishingCampListBox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "낚시터를 선택해주세요!")
            return

        self.emailWindow = Toplevel(self.frame1)
        self.emailWindow.title("이메일 입력")
        self.emailWindow.geometry("300x125")  # 창 크기 설정
        self.emailWindow.configure(bg='#E0FFFF')  # 배경 색 설정

        Label(self.emailWindow, text="수신자 이메일", font=("Consolas", 15, "bold"),fg='#2F4F4F', bg='#E0FFFF').pack(pady=10)
        self.emailEntry = Entry(self.emailWindow, font=("Consolas", 12), width=30)  # 글씨 크기와 엔트리 크기 설정
        self.emailEntry.pack(pady=5)

        Button(self.emailWindow, text="Send", command=self.send_mail).pack()

    def send_mail(self):
        selected_index = self.fishingCampListBox.curselection()
        if selected_index:
            selected_camp = self.fishingCamps[selected_index[0]]
            info_text = (
                f"이름: {selected_camp['name']}\n"
                f"면적(ha): {selected_camp['area']}\n"
                f"가격(원): {selected_camp['price']}\n"
                f"주소: {selected_camp['address']}\n"
                f"위도: {selected_camp['lat']}\n"
                f"경도: {selected_camp['lng']}\n"
            )
        else:
            messagebox.showerror("Error", "낚시터를 선택해주세요!")
            return
        recipientAddr = self.emailEntry.get()
        if not recipientAddr:
            messagebox.showerror("Error", "이메일을 입력해주세요!")
            return
        msg = MIMEText(info_text)
        msg['Subject'] = "FishingCamp 낚시터 정보"
        msg['From'] = senderAddr
        msg['To'] = recipientAddr
        try:
            s = mysmtplib.MySMTP(host, port)
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(senderAddr, passwd)
            s.sendmail(senderAddr, [recipientAddr], msg.as_string())
            s.close()
            messagebox.showinfo("Success", "이메일 전송 성공!")
            self.emailWindow.destroy()  # 성공적으로 보낸 후 창을 닫음
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {e}")

    def set_weather_text(self):
        weather_summary = {
            'POP': None,
            'TMP': None,
            'SKY': None
        }
        for item in self.weathers:
            category = item['category']
            if category in weather_summary:
                weather_summary[category] = item['fcstValue']

        # 하늘 상태 값을 해석
        sky_state = {
            '1': '맑음',
            '3': '구름많음',
            '4': '흐림'
        }
        sky_text = sky_state.get(weather_summary['SKY'], '알 수 없음')

        # 텍스트 변환
        self.weather_text_output = (
            f"강수확률: {weather_summary['POP']}%\n"
            f"1시간 기온: {weather_summary['TMP']}℃\n"
            f"하늘 상태: {sky_text}"
        )

    def get_weather_info(self, nx, ny):
        # 현재 날짜와 시간
        now = datetime.now()
        base_date = now.strftime('%Y%m%d')
        base_time = now.strftime('%H00')

        # 요청 파라미터
        params = {
            "serviceKey": weather_api_key,
            "pageNo": 1,
            "numOfRows": 1000,
            "base_date": base_date,
            'base_time': '0500',
            'nx': nx,
            'ny': ny
        }

        # API 요청
        response = requests.get(weather_url, params=params)

        # 응답 확인 및 파싱
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            rows = root.findall(".//item")
            self.weathers = []
            for item in rows:
                fcst_date = item.find('fcstDate').text
                fcst_time = item.find('fcstTime').text

                # 현재 날짜와 시간의 정각과 일치하는 항목 필터링
                if fcst_date == base_date and fcst_time == base_time:
                    weather_info = {
                        'baseDate': item.find('baseDate').text,
                        'baseTime': item.find('baseTime').text,
                        'category': item.find('category').text,
                        'fcstDate': item.find('fcstDate').text,
                        'fcstTime': item.find('fcstTime').text,
                        'fcstValue': item.find('fcstValue').text,
                        'nx': item.find('nx').text,
                        'ny': item.find('ny').text
                    }
                    self.weathers.append(weather_info)
            print(self.weathers)

        else:
            print(f"Error: {response.status_code}")
            return None

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
        self.areas = []
        for row in rows:
            fishingCamp = {
                "name": row.findtext("FISHPLC_NM"),  # 낚시터 이름
                "address": row.findtext("REFINE_ROADNM_ADDR"),  # 낚시터 도로명 주소
                "lat": row.findtext("REFINE_WGS84_LAT"),  # 위도
                "lng": row.findtext("REFINE_WGS84_LOGT"),  # 경도
                "area": row.findtext("FISHPLC_AR"),     # 낚시터 면적
                "price": row.findtext("UTLZ_CHRG"),  # 가격
            }
            self.areas.append(float(row.findtext("FISHPLC_AR")))
            self.fishingCamps.append(fishingCamp)

    def on_combobox_select(self, event):
        selected_gu = self.selected_gu.get()
        print(f"Selected: {selected_gu}")
        self.getFishingCampList(selected_gu)
        self.update_fishing_camp_listbox()
        self.update_fishing_camp_graph()

    def update_fishing_camp_listbox(self):
        self.fishingCampListBox.delete(0, END)
        for camp in self.fishingCamps:
            self.fishingCampListBox.insert(END, camp["name"])

    def update_fishing_camp_graph(self):
        self.areaCanvas.delete('graph')
        max_area = max(self.areas)
        bar_width = 20
        x_gap = 30
        x0 = 30
        y0 = 250

        canvas_width = x0 + len(self.areas) * (bar_width + x_gap)
        self.areaCanvas.config(scrollregion=(0, 0, canvas_width, 400))

        for i in range(len(self.areas)):
            x1 = x0 + i * (bar_width + x_gap)
            y1 = y0 - 200 * self.areas[i] / max_area
            self.areaCanvas.create_rectangle(x1, y1, x1 + bar_width, y0, fill='blue', tags='graph')
            self.areaCanvas.create_text(x1 + bar_width / 2 - 3, y0 + 75, text=self.fishingCamps[i]['name'], anchor='n',
                                        angle=90, tags='graph', font=('Consolas', 8))
            self.areaCanvas.create_text(x1 + bar_width / 2, y1 - 10, text=str(self.areas[i]), anchor='s', tags='graph',
                                        font=('Consolas', 10))

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
            if selected_camp['lat'] != '':
                lat = eval(selected_camp['lat'])
                lng = eval(selected_camp['lng'])
                self.star_map_widget.set_position(lat, lng, text=selected_camp['name'])
                self.star_map_widget.set_marker(lat, lng, text=selected_camp['name'])

    def on_listbox_select(self, event):            # 즐겨찾기 리스트 정보 표시
        selected_index = self.fishingCampListBox.curselection()
        if selected_index:
            selected_camp = self.fishingCamps[selected_index[0]]
            info_text = (
                f"이름: {selected_camp['name']}\n"
                f"면적(ha): {selected_camp['area']}\n"
                f"가격(원): {selected_camp['price']}\n"
                f"주소: {selected_camp['address']}\n"
                f"위도: {selected_camp['lat']}\n"
                f"경도: {selected_camp['lng']}\n"
            )
            self.info_label.config(text=info_text)
            if selected_camp['lat'] != '':
                lat = eval(selected_camp['lat'])
                lng = eval(selected_camp['lng'])
                self.map_widget.set_position(lat, lng, text=selected_camp['name'])
                self.map_widget.set_marker(lat, lng, text=selected_camp['name'])


    def pressdStar(self):
        selected_index = self.fishingCampListBox.curselection()
        if selected_index:
            selected_camp = self.fishingCamps[selected_index[0]]
            if selected_camp not in self.starredCamps:
                self.starredCamps.append(selected_camp)
                camp_name = selected_camp["name"]
                self.starFishingCampListBox.insert(END, camp_name)

    def pressdMail(self):
        self.open_email_window()

    def pressdInfo(self):
        # 좌측에 있는 지역 리스트를 숨김
        self.fishingCampListBox.place_forget()
        self.homeimage=PhotoImage(file='resource/home.gif')

        # info 버튼을 다시 눌렀을 때 기존의 UI를 복구하기 위한 함수를 바인딩
        self.Info.config(image=self.homeimage,text='home', command=self.restore_info)

    def restore_info(self):
        # 좌측에 지역 리스트를 다시 보이도록 설정
        self.fishingCampListBox.place(x=50, y=150)
        self.searchimage = PhotoImage(file='resource/search.gif')
        # info 버튼을 다시 눌렀을 때 원래 기능으로 돌아가도록 설정
        self.Info.config(image=self.searchimage, text='Info', command=self.pressdInfo)

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

    def animate_gif(self):
        try:
            frame = next(self.gif_frames)
            self.gif_label.config(image=frame)
            self.frame1.after(100, self.animate_gif)
        except StopIteration:
            self.gif_frames = iter(self.gif_images)
            self.animate_gif()

    def animate_gif_note2(self):
        try:
            frame = next(self.gif_frames_note2)
            self.gif_label_note2.config(image=frame)
            self.frame2.after(100, self.animate_gif_note2)
        except StopIteration:
            self.gif_frames_note2 = iter(self.gif_images_note2)
            self.animate_gif_note2()

    def setNoteOne(self):
        self.frame1 = Frame(self.window, bg='#E0FFFF')
        self.notebook.add(self.frame1, text='홈')

        original_image = Image.open('resource/fishing.gif')
        self.gif_images = []
        for frame in ImageSequence.Iterator(original_image):
            resized_frame = frame.resize((285, 100), Image.LANCZOS)
            self.gif_images.append(ImageTk.PhotoImage(resized_frame))
        self.gif_frames = iter(self.gif_images)

        self.gif_label = Label(self.frame1)
        self.gif_label.place(x=50, y=10)
        self.animate_gif()

        # 좌측에 정보를 출력할 라벨 생성
        self.info_label = Label(self.frame1, text="낚시터를 선택해주세요", font=("Consolas", 15), bg='#E0FFFF',
                                fg='#2F4F4F', wraplength=250)
        self.info_label.place(x=50, y=150)

        # 시군 선택 콤보박스 생성

        self.gu_combo = tkinter.ttk.Combobox(self.frame1, textvariable=self.selected_gu, values=list(self.gu_options))
        self.gu_combo.place(x=50, y=120)
        self.gu_combo.bind("<<ComboboxSelected>>", self.on_combobox_select)

        # 낚시터 리스트 박스
        self.fishingCampListBox = Listbox(self.frame1, width=26, height=17, font=("Consolas", 15), bg='#ADD8E6')
        self.fishingCampListBox.place(x=50, y=150)
        self.fishingCampListBox.bind("<<ListboxSelect>>", self.on_listbox_select)

        # 지도
        self.map_widget = TkinterMapView(width=350, height=350, corner_radius=0)
        self.map_widget.place(x=400, y=120)

        # 즐겨 찾기 버튼
        self.starimage = PhotoImage(file='resource/bookmark.gif')
        self.Star = Button(self.frame1,image=self.starimage, text="Star", width=100, height=100, bg='#ADD8E6', command=self.pressdStar)
        self.Star.place(x=370, y=450)

        # 메일 버튼
        self.mailimage = PhotoImage(file='resource/mail.gif')
        self.Mail = Button(self.frame1, image=self.mailimage,text="Mail", width=100, height=100, bg='#ADD8E6', command=self.pressdMail)
        self.Mail.place(x=520, y=450)

        # 돋보기 버튼
        self.searchimage = PhotoImage(file='resource/search.gif')
        self.Info = Button(self.frame1, image= self.searchimage, text="Info", width=100, height=100, bg='#ADD8E6', command=self.pressdInfo)
        self.Info.place(x=670, y=450)

        # 우측 상단에 정보를 출력할 라벨 생성
        self.weather_label = Label(self.frame1, text=self.weather_text_output, font=("Consolas", 15),
                                   bg='#E0FFFF', fg='#2F4F4F', anchor='ne', justify='right')
        self.weather_label.place(x=500, y=10)


    def setNoteTwo(self):
        self.frame2 = Frame(self.window, bg='#E0FFFF')
        self.notebook.add(self.frame2, text='즐겨찾기')

        original_image_note2 = Image.open('resource/fishing.gif')
        self.gif_images_note2 = []
        for frame in ImageSequence.Iterator(original_image_note2):
            resized_frame = frame.resize((285, 100), Image.LANCZOS)
            self.gif_images_note2.append(ImageTk.PhotoImage(resized_frame))
        self.gif_frames_note2 = iter(self.gif_images_note2)

        self.gif_label_note2 = Label(self.frame2)
        self.gif_label_note2.place(x=50, y=10)
        self.animate_gif_note2()

        # 낚시터 리스트 박스
        self.starFishingCampListBox = Listbox(self.frame2, width=26, height=15, font=("Consolas", 15), bg='#ADD8E6')
        self.starFishingCampListBox.place(x=50, y=120)
        self.starFishingCampListBox.bind("<<ListboxSelect>>", self.on_star_listbox_select)

        # 지도
        self.star_map_widget = TkinterMapView(self.frame2, width=350, height=300, corner_radius=0)
        self.star_map_widget.place(x=400, y=20)


        # 낚시터 정보 라벨
        self.starFishingCampInfo = Label(self.frame2, font=("Consolas", 15), bg='#E0FFFF', fg='#2F4F4F', wraplength=250)
        self.starFishingCampInfo.place(x=475, y=330)
        self.starFishingCampInfo.config(text="낚시터 정보를 선택하세요")

        # 즐겨찾기 삭제 버튼
        self.deleteimage = PhotoImage(file='resource/delete.gif')
        self.Delete = Button(self.frame2, image=self.deleteimage, text="Delete", bg='#ADD8E6', width=280, height=60, command=self.pressdDelete)
        self.Delete.place(x=50, y=500)

    def setNoteThree(self):
        frame3 = Frame(self.window, bg='#E0FFFF')
        self.notebook.add(frame3, text='면적 그래프')
        Label(frame3, text='면적 그래프', fg='#2F4F4F', font=('Consolas', 30), bg='#E0FFFF').pack()  # 짙은 남색 텍스트

        self.gu_comboThree = tkinter.ttk.Combobox(frame3, textvariable=self.selected_gu, values=list(self.gu_options))
        self.gu_comboThree.pack()
        self.gu_comboThree.bind("<<ComboboxSelected>>", self.on_combobox_select)

        self.canvas_frame = Frame(frame3)
        self.canvas_frame.pack(fill=BOTH, expand=True)

        self.h_scrollbar = Scrollbar(self.canvas_frame, orient=HORIZONTAL)
        self.h_scrollbar.pack(side=BOTTOM, fill=X)

        # 시군 콤보 박스 생성

        # 그래프 canvas 생성
        self.areaCanvas = Canvas(self.canvas_frame, width=780, height=400, bg='#ADD8E6',
                                 xscrollcommand=self.h_scrollbar.set)
        self.areaCanvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.h_scrollbar.config(command=self.areaCanvas.xview)

        self.areaLabel = Label(frame3,text='단위(ha)',fg='#2F4F4F', font=('Consolas', 15), bg='#E0FFFF')
        self.areaLabel.pack(side=RIGHT)


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
        self.get_weather_info(37, 127)
        self.set_weather_text()
        self.notebook = tkinter.ttk.Notebook(self.window, width=800, height=600)

        self.fishingCamps = []
        self.starredCamps = []

        self.setNoteOne()
        self.setNoteTwo()
        self.setNoteThree()

        self.show_splash_screen()

        import teller
        import noti
        self.bot = teller.telepot.Bot(noti.TOKEN)
        self.bot.message_loop(teller.handle)

        self.window.mainloop()





MainGUI()

