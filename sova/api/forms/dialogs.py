# -*- coding: utf-8 -*- 
'''
AON 20 mar 2019

'''
from . formTools import style, _div, labField, _field, label, _br
try:
    from common import toWell
except:
   from ... util.common import toWell

# *** *** ***
lsBgType = ['Видео (free from wix.com)|video','Рисунок|img','Цвет|color',]
lsVideo = ['Аполлон|image?Apollon.mp4', 'море|image?sea.mp4', 'волны|image?waves.mp4', '123']
lsPict = ['url(/image?owl_.png)',
          'url(/image?U_Mariani_3.jpg)',
          'url(/image?U_Mariani_4.jpg)',
          'url(/image?bg51.jpg)',]
toWell( lsVideo, 'bgValue', 'video')
toWell( lsPict, 'bgValue', 'img')
toWell( ['white', '#def'], 'bgValue', 'color')
lsFt = [
        'text|tx',
        'date|dt',
        'droplist single disable|lbsd',
        'droplist multi disable|lbmd',
        'droplist single enable|lbse',
        'droplist multi enable|lbme',
        'checkbox|chb',
        'fileShow|fileShow',
        'list|list',
        'for display only|fd',
        'view|view',
        'json|json',
        'rtf|rtf',
        'table|table',
        'checkbox3|chb3',
    ]

def pageProps():
    return [
        [_div(className='cellbg-green', **style(borderBottom='2px solid #fff'), children=[
            _div(children=[{'rowClassName': 'row'},
                _div(children=[*labField('formName', 'formName', **style(padding=3))]),
                _div(children=[*labField('Title', 'title', **style(padding=3))]),
                ])
            ]
        )],
        [_div(className='cellbg-green', **style(borderBottom='2px solid #fff'), children=[ 
            _div(children=[{'rowClassName': 'row'},
                _div(children=[*labField('category',
                                         'cat',
                                         'lbse',
                                          dropList='api.get?loadDropList&lsCat',
                                          small=1,
                                          **style(padding=3))]),
                _div(children=[*labField('subcategory',
                                         'subCat',
                                         'lbse',
                                          dropList='CAT|||api.get?loadDropList&lsCat|{FIELD}',
                                          small=1,
                                          **style(padding=3))
                    ])
                ])
            ]
        )],
        [_div(className='cellbg-green', **style(borderBottom='2px solid #fff'), children=[
            _div(children=[{'rowClassName': 'row'},
                  _div(children=[*labField('background-type', 'bgType', 'lbse', dropList=lsBgType, alias=1, small=1, **style(padding=3))]),
                  _div(children=[*labField('background-value', 'bgValue', 'lbse', dropList='BGTYPE|||api.get?loadDropList&bgValue|{FIELD}', alias=1, small=1, **style(padding=3))])
                ])
            ]
        )],
        [_div(className='cellbg-green', **style(borderBottom='2px solid #fff'), children=[
                *labField('javaScriptUrl', 'javaScriptUrl', **style(padding=3)),
                *labField('cssUrl', 'cssUrl', **style(padding=3))
            ]
        )],
        [_div(className='cellbg-green', name='cls', **style(height=200), children=[
                *labField('className', 'className', **style(padding=3)),
                *labField('style', 'style', **style(padding=3,  overflow='auto', height=120))
            ]
        )],
    ]

# *** *** ***

def fieldProps():
    return [
        [_div(className='cellbg-green', **style(borderBottom='2px solid #fff'), children=[
            _div(children=[{'rowClassName': 'row'},
                _div(children=[*labField('fieldName', 'fn', **style(padding=3))]),
                _div(children=[*labField('name', 'name', **style(padding=3))]),
                ])
            ]
        )],
        [_div(className='cellbg-green', **style(borderBottom='2px solid #fff'), children=[
            _div(children=[{'rowClassName': 'row'},
                _div(children=[*labField('fieldType', 'ft', 'lbsd', lsFt, alias=1, **style(padding=3))]),
                _div(children=[*labField('dropList', 'dropList', **style(padding=3))]),
                ]),
            _div(children=[*labField('param (delimiter ";")', 'param', **style(padding=3))])
            ]
        )],
        [_div(className='cellbg-green', **style(height=70), children=[
                _div(children=[*labField('className (parent div)', 'className', **style(padding=3))]),
                *labField('style (parent div)', 'style', **style(padding=3,  overflow='auto', height=52))
            ]
        )],
        [_div(className='cellbg-green', **style(height=70), children=[
                _div(children=[*labField('className (textarea)', 'ttaClassName', **style(padding=3))]),
                *labField('style (textarea)', 'ttaStyle', **style(padding=3,  overflow='auto', height=52))
            ]
        )],
        [_div(className='cellbg-green', name='label', **style(height=90), children=[
                _div(children=[*labField('label', 'label', **style(padding=3))]),
                _div(children=[*labField('className (label)', 'labelClassName', **style(padding=3))]),
                *labField('style (label)', 'labelStyle', **style(padding=3, overflow='auto', height=52))
            ]
        )],
    ]

# *** *** ***

def compProps():
    return [
        [_div(className='cellbg-green', **style(height=225, borderBottom='2px solid #fff'), children=[
                *labField('Python function', 'text', **style(padding=3), readOnly=1),
                *labField('__doc__', '_doc_', **style(padding=3, height=140), readOnly=1, br=1, overflow='auto'),
            ]
        )],
        [_div(className='cellbg-green', **style(height=185), children=[
                *labField('param *p (p1, p2...)', 'param', **style(padding=3, overflow='auto')),
                *labField('param **kv (k1=v1, k2=v2...)', 'paramKV', **style(padding=3, overflow='auto', height=100))
            ]
        )],
    ]
# *** *** ***

def tegProps():
    return [
        [_div(className='cellbg-green', **style(height=225, borderBottom='2px solid #fff'), children=[
                *labField('teg', 'type', 'lbsd', dropList=['input', 'textarea', 'a', 'span', 'form', 'ol', 'ul', 'b', 'i', 'p', 'label', 'div'], **style(padding=3)),
                *labField('text', 'text', **style(padding=3, height=140, overflow='auto'), br=1),
            ]
        )],
        [_div(className='cellbg-green', **style(height=185), children=[
                *labField('html attributes (separator: shift+Enter', 'htmlAttr', **style(padding=3, overflow='auto', height=80)),
                *labField('style', 'style', **style(padding=3, overflow='auto', height=80))
            ]
        )],
    ]
# *** *** ***

def btnProps():
    return [
        [_div(className='cellbg-green', **style(borderBottom='2px solid #fff'), children=[
            _div(children=[{'rowClassName': 'row'},
                _div(children=[*labField('label', 'text', **style(padding=3))]),
                _div(children=[*labField('name', 'name', **style(padding=3))]),
                ])
            ]
        )],
        [_div(className='cellbg-green', **style(borderBottom='2px solid #fff'), children=[
            _div(children=[{'rowClassName': 'row'},
                _div(children=[*labField('cmd', 'cmd', **style(padding=3))]),
                _div(children=[*labField('title', 'title', **style(padding=3))]),
                ]),
            _div(children=[*labField('param', 'param', **style(padding=3))])
            ]
        )],
        [_div(className='cellbg-green', **style(height=200), children=[
                _div(children=[*labField('className', 'className', **style(padding=3))]),
                *labField('style', 'style', **style(padding=3,  overflow='auto', height=120))
            ]
        )],
    ]

# *** *** ***

def divProps():
    return [
        [_div(className='cellbg-green', **style(borderBottom='2px solid #fff'), children=[
                _div(children=[{'rowClassName': 'row'},
                  _div(children=[*labField('name (if you want to hide this div)', 'name', **style(padding=3))]),
                  _div(children=[*labField('id', 'id', **style(padding=3))]),
                ])
            ]
        )],
        [_div(className='cellbg-green', **style(height=200), children=[
                *labField('text (new line: Shift+Enter)', 'text', **style(padding=3,  overflow='auto', height=180))
            ]
        )],
        [_div(className='cellbg-green', **style(height=200), children=[
                *labField('className', 'className', **style(padding=3)),
                *labField('style', 'style', **style(padding=3,  overflow='auto', height=120))
            ]
        )],
    ]

# *** *** ***

def svgProps():
    return  [
                label('SVG (new line: Shift+Enter)', **style(display='block', textAlign='left')),
                _field('text', **style(padding=3, overflow='auto', height=400, display='block'))
            ],

# *** *** ***

def imgProps():
    return [
        [_div(className='cellbg-green', **style(height=200), children=[
                _div(children=[*labField('src (URL)', 'src', **style(padding=3))]),
                *labField('className', 'className', **style(padding=3)),
                *labField('style', 'style', **style(padding=3, overflow='auto', maxHeight=90)),
                *labField('title', 'title', **style(padding=3, overflow='auto', maxHeight=50)),
            ]
        )],
        
        # <a>
        [_div(name='aImg', className='cellbg-green', **style(borderBottom='2px solid #fff'), children=[
                _div(children=[*labField('href (URL)', 'href', **style(padding=3))]),
                _div(children=[*labField('target', 'target', 'chb', '_blank', **style(width='99%', background='#eee', paddingBottom=3), title='default div+onClick')]),
                *labField('text on right', 'text', **style(padding=3,  overflow='auto', height=120)),
            ]
        )],
        
        # cmd
        [_div(name='cmdImg', className='cellbg-green', **style(borderBottom='2px solid #fff'), children=[
            _div(children=[{'rowClassName': 'row'},
                _div(children=[*labField('cmd', 'cmd', **style(padding=3))]),
                _div(children=[*labField('param', 'param', **style(padding=3))]),
                ]),
                _div(children=[*labField('text on right', 'label', **style(padding=3, overflow='auto', height=150))]),
            ]
        )],
    ]

# *** *** ***

def aTextProps():
    return [
        [_div(className='cellbg-green', **style(borderBottom='2px solid #fff'), children=[
                _div(children=[*labField('href (URL)', 'href', **style(padding=3))]),
            ]
        )],
        [_div(className='cellbg-green', **style(height=200), children=[
                *labField('text (new line: Shift+Enter)', 'text', **style(padding=3,  overflow='auto', height=180))
            ]
        )],
        [_div(className='cellbg-green', **style(height=200), children=[
                *labField('className', 'className', **style(padding=3)),
                *labField('style', 'style', **style(padding=3, overflow='auto', height=90)),
                _div(children=[*labField('title', 'title', **style(padding=3))]),
            ]
        )],
    ]

# *** *** ***

def svgMB():
    return [
        label('comment'),
        _field('notes')
    ]
# *** *** ***

def pageMB():
    return [
        # editMode устанавливает режим просмотра в режим edit (rsEdit = true) для разработки форм в режиме edit
        _div(children=[*labField('preview edit mode', 'editMode', 'chb', 'edit', **style(width='99%', background='#eee', paddingBottom=3), title='default div+onClick')]),
        _br(),
        _div(children=[*labField('comment', 'notes')])
    ]
# *** *** ***

def divMB():
    return [
        _div(children=[*labField('position, offset', 'position', 'chb3', dropList=['abs', 'rel'], **style(width='99%'), title='abs: absolute(left=x,top=y) rel: relative(margin(y,0,0,x)) null: ignore')]),
        _br(),
        _div(children=[*labField('a new line in the text', 'br', 'chb3', dropList=['br', 'p'], **style(width='99%'), title='replace "\\n" to <br> or <p>')]),
        _div(children=[*labField('comment', 'notes')])
    ]
# *** *** ***
def btnMB():
    return [
        _div(children=[*labField('button (or div)', 'btnType', 'chb', 'button', **style(width='99%', background='#eee', paddingBottom=3), title='default div+onClick')]),
        _br(),
        _div(name='subm', children=[*labField('submit', 'submit', 'chb', 'submit', **style(width='99%', background='#eee', paddingBottom=3), title='default div+onClick')]),
        _br(),
        _div(children=[*labField('comment', 'notes')])
    ]
# *** *** ***

def fieldMB():
    return [
        _div(children=[*labField('labeled field', 'labfield', 'chb3', dropList=['up', 'left'], **style(width=124), title='the label above or to the left')]),
        _br(),
        _div(children=[*labField('comment', 'notes')])
    ]
# *** *** ***
def aTextMB():
    return [
        _div(children=[*labField('target', 'target', 'chb', '_blank', **style(width='99%', background='#eee', paddingBottom=3), title='default div+onClick')]),
        _br(),
        _div(children=[*labField('comment', 'notes')])
    ]
# *** *** ***
def imgMB():
    return [
        _div(children=[*labField('onClick', 'aImg', 'chb3', dropList=['<a>', 'cmd'], **style(width='99%'), title='click action')]),
        _br(),
        _div(children=[*labField('comment', 'notes')])
    ]
# *** *** ***

def tegMB():
    return [
        _div(children=[*labField('a new line in the text', 'br', 'chb3', dropList=['br', 'p'], **style(width='99%'), title='replace "\\n" to <br> or <p>')]),
        _div(children=[*labField('comment', 'notes')])
    ]
# *** *** ***