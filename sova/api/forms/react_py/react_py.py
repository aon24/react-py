# -*- coding: utf-8 -*-
'''
Created on 13 февр. 2020 г.

@author: aon24
'''
# *** *** ***

from .. fm_svg.svgTools import svgToPy
from .. formTools import style, _div, _field, _h2, _h3, _btnD, _a

from math import *
import json

jsUrl = 'jsv?api/forms/react_py/react_py.js'
cssUrl = 'jsv?api/forms/react_py/react_py.css'

title = 'react-py'

# *** *** ***

notes = [
'''
<tspan x="10" dy="0.5em" stroke-width="0" font-weight="normal" font-size="14px">
В сложных системах нет мелочей.</tspan>
<tspan x="8" dy="1.5em" stroke-width="0" font-weight="normal" font-size="14px">
При постоянной работе с програм-</tspan>
<tspan x="12" dy="1.5em" stroke-width="0" font-weight="normal" font-size="14px">
мой задержки даже в 1-2 секунды</tspan>
<tspan x="30" dy="1.5em" stroke-width="0" font-weight="normal" font-size="14px">
раздражают. Пример работы</tspan>
<tspan x="40" dy="1.5em" stroke-width="0" font-weight="normal" font-size="14px">
с кэшируемым списком </tspan>
<tspan x="60" dy="1.5em" stroke-width="0" font-weight="normal" font-size="14px">
из 1000 объектов.</tspan>
''',

'''Фреймворк React-py (Sova) это:
<tspan x="30" dy="1.5em">- мост между Python и React</tspan>
<tspan x="30" dy="1.5em">- открытый код</tspan>
<tspan x="30" dy="1.5em">- меньше 300 Кб JS</tspan>
<tspan x="45" dy="1.5em" stroke-width="0" font-weight="normal" font-size="14px">
Python 3.7 / React 16.12</tspan>
<tspan x="65" dy="1.5em" stroke-width="0" font-weight="normal" font-size="14px">
Linux, Windows 7/10 </tspan>
''',

'''
<tspan x="10" dy="0.5em" stroke-width="0" font-weight="normal" font-size="14px">
В сложных системах нет мелочей.</tspan>
<tspan x="8" dy="1.5em" stroke-width="0" font-weight="normal" font-size="14px">
Грамотно организованная система</tspan>
<tspan x="12" dy="1.5em" stroke-width="0" font-weight="normal" font-size="14px">
логгирования облегчает отладку</tspan>
<tspan x="22" dy="1.5em" stroke-width="0" font-weight="normal" font-size="14px">
и сопровождение приложения.</tspan>
<tspan x="40" dy="1.5em" stroke-width="0" font-weight="normal" font-size="14px">
Недаром модуль назван</tspan>
<tspan x="100" dy="1.5em">first.py</tspan>
''',

'''Разработка форм на 2-х экранах
<tspan fill="#048" x="5" dy="1.5em" stroke-width="0" font-weight="normal" font-size="14px">
При редактировании формы</tspan>
<tspan fill="#048" x="10" dy="1.5em" stroke-width="0" font-weight="normal" font-size="14px">
изменения будут отображаться</tspan>
<tspan fill="#048" x="20" dy="1.5em" stroke-width="0" font-weight="normal" font-size="14px">
в реальном времени на всех</tspan>
<tspan fill="#048" x="30" dy="1.5em" stroke-width="0" font-weight="normal" font-size="14px">
подключенных устройствах.</tspan>
<tspan fill="#048" x="50" dy="1.5em" stroke-width="0" font-weight="normal" font-size="14px">
Синхронизация через</tspan>
<tspan fill="#048" x="90" dy="1.5em" stroke-width="1" font-weight="normal" font-size="14px">
WebSocket.</tspan>
''',

'''Пример многооконного прило-
<tspan x="15" dy="2.5em">жения. Вы можете двигать</tspan>
<tspan x="35" dy="2.5em">окна и открывать окна</tspan>
<tspan x="60" dy="2.5em">в новых вкладках.</tspan>
''',

'''
Пример WEB-приложения для
<tspan x="12" dy="1.5em">
смартфона. Заказчик оценил</tspan>
<tspan x="22" dy="1.5em">
на 5+.</tspan>
<tspan fill="#048" x="80" stroke-width="0" font-weight="normal" font-size="14px">
Установка на телефон:</tspan>
<tspan fill="#048" x="30" dy="1.5em" stroke-width="0" font-weight="normal" font-size="14px">
открыть страницу в браузере </tspan>
<tspan fill="#048" x="40" dy="1.5em" stroke-width="0" font-weight="normal" font-size="14px">
и добавить ее на главный</tspan>
<tspan fill="#048" x="50" dy="1.5em" stroke-width="0" font-weight="normal" font-size="14px">
экран.</tspan>
''',
]

def priz():
    cx, cy = 400, 400
    r = 350
    p1 = p2 = p3 = ''
    pi3, pi6 = pi/3, pi/6
    color = ['#efd', '#eee', '#fde', '#edf', '#dfe', '#def']
    for  i in range(6):
        ccx = cx+(r-160)*cos(pi6+pi3*i)
        ccy = cy+(r-160)*sin(pi6+pi3*i)
        tx = cx+(r-10)*cos(pi*0.065+pi3*i)
        ty = cy+(r-10)*sin(pi*0.065+pi3*i)
        tx2 = cx+(r-10)*cos(pi*0.275+pi3*i)
        ty2 = cy+(r-10)*sin(pi*0.275+pi3*i)
        refs = ['/newdoc?&amp;themes', '/newdoc?&amp;home', '/newdoc?&amp;lm',
                '/home-ru', '/newdoc?&amp;mp_spa', '/newdoc?_&amp;schedule']
        text = [
                '___Кэшируемые списки______',
                '_____ Документация _______',
                '_________ Logging ________',
                '_____ Layout manager______',
                '____ Multi-window SPA_____',
                '_____ Почасовая ареда_____',
                ]

        #'/docopen?SOVA/SCHEDULE&amp;20202020202020202020202020202020&amp;edit'
        p1 += f'''
<a href="{refs[i]}" target="_blank">
    <circle cx="{ccx}" cy="{ccy}" r="210" fill="{color[i]}"/>
    <defs><path id="txt1{i}"  d="M {tx},{ty} A 160,160 0 0 1 {tx2},{ty2}"/></defs>
    <defs><path id="txt2{i}"  d="M {tx},{ty} L {tx2},{ty2}"/></defs>
    <text x="0" y="0" style="stroke: #00f; font: normal 20px Times">
      <textPath xlink:href="#txt1{i}">{text[i]}</textPath>
    </text>
    <text x="{0}" y="{0}" style="stroke: #00f; font: normal 20px Times">
        <textPath xlink:href="#txt2{i}"> ________Открыть______</textPath>
    </text>
</a>
'''
    for i in range(6):
        stroke = ['#555', '#555', '#555', '#048', '#00f', '#048']
        tx2 = cx+(r-20)*cos(pi*0.28+pi3*i) if i+3 < 3 else cx+(r-35)*cos(pi*0.02+pi3*i) 
        ty2 = cy+(r-20)*sin(pi*0.28+pi3*i) if i+3 < 3 else cy+(r-35)*sin(pi*0.02+pi3*i)
        tx3 = cx+(r-20)*cos(pi*0.13+pi3*i) if i+3 < 3 else cx+(r-35)*cos(pi*0.312+pi3*i)
        ty3 = cy+(r-20)*sin(pi*0.13+pi3*i) if i+3 < 3 else cy+(r-35)*sin(pi*0.312+pi3*i)
        s = f'fill="{color[i]}" stroke="#fff" stroke-width="1"'
        p1 += f'''<polygon {s} points="{cx+r*cos(pi3*i)},{cy+r*sin(pi3*i)} {cx+r*cos(pi3*(i+1))},{cy+r*sin(pi3*(i+1))} {cx},{cy}"/>
<defs><path id="txt3{i}"  d="M {tx2},{ty2} L {tx3},{ty3}"/></defs>
<text x="{0}" y="{0}" stroke="{stroke[i]}" style="font: normal 16px Arial" letter-spacing="1.2">
  <textPath xlink:href="#txt3{i}">{notes[i]}</textPath>
</text>
'''
    
    p2 += f'''
<circle cx="{cx}" cy="{cy}" r="150" fill="#fff" stroke="#048" stroke-width="1"/>
<circle cx="{cx}" cy="{cy}" r="110" fill="#fed" stroke="#048" stroke-width="1"/>
'''
    
    p2 += f'''
<defs><path id="script1" d="M {cx-126},{cy}  A 126,126 0 0 1 {cx+126},{cy}"/></defs>
<defs><path id="script2" d="M {cx-131},{cy}  A 131,131 0 0 0 {cx+131},{cy}"/></defs>
<defs><path id="python" d="M {cx-80},{cy}  A 80,80 0 0 1 {cx+80},{cy}"/></defs>
<defs><path id="react"  d="M {cx-100},{cy}  A 100,100 0 0 0 {cx+100},{cy}"/></defs>
<text x="20" y="0" style="stroke: #048; font: normal 15px Times" letter-spacing="1.5">
  <textPath xlink:href="#script1">Все приложения разработаны на Python 3.7</textPath>
</text>
<text x="30" y="0" style="stroke: #048; font: normal 15px Times" letter-spacing="1.5">
  <textPath xlink:href="#script2">Javascript общий для всех приложений</textPath>
</text>
<text x="30" y="0" style="stroke: #048; font: normal 30px Times">
  <textPath xlink:href="#python">R e a c t - p y</textPath>
</text>
<text x="50" y="0" style="stroke: #048; font: normal 20px Times">
  <textPath xlink:href="#react">P y t h o n  -  R e a c t </textPath>
</text>'''

    for i in range(12):
        p3 += '<polygon points="0,0 0,0 0,0 0,0" stroke-width="1"/>'

    svg = f'''
<svg width="{2*cx+20}" height="{2*cy}">
    <svg width="{2*cx+20}" height="{2*cy}"><g>{p1}</g></svg>
    <svg width="{2*cx+20}" height="{2*cy}">{p2}</svg>
    <svg width="{2*cx+20}" height="{2*cy}">{p3}</svg>
</svg>'''

    return [ svgToPy(svg) ]

# *** *** ***

def page(dbAlias, mode, userName, multiPage):
    def descr(name, width):
        ds = [
            ['Пример многооконного приложения',
             '''Фремворк основан на принципах объектно-оринтированного программирования. Объекты генерируют и обрабатывают события в стиле <<B+ООП>>, что гораздо проще и понятней, чем <<B:Redux>>. 
             В примере вы можете двигать окна и открывать окна в новых вкладках.\n''',
             '/newdoc?&mp_spa'],
            
            ['Пример WEB-приложения для смартфона',
             '''Заказчик оценил на <<R+5+>>. Установка на телефон:
                - открыть страницу в браузере
                - добавить ее на главный экран.''',
             '/newdoc?_&schedule', '/home-ru'],
                 
            ['Разработка форм на 2-х экранах',
             '''При редактировании формы изменения будут отображаться в реальном времени на всех подключенных устройствах.
             Синхронизация через <<B+WebSocket>>.''',
            '/home-ru'],
        
            ['',
             '''В сложных системах нет мелочей. При постоянной работе с программой задержки даже в 1-2 секунды раздражают.
             Пример работы с кэшируемым списком из 1000 объектов.
             ''',
            '/newdoc?&themes'],

            ['Журнал работы приложения', '''
            В сложных системах нет мелочей. Грамотно организованная система логгирования облегчает отладку и сопровождение приложения.
            Недаром модуль назван <<B+first.py>>''',           
            '/newdoc?&lm'],

            ['','''Описание несколько устарело. Фреймворк постоянно развивается и меняется в сторону упрощения.
            <<C+Пример>>. <<B:React-py>> для прорисовки должен получить словарь:
            \xa0
{'<<R:_teg>>': '<<G+div>>', '<<R:text>>': '<<G+Hello>>-', '<<R:attributes>>': {'<<R:className>>': '<<G+h2>>'},
    \xa0\xa0\xa0\xa0'<<R:children>>': [{'<<R:_teg>>': '<<G+a>>', '<<R:text>>': '<<G+Привет>>',
    \xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0'<<R:attributes>>': {'<<R:href>>': <<G+'http://ya.ru>>', '<<R:style>>': {'<<R:color>>': '<<G+red>>'}}}]
}            
            тот же словарь можно создать с помощью элементарных функций:
\xa0
<<B+_h2>>('<<G+Hello>>-', <<R:children>>=[<<B+_a>>('<<G+Привет>>', <<R:href>>=<<G+'http://ya.ru>>', **<<B+style>>(<<R:color>>='<<G+red>>'))]),
''',
            '/newdoc?&home'],
        ]
        
        return [ _div(name=f'{name}{i+1}', className='descr', **style(width=width),
                    children=[
                        _h2(ds[i][0]),
                        _div(ds[i][1], br='p'),
                        _h2('Hello-', children=[_a('Привет', href='http://ya.ru', **style(color='red'))]) if i == 5 else None,
                        _btnD('Открыть', 'xopen', ds[i][2], className='svTop', **style(width=100, margin='10px auto'))
                    ]
                ) for i in range(6)]

        
    tit = [
        '1. Multi-window SPA',
        '2. Почасовая ареда',
        '3. Layout manager',
        '4. Кэшируемые списки',
        '5. Logging',
        '6. Документация',
    ]

    return _div(
        **style(overflow='auto'),
        children = [
            _h2('Фрейморк React-py ', **style(color='blue')),
            _h3('''7 примеров, разработаных на Python 3.7.
                Во всех приложениях использован один
                Javascript (всего 260 Кб)''', **style(color='#048'), br=1),
            
            _field('chMode_fd', 'chb3', dropList=['презентация|p', 'описание|n'], **style(width=280, font='normal 24px Arial', margin='10px auto'), noEmpty=1),

            _div(name='plain1', className='tbl', children=
                [_btnD(tit[i], f'app1{i+1}', className='nosel', **style(borderBottomWidth=0)) for i in range(3, 6)],
                ),
            _div(name='plain1', className='tbl', **style(width=660, background='#eee'), children=
                [_btnD(tit[i], f'app{i+1}', className=f'{"nosel" if i else "sel"}') for i in range(3)],
                ),

            _div(name='plain2', className='tbl', children=
                [_btnD(tit[i], f'app1{i+1}', className='nosel', **style(borderBottomWidth=0)) for i in range(3)],
                ),
            _div(name='plain2', className='tbl', **style(width=660, background='#eee'), children=
                [_btnD(tit[i], f'app{i+1}', className='nosel') for i in range(3, 6)],
                ),

            _div(name='plain_1', className='tbl', **style(width=360,) , children=
                [_btnD(tit[i], f'app_1{i+1}', className='nosel', **style(borderBottomWidth=0)) for i in range(3, 6)],
                ),
            _div(name='plain_1', className='tbl', **style(width=360, background='#eee'), children=
                [_btnD(tit[i], f'app_{i+1}', className=f'{"nosel" if i else "sel"}') for i in range(3)],
                ),
            _div(name='plain_2', className='tbl', **style(width=360,) , children=
                [_btnD(tit[i], f'app_1{i+1}', className='nosel', **style(borderBottomWidth=0)) for i in range(3)],
                ),
            _div(name='plain_2', className='tbl', **style(width=360, background='#eee'), children=
                [_btnD(tit[i], f'app_{i+1}', className='nosel') for i in range(3, 6)],
                ),


            *descr('descr', 660),
            *descr('descr_', 360),

            _field('polygon_fd', 'json', **style(width=400, margin='auto', textAlign='center')),

            _field('screen_fd', 'chb3', name='priz', dropList=['смартфон|s', 'компьютер|p'], **style(width=250, margin='10px auto'), noEmpty=1),
        ])
    
# *** *** ***

def queryOpen(d, mode, ground):
    d._polygon = json.dumps(priz(), ensure_ascii=False)
    d.chMode_fd = 'p'

# *** *** ***











