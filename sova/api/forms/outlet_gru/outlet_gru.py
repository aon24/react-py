# -*- coding: utf-8 -*- 
'''
AON 18 apr 2017

'''
try:
    from .... util.common import *
except:
    from tools import *
    from common import *
    import docTools
    
from .. toolbars import toolbar
from .. formTools import style, label, label_, _table, labField, labField_
from .. cf import sw, cf, dl, docTitle, sent, makeDL


# *******************

title = 'Уведомление'
forPrint = 'Распечатать уведомление|outlet.gru.print&Уведомление'
javaScriptUrl = 'jsv?api/forms/outlet_gru/outlet_gru.js'
cssInline = '#root{background-image:url(/image?24x24LB.png);min-height:calc(100vh - 30px)}'

# *******************

"""
    Выпадающий список - это массив(или tuple) строк типа:
    'метка в выпадающем списке | значение, которое переносится в поле ¤ алиас'
    , где "¤ алиас" - неотображаемая часть спискового поля 
    
    ['Простое',
     'Заказное',
    'Зак. с ув.|Заказное с уведомлением¤RF.AKK',
    ]
"""
# *** *** ***

def queryOpen(d, mode, ground):
    main = d.db.getDocumentByUNID(d.ref)
    makeDL(d, main)
    orgName = well('MAIN', 'ORGNAME')
    d.orgNameVP = orgName.partition('образование ')[2] or orgName.partition('МО ')[2] or orgName

# *** *** ***

def querySave(d, dic):
    if not profile(d.db.alias).notNotSend:
        d.notSend = '1'
    
    fw = well('who', d.fromWho + '|' + d.fromWho_alias)
    if fw:
        d.post = fw.post
        
# *** *** ***    

def page(dbAlias, mode, userName, multiPage):
    wl = '40mm'
    
    outlet = dict(
    
    style = {'height': 490, 'width': 785} if multiPage else {'width': 785},
    className = 'page',
    
    div = [

        docTitle('Уведомление', left=['FINISH', 'закрытие'], right=['SMTPSENTOK', 'отправлено'], width='68%', classic=1),
        dl(wl),

        dict (wl=wl, className='cellbg-green', div=_table(
            labField_('Обращ. заявителя', 'TOCORR'),
            labField_('Регион', 'REGION'),
            labField_('Адрес заявителя', 'TOADDRESS'),
            [ label_('e-mail заявителя'), cf.email],
            [ label_('Поступил'), {'field':cf.thru}],
            [ label('через'), {'field':cf.thru2}],
        )),
  
        dict ( wl=wl, className='cellbg-green', div=_table(
            [ label_('По поручению'), {'field': ('ONASS', 'lbse', 'ОГ_по поручению2', 'dbProfile.dName' ), 'sep': '=>', 'alias': 1}],
            [ label_('Направлено в'), {'field': ('WHO', 'lbme', 'orgList'), 'sep': '|'}],
            [ label_('Совместно с'), {'field': ('WHO_SOISP', 'lbme', 'orgList'), 'sep': '|'}],
            [ label_('Подписал'), {'field': cf.fromWho, 'saveAlias': 1}],
            [ label_('Отправка по почте'), {'field': ('ENVTYPE', 'lbsd', ['Простое', 'Заказное', 'Заказное с уведомлением'])}],
            labField('Комментарий', 'NOTES'),
        )),
   
        dict ( wl=wl, className='cellbg-green', div=_table(
            [
                { 'rowStyle': {'width': 'auto'}},
                 label_('Шаблон'),
                { 'field': ('TEMPLATE', 'lbsd', 'ОГ_уведомления-список'), **sw(120), 'saveAlias': 1 },
                 label('Дата отправки', style={'width': '30mm', 'verticalAlign': 'bottom'} )
            ],
            [
                { 'rowStyle': {'width': 'auto'}},
                 label_('Обращение'),
                { 'field': ('APPEAL', 'tx'), **sw(120) },
                 label('', '5mm'),
                { 'field':('SENDDA', 'dt'), **sw(35) },
            ],
            [
                { 'rowStyle': {'width': 'auto'}},
                label('Размер шрифта'),
                { 'field': ('FONTSIZE', 'lbsd', ['нормальный|10.5pt/1.0', 'мелкий|8.5pt/1.0', 'крупный|12.5pt/1.0']), **sw(120), 'saveAlias': 1 },
            ],
        )),
     
        dict ( fileShow='FILES1_', wl=wl, className='cellbg-green', label='вложения '),
        dict( className='cellbg-green', div=[ {'field': ('BODYPRN', 'tx')} ] ),
        sent(),
    ]
)

    return dict(
        style(backgroundImage='url(/image?24x24LB.png)', overflow='hidden'),
        focus = 'ONASS',
        div = [toolbar.o(mode), outlet]
    )
# *******************
