#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

key = '74fa492cdb04499b94a9f323b07ccecf'
TOKEN = '7456156502:AAGciRH9_v2YO6N4NIZNGzDT4JL2H-mEGko'
MAX_MSG_LENGTH = 300
baseurl = 'http://openapi.gg.go.kr/FishingPlaceStatus?Key='+key
bot = telepot.Bot(TOKEN)



def getData(loc_param):
    res_list = []
    encoded_loc_param = quote(loc_param)
    url = baseurl+'&pIndex=1'+'&pSize=50'+ '&SIGUN_NM=' + encoded_loc_param
    res_body = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(res_body, 'html.parser')
    items = soup.findAll('row')
    for item in items:
        item = re.sub('<.*?>', '|', item.text)
        parsed = item.split('\n')
        try:
            row = '낚시터 명: '+parsed[5]+', 면적: '+parsed[6]+'ha , 가격: '+parsed[7]+', 도로명주소: '+parsed[9]+ '\n'
        except IndexError:
            row = item.replace('|', ',')

        if row:
            res_list.append(row.strip())
    return res_list

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run(param='가평군'):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user , param)
        res_list = getData( param )
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run(current_month)


