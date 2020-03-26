'''
topic.py

Created on 20 apr. 2018

@author: aon
'''
from .. formTools import style, labField, _div, showCode, _field, _table
from .. toolbars import toolbar

# *** *** ***

cssUrl = 'jsv?api/forms/topic/topic.css'
jsUrl = 'jsv?api/forms/topic/topic.js'

# *** *** ***

def page(dbAlias, mode, userName, multiPage):
    if mode in ['read', 'preview']:
        p = _div(
            style={'overflow':'auto', 'maxHeight':'100vh', 'padding': 10},
            children=[
                _div( wl='50mm', className='topic', children=_table(
                    [ _field('title', 'fd', className='h2')], # _field вернет {'field': ['title', 'fd'], 'className': 'h2'}
                    [ _field('content', 'fd', className='article', br='p', style={'whiteSpace':'pre-wrap'})], # разбивать текст на параграфы
                    [ _field('rtf', 'rtf', **style(font='normal 14px Courier', whiteSpace='pre'))],
                    [ _field('json', 'json', **style(font='normal 14px Courier', whiteSpace='pre'))],
                    [ _field('comment', 'fd', className='article', br='p', style={'whiteSpace':'pre-wrap'})], # разбивать текст на параграфы
                )),
            ]
        )
    else:
        p = _div(
            **style(overflow='auto', maxHeight='100vh', maxWidth=1200, padding=10),
            className='page',
            focus='title',
            children=[
                toolbar.rgb(),
                _div( wl='50mm', className='topi-c', children=_table(
                    labField('Раздел', 'title'),
                    [{'field': ('content', 'tx')}],
                    [_div('rtf')],
                    [{'field': ('rtf', 'tx'), 'ttaStyle': {'font': 'normal 14px Courier', 'whiteSpace': 'pre'}}],
                    [_div('json')],
                    [{'field': ('json', 'tx'), 'ttaStyle': {'font': 'normal 14px Courier', 'whiteSpace': 'pre'}}],
                    [{'field': ('comment', 'tx')}],
                    labField('o_level', 'o_level', 'tx'),
                    labField('dir', 'dir', 'tx'),
                    labField('unid', 'unid', 'fd'),
                )),
            ]
        )
    
    return p

# *** *** ***

def queryOpen(d, mode, ground):
    global title
    title = d.title
    
    if mode == 'read':
        d.rtf = showCode(d.rtf)




