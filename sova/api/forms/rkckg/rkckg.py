# -*- coding: utf-8 -*- 
'''
AON 18 apr 2017

'''
from .. toolbars import toolbar
from .. cf import cf, docTitle, sent, sw
from .. formTools import style, label, label_, _table, _btnD, _div

try:
    from tools import profile
except:
    from .... util.common import profile 

import re
# *** *** ***

title = 'Обращение'
forPrint = '¤'.join([
    'Распечатать обращение|rkckg.tx.print',
    'Распечатать РКФ с резолюциями|rkckg.print',
    'Распечатать карточку личного приема|rkckg.lp.print',
    ])
javaScriptUrl = 'jsv?api/forms/rkckg/rkckg.js'

# *** *** ***

cssInline = '#root{background-image:url(/image?24x24LB.png);min-height:calc(100vh - 30px)}'

# *** *** ***
"""
    Выпадающий список - это массив(или tuple) строк типа:
    'метка в выпадающем списке | значение, которое переносится в поле ¤ алиас'
    , где "¤ алиас" - неотображаемая часть спискового поля 
    
    ['Простое',
     'Заказное',
    'Зак. с ув.|Заказное с уведомлением¤RF.AKK',
    ]
"""

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
        
        docTitle('', field='LOGTITLE', left=['printed', 'Распечатано'], right=['urgent', 'Срочно'], width='68%', classic=1),

        dict (
                wl = '19mm',
                className = 'cellbg-gray',
                div = _table(
            [
              label_('Вх. №'),
             
               {'field': ('PREF', 'tx'),  **sw(17), 'readOnly': 1} if mode == 'edit' else {'field': ('FULLNO', 'tx'), **sw(70)},
               {'field': ('DOCNO', 'tx'), **sw(26), 'readOnly': 1} if mode == 'edit' else {'skip':1},
               {'field': ('SUFF', 'tx'),  **sw(20), 'readOnly': 1} if mode == 'edit' else {'skip':1},
             
             label_('от', '7mm'),
             {'field': ('DOCDA', 'dt'), **sw(35)} if mode == 'edit' else {'field': ('dateTime', 'tx'), **sw(46)},
             {'field': ('DOCTM', 'tx'), **sw(18), 'readOnly': 1} if mode == 'edit' else {'skip':1},
             _btnD('Доп. №', 'addNo', className='label_ abutton', **sw(17)) if mode == 'edit' else label_('Доп. №', '17mm'),
                    {'field': ('AddNo', 'tx'), **sw(54), 'readOnly': 1},
                    label_('от', '5mm'),
                    {'field': ('AddDa', 'dt'), 'readOnly': 1},
            ],
            
            [label_('Заявитель'), {'field': ('FROMCORR', 'tx'), **sw(70)},
             {'field': ('activeAuthor', 'chb', 'много пишущий автор'), 'classic': 1, **style(width='53mm', textAlign='center', color='#004080', font='bold 9pt Arial')},
               label_('Исх. №', '17mm'), {'field': ('FROMNO', 'tx'), **sw(54)}, label('от', '5mm'), {'field': ('FROMDA', 'dt')},
             
             ],
            [ label_('Район'), {'field': ('RNN', 'lbsd', 'ОГ_район'), **sw(123), 'saveAlias': 1},
             {'field': ('townLabFD', 'fd'), **sw(17), 'className':'label_'}, {'field': ('TOWN', 'lbsd', 'ОГ_поселение',
                    "'RF.AKK.MOKRASG' if dbProfile.dName.startswith('RF.AKK.MOKRASG') else dbProfile.dName" )},
             ],

            [ label('Поступил'), {'field': cf.thru, **sw(123)},
              label('через', '17mm'), {'field': cf.thru2},
             ],
                    )
        ),
 
        dict (
                className = 'cellbg-gray',
                wl = '40mm',
                div = _table(
            [ label_('Адрес заявителя'), {'field': ('fromAddress', 'tx')},
             ],
                         
            [ label_('Тип автора'), {'field': ('authorType', 'lbmd', 'ОГ_тип автора'), **sw(102)},
              label_('Телеф.', '17mm'), {'field': ('phone', 'tx')}
             ],
            [
              label_('Вид обращения'), {'field': cf.titleRKCKG, **sw(102) },
              label_('e-mail', '17mm'), cf.email,
             ],
            [
              {'field': ('TONAMELABFD', 'fd'), **sw(40), 'className':'label'}, {'field': cf.toName, **sw(102), 'saveAlias': 1},
              label('повтор', '17mm'), {'field': ('RETRY', 'tx'), **sw(54)},
              label('кол. чел.', '17mm'), {'field': ('howMany', 'tx')},
             ],
                    )
        ),
  
        dict (
                className = 'cellbg-gray',
                wl = '40mm',
                div = _table(
            [ label_('СОДЕРЖАНИЕ'), {'field': ('subj', 'tx')},
            ],

            [ label('Приложение на'), {'field': ('pages', 'lbse', ['л. + пакет документов', 'л. + (составлен акт о недовложении)']), **sw(102)},
              label('Тема', '17mm'), {'field': ('theme', 'tx')}
            ],
                    )
        ),
  
        dict (
                wl = '1mm',
                className = 'cellbg-gray',
                div = _table(
            [ { 'rowStyle': {'width': 'auto'}},
              label_('Контроль', '40mm'), {'field': cf.ccType, **sw(102)},
              label('Срок', '17mm'), {'field': ('CCDA', 'dt'), **sw(35)},
            ],
            [ label('Предыд. обращения', '40mm'), {'field': ('grounds', 'gr'), 'btn':(3, '65mm')}],
                    )
        ),
                
        dict ( fileShow='FILES1_', wl='40mm', className='cellbg-gray', label='вложения ' ),
        
        dict (
                wl = '19mm',
                className = 'cellbg-green',
                **style(backgroundColor='#eee'),
                div = _table(
                    [ label('Тематический классификатор Управления Президента РФ по работе с обращениями граждан', style={'border': '0', 'textAlign':'center', 'color':'#4080C0'})],
            [
                label_('Раздел', style={'color':'#4080C0', 'textAlign': 'left'}),
                { 'field': ('RGPART', 'fd'), 'className':'tta' },
            ],
            [
                label_('Тематика', style={'color':'#4080C0', 'textAlign': 'left'}),
                { 'field': ('rgTheme', 'fd'), 'className':'tta' },
            ],
            [
                label_('Тема', style={'color':'#4080C0', 'textAlign': 'left'}),
                { 'field': ('rgSubj', 'fd'), 'className':'tta' },
            ],
            [
                label_('Вопрос', style={'color':'#4080C0', 'textAlign': 'left'}),
                { 'field': ('rgAsk', 'fd'), 'className':'tta' },
            ],
            [
                label('Код', style={'color':'#4080C0', 'border': '0', 'textAlign': 'left'}),
                { 'field': ('rgCode', 'table'), 'btn':(4, '55mm'), 'ttaStyle': {'padding': 0, 'background': '#fff'} },
            ],
                    )
        ),
    
         dict (
                className = 'cellbg-gray',
                div = _table(
            [label('Отметки об исполнении', style={'width':'124mm', 'textAlign': 'left'}),
             label(''),
             label('Более поздние обращения, ответы на обращения', style={'width':'118mm', 'textAlign': 'left'}),
             ],
                         
            [{'field': ('hist', 'tx'), **sw(124)},
             label(''),
             {'field': ('links', 'gr'), **sw(120), 'btn':(2, '58mm')}
             ],
            [label('Номера и даты ответов', style={'width':'124mm', 'textAlign': 'left'}),
             label(''),
             label('Доп. информация для заметок (не распечатывается, не отправляется)', style={'width':'118mm', 'textAlign': 'left'}),
             ],
                         
            [{'field': ('RENUM', 'tx'), **sw(124)},
             label(''),
             {'field': ('addNotes', 'tx'), **sw(120)}
             ],

            [label('Дата закрытия', style={'width':'36mm', 'textAlign': 'left'}),
             label('\u00a0', '4mm'),
             label('Дело № (том №, листы, примечания)', style={'width':'84mm', 'textAlign': 'left'}),
             label(''),
             label('Подписал', style={'width':'118mm', 'textAlign': 'left'}),
             ],

            [{'field': ('clsDa', 'dt'), **sw(36)},
             label('', '4mm'),
             {'field': ('fileNo', 'tx'), **sw(84)},
             label(''),
             {'field': ('clsName', 'tx'), **sw(120)}
             ],

                )
        ),
              
        dict (
                className = 'cellbg-gray',
                div = _table(
            [label_('Причина жалобы', '40mm'), {'field': ('cause', 'tx')},],
            [label('Примечание', '40mm'), {'field': ('notes', 'tx')},],
                )
        ),
        
        sent(),
    ]
)
    
    return _div(
        **style(backgroundImage='url(/image?24x24LB.png)', overflow='hidden'),
        focus = 'fromCorr',
        children=[toolbar.rkck(mode), rk]
    )


# *** *** ***

def queryOpen(d, mode, ground):
    dbProfile = profile(d.db.alias)
    
    d._SENT = d._SENT.replace('<br>', '¤')
    d.grounds = re.sub(r'<[\s\S]*?>', '', d.grounds)
    d.links   = re.sub(r'<[\s\S]*?>', '', d.links)
    d.toNameLabFD = dbProfile.toNameLab or 'Адресат'
    d.townLabFD = dbProfile.townLab or 'Поселен.'

    if mode in ['read', 'preview']:
        d.fullNo = d.pref + d.docNo + d.suff
        d.dateTime = d.D('docDa') + ' ' + d.docTm
    
    