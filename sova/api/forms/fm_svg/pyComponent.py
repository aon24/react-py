# -*- coding: utf-8 -*- 
'''
Created on 24 apr 2019.

@author: aon
'''
from .. formTools import style, _div, _field, _button, _btnD, _a, _img, labField

import types

# *** *** ***

def countdown(ru=None):
    '''
@Title: countdown(ru=None)
@Author: AON, aon24@mail.ru
@Created: 2017-05-17
@param: 1 => return Russsian text, otherwise English
'''
    ls = ['дней', 'часов', 'мин', 'сек'] if ru else ['days', 'hours', 'min', 'sec']
    return _div(**style(textAlign='center'), children=[
             _div(children=[_div(t, className='ddhhmmss') for t in ls]),
             _div(id='countdown', children=[ _div(**( style(marginRight=20) if i%2 else style(marginLeft=20) ) ) for i in range(8)]
                  )
            ])
# *** *** ***

lsComp = [ k for k,v in dict(globals()).items() if isinstance(v, types.FunctionType) and v.__module__.endswith('pyComponent')]
