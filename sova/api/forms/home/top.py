# -*- coding: utf-8 -*- 
'''
Created on 18 . 04 . 2018 

@author: aon
'''
from .. formTools import style, _div, _img, _a, _btnD
from .... util.common import well

import sys

def panel():
    return [
        _div ('С о в а', className='sova'),
        
        _div (**style(display='block'), children=[
#             _div('Новый стек технологий. Интерактивная разработка на нескольких устройствах', **style(paddingLeft=175)),

            _div(className='topnav', children=[
                _btnD('LM', 'newDoc', 'RF.AKK.MOTIHOR.PSNR/FM_2019&fm_manager&1', title='Layout manager (repository of forms)'),
                _btnD('log', 'newDoc', '&lm', title='Application log'),
                _btnD('about', 'about'),
                _btnD('habr', 'xopen', 'https://habr.com/ru/post/424779/', title='outdated description'),
                _btnD('logoff', 'logoff'),
            ]),
            
            _div(**style(display='table-row', width='calc(100% - 152px)'), children=[
                _div('\nSova-online\nMulti-page SPA\nReact-py', className='hello', s2=2, br='br', **style(display='table-cell')),
                _div('''<<B+React-py (Сова)>> - это мост между <<B:Python>> и <<B:React>>, позволяющий создавать многооконные приложения с многоролевой бизнес-логикой и сложными формами. Движок на <<B:ReactJS>> отрисует разметку, созданную на <<B:Python>>.
                        <<B+React-py>> - это инструмент для замены толстых клиентов на приложения, работающие через браузер.''',
#                     <<B:Графический редактор форм>> позволяет в реальном времени оценивать результат одновременно <<B:на нескольких>> компьютерах/планшетах/смартфонах.''',
                    **style(display='table-cell', width='55%', textAlign='justify', fontSize=14, textIndent=20), br='p'),

                _div(**style(display='table-cell', width='18%', paddingLeft=30), children=[
                        _img('image?python.ico', **style(width=16), href='https://www.python.org'),
                        _a(f' Python {sys.version.split()[0]}', href='https://www.python.org'),
                        _div(' ', **style(width=130, height=45, margin='3px 0', boxShadow='inset 0 0 10px 5px #fff',
                            backgroundImage='url(image?bridge.jpg)', backgroundSize='100%')),
                        _img('image?react.ico', **style(width=16), href='https://reactjs.org'),
                        _a(' React 16.12.0', id='reactVer', href='https://reactjs.org'),
                    ]),
            ])
        ])
    ]
