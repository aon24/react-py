# -*- coding: utf-8 -*- 
'''
AON 18 oct 2017

'''
from .. toolbars import toolbar
from .. cf import cf, docTitle, sent, sw
from .. formTools import style, label, label_, _table

from tools import *
from toolsLC import config
import docTools

import re
# *******************

title = 'Исх. письмо'
forPrint = '¤'.join([
    'РКФ исходящего документа|rkcki.print',
    'Информация об отправке на E-mail|rkcki.email.print&Информация об отправке на E-mail',
    'Ответ заявителю на бланке|rkcki.blank&Исходящее письмо',
    'Ответ заявителю на бланке 2|rkcki.blank2&Исходящее письмо',
    'Евроконверт (DL/E65 110 x 220 мм)|envelope.eu.print',
    'Евроконверт без полей(DL/E65 110 x 220 мм)|envelope.eu2.print',
    'Евроконверт с окошком (лист А4)|envelope.euw.print',
    'Конверт для А4 (C4 229 x 324 мм)|envelope.a4.print',
    'Конверт для А4 на листе А4 (наклеить на конверт)|envelope.a44.print',
    'Конверт для А5 (С5 162 x 229 мм)|envelope.a5.print',
    'Конверт для А6 (С6 114 x 162 мм)|envelope.a6.print',
    ])
javaScriptUrl = 'jsv?api/forms/rkcki/rkcki.js'
cssInline = '#root{min-height: 100vh}'

# *******************

def page(dbAlias, mode, userName, multiPage):
    
    st =  {'width': '253mm'}
    if multiPage:
        st['height'] = 440
    elif mode == 'preview':
        st['overflowY'] = 'hidden'
        st['height'] = 'auto'
        
    rk = dict(

    style = st,
    className = 'page',
    
    div = [

        docTitle('Ответ заявителю', left=['finish', 'Закрыть основания'], right=['SMTPSENTOK', 'отправлено'], width='60%', classic=1),        

        dict ( wl='40mm', className='cellbg-green', div=_table(
            [
               label('Исх. №'),
               {'field': ('PREF', 'tx'),  **sw(26), 'readOnly': 1} if mode not in ['read', 'preview'] else {'field': ('FULLNO', 'tx'), **sw(79)},
               {'field': ('DOCNO', 'tx'), **sw(27), 'readOnly': 1} if mode not in ['read', 'preview'] else {'skip':1},
               {'field': ('SUFF', 'tx'),  **sw(26), 'readOnly': 1} if mode not in ['read', 'preview'] else {'skip':1},
             
              label('от', '7mm'), {'field': ('DOCDA', 'dt'), **sw(33)},
              label('осн.', '14.5mm'), {'field': ('grounds', 'gr'), 'btn':(1, '55mm')},
            ],
        )),
                         
        dict ( wl='40mm', style={'background': '#d2dacb'}, className='cellbg-green', div=_table(
            [ {'rowStyle': {'overflow': 'hidden', 'width': '99.5%' } },  
             label_('Заявитель'), {'field': ('ToCorr', 'tx'), **sw(117) },
             label('доп.№', '14mm'), {'field': ('ADDNO', 'tx'), **sw(40)}, label('от', '5mm'), {'field': ('ADDDA', 'dt'), **sw(33)}
            ],
            [ label_('Адрес заявителя'), {'field': ('toAddress', 'tx')}],
            [ label('E-mail'), cf.email]
        )),
  
        dict ( wl='40mm', className='cellbg-green',  div=_table(
            [ label_('Отметки об исполнении'), {'field': cf.hist}],
            [ label_('СОДЕРЖАНИЕ'), {'field': ('subj', 'tx')}],
            [ label_('Приложение на'), {'field': ('att', 'lbse', ['нет', 'л. + пакет документов', 'л. + (составлен акт о недовложении)'])}],
            [ label('Примечание'), {'field': ('notes', 'tx')}],
        )),
  
        dict ( wl='40mm', style={'background': '#d2dacb'}, className='cellbg-green', div=_table(
            [ label_('Подписал'), {'field': cf.fromWho, 'saveAlias': 1}],
            [ label_('Визы'), {'field': cf.visa}],
            [ label_('Подразделение'), {'field': cf.depName, 'saveAlias': 1}],
            [ label('Подготовил'), {'field': cf.whoRkcki, 'saveAlias': 1}], #whoRkcki
        )),
              
        dict ( fileShow='FILES1_', wl='40mm', className='cellbg-green', label='скан ответа заявителю' ),

        dict ( wl='40mm',className='cellbg-green', div=_table(
            [ label('', '40mm'),
             {'field': ('sstu', 'chb', 'Выгрузить информацию на портал ССТУ.РФ'), 'classic': 1, 'className': 'ttar',
              'style':{'padding': 3,'textAlign':'left', 'font':'bold 10pt Arial'}},
            ]
        )),
        
        
        docTitle('Сопроводительное письмо (ответ в другой орган)', left=['hideCover.FD', 'скрыть'], width='80%', classic=1),        
        
        dict ( fileShow='FILES2_', name='cover', wl='40mm', className='cellbg-green', label='скан письма' ),

        dict ( name='cover', wl='40mm', className='cellbg-green', div=_table(
            [
                { 'rowStyle': {'width': 'auto'}},
                label_('Шаблон'),
                { 'field': ('TEMPLATE', 'lbsd', 'ОГ_уведомления-список'), **sw(120), 'saveAlias': 1 },
            ],
            [
                { 'rowStyle': {'width': 'auto'}},
                label('Размер шрифта'),
                { 'field': ('FONTSIZE', 'lbsd', ['нормальный|10.5pt/1.0', 'мелкий|8.5pt/1.0', 'крупный|12.5pt/1.0']), **sw(120), 'saveAlias': 1 },
            ],
        )),

        dict ( name='cover', className='cellbg-green', div=[{ 'field': ('BODYPRN', 'tx') }] ),
        
        sent(),
    ]
)

    return dict(
        style(backgroundImage='url(/image?24x24LB.png)', overflow='hidden'),
        focus = 'hist',
        div = [toolbar.rkck(mode), rk]
    )
    
# *** *** ***

def queryOpen(d, mode, ground):
    d._SENT = d._SENT.replace('<br>', '¤')
    d.grounds = re.sub(r'<[\s\S]*?>', '', d.grounds)
    d.links   = re.sub(r'<[\s\S]*?>', '', d.links)

    if mode in ['read', 'preview']:
        d.fullNo = d.pref + d.docNo + d.suff
        
    dbProfile = profile(d.db.alias)
    if mode == 'new':
        d.MAIN = '1'
        d.DIR = '1'
        d.LINKRULE = dbProfile.LINKRULE or 'Исх'
        d.DOCDA = today()
        d.pages = '1'
        d.dup = '1'
        d.att = 'нет'
        d.CORRTYPE = dbProfile.CORRTYPE
        d.title = dbProfile.DOCTITLE or 'Исходящее письмо'
        d.DEPNAME = well('ouByDName', dbProfile.dname).DNTITLE
        d.DEPNAME_ALIAS = dbProfile.dname
        if config.SvojaNemeraciaDliaIshodjashih:
            d.docNo = ''
    docTools.makePrefSuff(d, dbProfile)

# *** *** ***

def querySave(d, dic):
    fw = well('who', d.fromWho + '|' + d.fromWho_alias)
    if fw:
        d.post = fw.post
    docTools.rkckgQSave(d)
        
# *** *** ***

