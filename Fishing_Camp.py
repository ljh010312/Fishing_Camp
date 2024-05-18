#pip install pillow
#pip install googlemaps
#pip install requests
import tkinter as tk
import tkinter.ttk as ttk
import requests
import xml.etree.ElementTree as ET
from PIL import Image, ImageTk
import io
from googlemaps import Client

zoom = 13

# 공공데이터 API 키
api_key = "74fa492cdb04499b94a9f323b07ccecf"

# 서울시 구별 병원 정보 데이터
url = "https://openapi.gg.go.kr/FishingPlaceStatus"
params = {
    "Key": api_key,
    "pIndex": 1,
    "pSize": 50,
    "SIGUN_CD": 41280,
}
response = requests.get(url, params=params)

root = ET.fromstring(response.content)
rows = root.findall(".//row")

fisingCamps = []
for row in rows:
    fisingCamp = {
        "name": row.findtext("FISHPLC_NM"),  # 병원 이름
        "address": row.findtext("REFINE_ROADNM_ADDR"),  # 병원 주소
        "lat": row.findtext("REFINE_WGS84_LAT"),  # 위도
        "lng": row.findtext("REFINE_WGS84_LOGT"),  # 경도
        "price": row.findtext("UTLZ_CHRG"),  # 가격
}
    fisingCamps.append(fisingCamp)


print(fisingCamps)


