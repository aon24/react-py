# -*- coding: utf-8 -*- 
'''
AON 18 sep 2019

'''

from .. formTools import style, label, _div, _btnD, _field
from ...views.viewTools import viewDiv

try:
    from tools import well
except:
    from .... util.common import well

# *** *** ***

title = 'Тематический классификатор Управления Президента РФ по работе с обращениями граждан и организаций'
jsUrl = 'jsv?api/forms/themes/themes.js'
cssUrl = ['jsv?api/forms/themes/themes.css', 'jsv?api/views/view.css']

# *** *** ***
partList = [
    '1. Государство, общество, политика|+0001',
    '2. Социальная сфера|+0002',
    '3. Экономика|+0003',
    '4. Оборона, безопасность, законность|+0004',
    '5. Жилищно-коммунальная сфера|+0005']

def page(dbAlias, mode, userName, multiPage):
    dlg = \
        _div(className='dlgDiv', **style(margin='10px auto', width='25cm', height='calc(100vh - 50px)', backgroundImage='url("/image?bg51.jpg")'), children=
            [
            _div(title, className='dlgTitleBar', children=
                    [ _btnD('\u00d7', 'clsDlg', className='dlgCloseButton', title='Закрыть') ]
                ),
            _div(**style(display='table', width='100%', padding=3),
                children=
                    [
                        _field('find', 'tx', keyCode_13='setFilter',
                            **style(display='table-cell', width='8.5cm'),
                            placeholder='Введите номер или слово, или 2 слова. Пробел между словами - искать по "И", звездочка между словами - искать по "ИЛИ". Enter ',
                        ),
                    ],
            ),
            
            #  ***
            _div( className='rubOG', children=[_field('rog', 'readyList')] ),
            #  ***
            
            _div(**style(display='table', width='100%', padding=3),
                children=
                    [
                        _field('dlgPart', 'lbsd', partList,
                            saveAlias=1,
                            **style(display='table-cell', width='8.5cm'),
                            placeholder='Выберите раздел из списка',
                        ),
                        label(),
                        _field('dlgTheme', 'lbsd', [''],
                            saveAlias=1,
                            **style(display='table-cell', ),
                            placeholder='Выберите тематику из списка',
                        ),
                        label(),
                        _btnD('закрыть', 'clsDlg', className='svTop', **style(display='table-cell', width='24mm')),
                ]),
            ]
        )
    
    return _div(
        **style(backgroundImage='url(/image?24x24LB.png)', overflow='hidden'),
        children = [dlg]
    )
# *** *** ***

def queryOpen(d, mode, ground):
    d.readyListUrl = 'readyList?rogView::' + well('verRubrOG')
    d.readyDCUrl   = 'readyList?rogDC::' + well('verRubrOG')
    d.noSave = '1'
    
# *** *** ***

