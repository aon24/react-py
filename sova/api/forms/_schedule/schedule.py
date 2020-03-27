# -*- coding: utf-8 -*-
'''
Created on 16.05.2018

@author: aon
'''
from .. .. api.forms.formTools import style, _div, _field, _table, label, labField, _btnD, _a, _br
from .... dbToolkit.Book import getDocByUnid, getDB, createDB, dbExists
from .... util.common import well, toWell, accessDenied, DC, today
from .... util.first import snd, err
from .... util.checkRights import notEditor

import datetime
import time
import json
# import mysql.connector
import pymysql as mysql
from hashlib import md5

cssUrl = 'jsv?api/forms/schedule/schedule.css'
jsUrl  = 'jsv?api/forms/schedule/schedule.js'
title = 'Owl'
rooms = {}

# *** *** ***
_morning = 11 # 11:00 начало бронироаания
_evening = 21 # 21:00 конец бронирование (бронь 21:00-22:00)
_workTime = _evening - _morning + 1
# *** *** ***

titleRoom = ['35 маленькая|little-rooms', '37 маленькая|little-rooms', '42 маленькая|little-rooms', '43 маленькая|little-rooms', '46 маленькая|little-rooms', '48 маленькая|little-rooms',
             '36 средняя|middle-rooms', '38 средняя|middle-rooms',
             '310 большая|large-rooms', '41 большая|large-rooms', '44 большая|large-rooms', '45 большая|large-rooms', 
            ]
nRooms = len(titleRoom)
month = ['', 'Январь', 'Февраль','Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
mLen = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
rId = {}
database = ''
_line = _div(**style(border='solid 0 #aaa', borderBottomWidth=1, width=350, margin='10px auto'))

# *** *** ***

class DB(object):
    def __init__(self):
        global database
        try:
            database = 'aon24mel_bs'
            self.con = mysql.connect(host='127.0.0.1', port=3306, user='root', passwd='24', database=database, charset='utf8')
#             self.con = mysql.connect(host='127.0.0.1', port=3306, user='root', passwd='utHYQCRRibWpKVu', database=database, charset='utf8')
        except:
            database = 'xxx'
            self.con = mysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', database=database, charset='utf8')
        self.cursor = self.con.cursor()

def loadUser(login):
    fi = 'id, name, mail, phone, password'
    s = f"SELECT {fi} FROM tbl_users WHERE mail='{login}' AND our=1;"
    try:
        db = DB()
        db.cursor.execute(s)
        for row in db.cursor: # nnosikova@yandex.ru
            dc = DC()
            dc.dname = 'NV'
            dc.uid, dc.userName, dc.login, dc.phone, password = row
            dc.password = md5(f'{dc.login}:sova.online:{password}'.encode()).hexdigest()
            toWell(dc, 'login', dc.login)
            toWell(dc, 'userName', f'{dc.userName}/{dc.dname}')
            return dc
    except Exception as ex:
        err(f"Exception. login='{login}'\n{ex}", cat='schedule.py.loadUser')
        
def getRoomsId():
    db = DB()
    db.cursor.execute('SELECT * FROM tbl_rooms')
    
    for row in db.cursor:
        rn = row[2].partition(' ')[0]
        for i in range(nRooms):
            if rn == titleRoom[i].partition(' ')[0]:
                titleRoom[i] += '|' + str(row[0])
                rId[str(row[0])] = rn
                break 

# *** *** ***

def loadMonth(dKey, userName):
    cat = 'schedule.py.loadMonth()'
    roomId, mm, yy = dKey.split('_')

    m1 = int(mm)
    y1 = y2 = int(yy)
    
    if m1 == 2 and not (y1 % 4):
        lenM = 29
    else:
        lenM = mLen[m1]
            
    m1 -= 1
    m2 = m1 + 2
    if m1 < 0:
        m1 = 12
        y1 -= 1
    if m2 > 12:
        m2 = 1
        y2 += 1

    fi = 'from_date, to_date, state, name, event, contacts, admin_comments'
    s = f"SELECT {fi} FROM tbl_roomsshedule where from_date >= '{y1}-{m1:02}-01' AND from_date < '{y2}-{m2:02}-01' AND room={roomId};"
    db = DB()
    db.cursor.execute(s)
    
    dt1 = datetime.datetime(int(yy), int(mm), 1)
    
    ls = ['F']*31*_workTime
    for row in db.cursor:
#         print( '---'.join([ str(x) for x in row ]) )
        if row[0] >= row[1]:
            err(f'время начала >= времени конца(ауд:{rId[roomId]}): {row[0]} {row[1]}', cat=cat)
            continue

        status, userName, notes, phone, vid = [x or '' for x in row[2:7]]
        if row[1] < dt1 or status not in ['Бронь подтверждена', 'Занята']:
            continue
# При заказе через сайт не "нашим" пользователем устанавливается статус "Забронирована".
# Потом администратор переводит статус заказа в "Бронь подтверждена", а в личном кабинете появляется возможность оплатить.
# После оплаты устанавливается статус "Занята".
# Если заказывает "наш" пользователь (этим пользователем не нужно оплачивать) - сразу ставится статус "Занята".       

        dayBegin, hourBegin = row[0].date().day, row[0].hour
        dayEnd, hourEnd = row[1].date().day, row[1].hour
        
        if hourBegin < _morning:
            err(f'время вне дисапазона(ауд:{rId[roomId]}): from_date={row[0]}', cat=cat)
            hourBegin = _morning
        if hourBegin > _evening:
            err(f'время вне дисапазона(ауд:{rId[roomId]}): from_date={row[0]}', cat=cat)
            hourBegin = _evening
        if hourEnd < _morning + 1:
            err(f'время вне дисапазона(ауд:{rId[roomId]}): to_date={row[1]}', cat=cat)
            hourEnd = _morning + 1
        if hourEnd > _evening + 1:
            err(f'время вне дисапазона(ауд:{rId[roomId]}): to_date={row[1]}', cat=cat)
            hourEnd = _evening + 1
            
        dayBegin2 = dayBegin
        while dayBegin2 <= dayEnd:
            hourBegin2 = hourBegin if dayBegin2 == dayBegin else _morning
            hourEnd2 = hourEnd if dayBegin2 == dayEnd else _evening + 1
            while hourBegin2 < hourEnd2:
                # дни слева направо (ряд), часы сверху вниз (столбец)
                try:
                    stat = 'U' if vid.startswith('Учебный') else 'A' if vid else 'M'
                    ls[(hourBegin2 - _morning)*lenM + dayBegin2-1] = [stat, f'{userName}\n{phone}', notes]
                except Exception as ex:
                    err(f'begin:{dayBegin} {hourBegin}, end:{dayEnd} {hourEnd}, i={(hourBegin2 - _morning)*lenM + dayBegin2-1}\n{ex}', cat=cat)
                hourBegin2 += 1
            dayBegin2 += 1
            
    return 200, 'application/json', json.dumps(ls, ensure_ascii=False)

# *** *** ***
getRoomsId()
snd(f'Connect to "{database}" successful', cat='MySQL')

# for i in range(16):
#     loadMonth(f'qq&{i+1}_07_2019')
# *** *** ***

def page(dbAlias, mode, userName, multiPage):
    now = datetime.datetime.now()
    m = now.month
    year = now.year
    
    m14 = {}
    j = 0
    _all = 0

    for i in range(-1, 9):
        k = m + i
        y = year
        if k <= 0:
            k += 12
            y -= 1
        elif k > 12:
            k -= 12
            y += 1
        if k == 2 and not (y % 4):
            l = 29
        else:
            l = mLen[k]

        m14[j] = [{'rowStyle': {'textAlign': 'center'}}]
        for r in range(nRooms):
            r1, r2, rommId = titleRoom[r].replace(' ', '\xa0').split('|')
            _all += 1
            if 'маленькая' in r1:
                typ = 'M'
            elif 'средняя' in r1:
                typ = 'S'
            elif 'большая' in r1:
                typ = 'B'
            m14[j].append(_field(f'sch_{_all}', 'sch', name=f'sch_{_all}', showCol=f'{j+1}', btn=l, header=f'{r1}|http://institutnv.ru/{r2}|{typ}|{month[k]}\xa0{y}|{rommId}_{k}_{y}'))
        j += 1

    main = [
            _btnD('Загрузить все сразу', 'al', className='btn', **style(margin=5)),
            ]
    mar = 5
    main += [_div(children=[
            _btnD('М-', 'm', className='btn', **style(margin=mar)),
            _btnD('М+', 'ml', className='btn', **style(margin=mar)),
            _btnD('С-', 's', className='btn', **style(margin=mar)),
            _btnD('С+', 'sl', className='btn', **style(margin=mar)),
            _btnD('МС-', 'ms', className='btn', **style(margin=mar)),
            _btnD('МС+', 'msl', className='btn', **style(margin=mar)),
            _btnD('Б-', 'b', className='btn', **style(margin=mar)),
            _btnD('Б+', 'bl', className='btn', **style(margin=mar)),
        ])
    ]
    
    main.append(_div('Вид брони и комментарий (значения по умолчанию):', **style(font='bold 9pt Arial', color='#048')))
    main += [_div(**style(width=390, margin='5px auto'), children=[
                _field('status_fd', 'chb3', dropList=['уч. проц.|u', 'аренда|a'], **style(float='left'), noEmpty=1),
                _field('notes_fd', **style(width=160, display='inline-block')),
                ])
        ]
    main += [
            _div(**style(width=350, margin='auto'), children=[
                _div('выбрать дату', **style(verticalAlign='top', width=100, font='bold 9pt Arial', color='#048', display='inline-block', padding='3px 5px 0 0')),
                _field('date_fd', 'dt', **style(width=125, display='inline-block')),
                _btnD('Показать', 'chDate', className='btn'),
                ]),
        ]
    
    x = []
    for r in m14:
        x += m14[r]
    main += [_div(**style(display='table', margin='auto'), children=x),
                 _line,
                 _btnD('Мои заказы', 'myHours', className='btn', **style(marginBottom=10)), _br(),
                 _field('date1_fd', 'dt', **style(width=125, display='inline-block')),
                 label('\xA0-- ', **style(display='inline-block')),
                 _field('date2_fd', 'dt', **style(width=125, display='inline-block')),
                 _field('myHours', 'json'),
                 _field('screen_fd', 'chb3', dropList=['смартфон|s', 'компьютер|p'], **style(width=250, margin='10px auto'), noEmpty=1),
                 _a('Журнал', href='newdoc?&lm', target='_blank'),
                 _line,
            ]

    return _div( **style(overflow='auto', textAlign='center', height='100vh'), children=main)

# *** *** ***

def queryOpen(d, mode, ground):
    d.show_FD = 2
    d.nRooms_FD = nRooms
    d.cellProps_fd = json.dumps(cellProps(), ensure_ascii=False)
    d.status_fd = 'a'
    d.screen_fd = 's'
    d._page_ = '1'
    d.date1_fd = today()
    d.myHours = json.dumps([_line], ensure_ascii=False)

# *** *** ***

def myHours(par, userName):
    cat = 'schedule.py.querySave'
    uName, _, ip = userName.partition('::')
    un1, _, dn1 = uName.partition('/')
    tm1, _, tm2 = par.partition('&')
    tm1 += ' 00:00:00'
    tm2 = (tm2 or '2100-01-01') + ' 23:59:59'
    tbl = 'tbl_roomsshedule'

    myHo = {}

    fi = 'id, state, name, event, from_date, to_date, room, admin_comments'
    s = f"SELECT {fi} FROM {tbl} WHERE from_date >= '{tm1}' AND from_date <= '{tm2}';"
    db = DB()
    db.cursor.execute(s)
    for row in db.cursor:
        un2, _, dn2 = row[2].partition('/') # имя автора изменений без домена, dname
        roomId = str(row[6])
        if un1 == un2 and rId.get( roomId ):
            dt = row[4].date()
            tm = row[4].strftime('%H.%M') + roomId
            myHo[dt] = myHo.get(dt, {})
            myHo[dt][tm] = myHo[dt].get(tm, {})
            myHo[dt][tm] = list(row) + [ rId[roomId] ]
            
    if myHo:
        js = []
        for dd in sorted(myHo):
            js.append( _div(dd.strftime('%d.%m.%Y'), **style(textAlign='left', color='#840', font='bold 12px Verdana')) )
            hours = []
            for hh in sorted(myHo[dd]):
                hours.append(_btnD('удалить', 'delHour', str(myHo[dd][hh][0]), className='ma btn2') )
                hours.append( label(myHo[dd][hh][4].strftime('%H.%M')) )
                hours.append( label('- ' + myHo[dd][hh][5].strftime('%H.%M')) )
                hours.append( label('Аудитория ' + myHo[dd][hh][8], **style(color='#00f')) )
                hours.append( label(' ('+str(myHo[dd][hh][1]) + ')', **style(color='#084')) )
                hours.append( _div(str(myHo[dd][hh][7]) + ' (' + (str(myHo[dd][hh][3]) or '-') + ')',
                    **style(font='normal 10px Verdana', border='solid 0 #def', borderBottomWidth=1, textAlign='left')) )
#                 hours.append(_div(hh.strftime('%H.%M'), **style(textAlign='left', color='#048', font='bold 10px Verdana')))
            js.append(_div(children=hours))
            js.append(_line)
    else:
        js = [_div('Список пуст')]
    snd(f'с {tm1} по {tm2} ({userName})', cat='Мои заказы')
    return 200, None, json.dumps([_div(**style(width=350, margin='auto'), children=js)], ensure_ascii=False)

# *** *** ***

def delHour(idb, userName):
    cat='Изменения в расписании'
    tbl = 'tbl_roomsshedule'
    fi = 'room, from_date, to_date'
    sql = f"SELECT {fi} FROM {tbl} WHERE id={idb};"
    db = DB()
    db.cursor.execute(sql)
    for row in db.cursor:
        sql = f"DELETE FROM {tbl} WHERE id={idb};"
        log =  f': ауд. {rId[str(row[0])]} {row[1]} {row[2]} ({userName})'
        return runSQL(db, sql, cat, f'Удалено{log}')
    else:
        err(f'Запись не найдена id={idb}', cat=cat)
        return 404,

# *** *** ***
    
def saveHour(dKey, newValue, userName):
    cat = 'schedule.py.saveHour'
    uName, _, ip = userName.partition('::')
    state, _, notes = newValue.replace("'", "''").partition('|')
    try:
        user = well('userName', uName)
        uid = user.uid
        phone = user.phone
    except:
        uid = 0
        if userName == 'Designer/SOVA::127.0.0.1':
            phone = '8-7654321'
        else:
            err(f'invalid user: {userName}', cat=cat)
            return 400, None, 'invalid user'

    roomId, mm, yy, dd, hh, force = dKey.replace("'", "").split('_') # 12_8_2019_31_21
    hh2 = str(int(hh) + 1)
    tm = f'{yy}-{mm.zfill(2)}-{dd.zfill(2)} {hh.zfill(2)}:00:00'
    tm2 = f'{yy}-{mm.zfill(2)}-{dd.zfill(2)} {hh2.zfill(2)}:00:00'

    vid = 'Аренда' if state.lower() == 'a' else 'Учебный процесс'
    log = f': ауд. {rId[roomId]} {dd.zfill(2)}.{mm.zfill(2)}.{yy} {hh.zfill(2)}:00 ({vid}, {userName}, {notes})'
    
    tbl = 'tbl_roomsshedule'
    fi = 'id, state, name, event'
    s = f"SELECT {fi} FROM {tbl} WHERE from_date <= '{tm}' AND to_date > '{tm}' AND room={roomId};"
    db = DB()
    db.cursor.execute(s)
    for row in db.cursor:
        un2 = row[2].partition('/')[0] # имя автора изменений без домена
        s = str(row[3]).lower().strip()
        ena = un2 == 'Новый Век' and (not s or 'отпуск' in s)
        if un2 == uName.partition('/')[0] or ena:
            if state == 'F':    # удалить запись
                sql = f"DELETE FROM {tbl} WHERE id={row[0]};"
                return runSQL(db, sql, cat, f'Удалено{log}')

        elif row[1] in ['Бронь подтверждена', 'Занята'] and not force:
            db.cursor.close()
            db.con.close()
            s = 'КОНФЛИКТ ПРИ СОХРАНЕНИИ'
            err(s, cat=cat)
            return 409, None, s
            
        sql = f"UPDATE {tbl} SET state='Занята', name='{uName}', contacts='{phone}', event='{notes}', admin_comments='{vid}' WHERE id={row[0]}" 
        return runSQL(db, sql, cat, f'Изменено{log}')

    sql =f"""
        INSERT INTO {tbl}
            (room, from_date, to_date, state, name, contacts, event, admin_comments, user, ip)
        VALUES
            ({roomId}, '{tm}', '{tm2}', 'Занята', '{uName}', '{phone}', '{notes}', '{vid}', '{uid}', '{ip}');"""
    
    if state == 'F': # нет такой записи, нечего удалять
        db.cursor.close()
        db.con.close()
        return 200,
    
    return runSQL(db, sql, cat, f'Добавлено{log}')
    
# *** *** ***
    
def runSQL(db, sql, cat, log):
    try:
        db.cursor.execute(sql)
        db.con.commit()
        db.cursor.close()
        db.con.close()
        snd(log, cat='Изменения в расписании')
        return 200,
    except Exception as ex:
        db.con.rollback()
        db.cursor.close()
        db.con.close()
        s = f'Ошибка при записи в базу данных:\n{ex}'
        err(s, cat=cat)
        return 403, None, s

# *** *** ***

def cellProps():
    return [
        [   _div(className='cellbg-green', **style(borderBottom='2px solid #fff'), children=
              [ 
                _field('status', 'chb3', dropList=['уч. проц.|u', 'аренда|a'],
                       **style(width='99%', margin='3px auto')),
                *labField('Комментарий', 'notes', **style(padding=3, height=45, overflow='auto'), br=1),
                *labField('Забронировал', 'userName', **style(padding=3), readOnly=1),
              ]),
        ],
    ]

# *** *** ***










