# -*- coding: utf-8 -*-
'''
Created on 21 mar 2018

@author: aon
'''
from .dbToolkit.Book import getDB, createDB
from .util.common import well, toWell, DC, tryDecode, liform
from .loadRog import loadRog

from hashlib import md5

# *** *** ***

# регистрация пользователя Guest/SOVA (лгин: 1, пароль: 1)
for i in range(10000):
    dc = DC()
    dc.userName = f'Guest-{i}'
    dc.dname = 'SOVA'
    dc.login = str(i)
    dc.password   = md5(f'{dc.login}:sova.online:{i}'.encode()).hexdigest()
    toWell(dc, 'login', dc.login)

# *** *** ***

toWell('sova.', 'app')
toWell('sova/', 'path')

toWell(DC( {'dName': 'SOVA'} ), 'profile', 'SOVA/SITE')
toWell(DC( {'dName': 'SOVA'} ), 'profile', 'RF.AKK.MOTIHOR.PSNR/FM_2019')
toWell(DC( {'dName': 'SOVA'} ), 'profile', 'SOVA/SCHEDULE')
toWell(DC( {'dName': 'SOVA'} ), 'profile', 'RS/ROG')

toWell({'default': 'reader'}, 'acr', 'SOVA/SITE')
toWell({'default': 'reader'}, 'acr', 'RF.AKK.MOTIHOR.PSNR/FM_2019')
toWell({'default': 'editor'}, 'acr', 'SOVA/SCHEDULE')

toWell('SOVA/SITE', 'MAIN', 'BOOK')
toWell('SOVA/SCHEDULE', 'SCHEDULE')

loadRog('RS/ROG')

s = '''Албертсон Алла Аскольдовна
Бок-Розов Павел Халиуллович
Даглас Мила Тимуровна
Иванов Иван Иванович
Кэри Илона Макаровна
Петров Петр
Петров Ульрих Владимирович
Сидоров
администрация МО Аронский район
администрация МО Центральный район
администрация МО Южный район'''

toWell(s.split('\n'), 'whoForDN', 'SOVA')
s = '''Бок-Розов Павел Халиуллович
Даглас Мила Тимуровна
Кэри Илона Макаровна
Ульрих Петр Владимирович'''
toWell(s.split('\n'), 'whoSign', 'SOVA')

s = '''Рассмотрение руководителем
Ответственный исполнитель
Ответственный исполнитель (свод)
Ответственный исполнитель + соисполнители
Соисполнитель
Отправка через МЭДО
Рассмотрение руководителем (соисполнитель)'''
toWell(s.split('\n'), 'classifier', 'Направлено')

s = '''Свод + соисп.|Ответственный исполнитель (свод)
Отв. исп.|Ответственный исполнитель
Соисп.|Соисполнитель
Скрыт. соисп.|Соисполнитель'''
toWell(s.split('\n'), 'classifier', 'Направлено (проект)')

s = '''Для сведения
К сведению
Для работы
Для соответствующей работы
Для рассмотрения и подготовки ответа в указанный срок
Для рассмотрения и подготовки ответа заявителю в срок _CCDA_
Для рассмотрения и подготовки ответа в срок _CCDA_'''
toWell(s.split('\n'), 'Резолюции', 'ОГ')

s = '''Разъяснено
Меры приняты
Поддержано
Не поддержано
Оставлено без ответа автору'''
toWell(s.split('\n'), 'Результат обращения', 'ОГ')

_pa = 'sova/api/react.js/%s.html'
for s in ['index', 'download', 'topic', 'content', 'rreport', 'habr']:
    try:
        with open(_pa % s, 'rb') as f:
            _fo = DC()
            _fo.html = tryDecode(f.read())[0]
            toWell(_fo, 'otherForms', s)
    except:
        pass
        
# *** *** ***

coll = getDB(well('MAIN', 'BOOK')).allDocuments()
content = ''
                                                             
for d in coll:
    if d.form.endswith('topic'):
        def repGt(fi):
            for s in ['<<B:', '<<B+', '<<G:', '<<G+', '<<R:', '<<R+', '<<C+', '>>' ]:
                fi = fi.replace(s, ' ')
            return fi.replace('>', '&GT;').replace('<', '&LT;').replace('\n', '<br>')
    
        html = liform('topic', 'html') % (d.title, repGt(d.content), repGt(d.rtf), repGt(d.comment))
        toWell(html, 'topic', d.unid)
        content += '<br><a href="topic?%s">%s</a>' % (d.unid, d.title)

habr = repGt(liform('habr', 'html'))
toWell('%s<div>%s</div>' % (content, habr), 'content')

# *** *** ***

try:
    with open('webSocketServer.txt', 'rt') as f:
        ws_server, _, p = f.read().partition(':')
        ws_port = int(p)
        toWell( f'{ws_server}:{ws_port}', 'webSocketServer' )
except Exception as ex:
    ws_server = ws_port = None

if ws_server:
    try:
        import threading
        from sova.api.forms.fm_svg.web_socket import wsServer 
        threading.Thread(target=wsServer, args=(ws_port,)).start()
    except:
        pass

