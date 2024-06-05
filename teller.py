#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

import noti


def replyAptData(user, loc_param='가평군'):
    print(user, loc_param)
    res_list = noti.getData(loc_param)
    msg = ''
    for r in res_list:
        print( str(datetime.now()).split('.')[0], r )
        if len(r+msg)+1> noti.MAX_MSG_LENGTH:
            noti.sendMessage(user, msg)
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        noti.sendMessage(user, msg)
    else:
        noti.sendMessage(user, '지역을 제대로 입력해주세요')

def save( user, loc_param ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    try:
        cursor.execute('INSERT INTO users(user, location) VALUES ("%s", "%s")' % (user, loc_param))
    except sqlite3.IntegrityError:
        noti.sendMessage(user, '이미 해당 정보가 저장되어 있습니다.')
        return
    else:
        noti.sendMessage(user, '저장되었습니다.')
        conn.commit()

def check( user ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    cursor.execute('SELECT * from users WHERE user="%s"' % user)
    for data in cursor.fetchall():
        row = 'id:' + str(data[0]) + ', location:' + data[1]
        noti.sendMessage(user, row)


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('정보') and len(args) > 1:
        print('try to 정보', args[1])
        replyAptData(chat_id, args[1])
    else:
        noti.sendMessage(chat_id, '모르는 명령어입니다.\n정보 [지역이름] 명령을 입력하세요.')




