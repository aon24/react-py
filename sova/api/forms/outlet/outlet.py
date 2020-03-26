# -*- coding: utf-8 -*- 
'''
AON 18 apr 2017

'''
from .. toolbars import toolbar
from .. formTools import style, label, label_, _table
from .. cf import sw, cf, dl, docTitle, sent, makeDL
try:
    from MrDB import getDocByUnid
    from tools import profile
except:
    from .... dbToolkit.Book import getDocByUnid
    from .... util.common import profile

# *******************

title = 'Результаты рассмотрения|outlet.print&Результаты рассмотрения'
forPrint = 'Результаты рассмотрения|outlet.print&Результаты рассмотрения'
javaScriptUrl = 'jsv?api/forms/outlet/outlet.js'
cssInline = '#root{background-image:url(/image?24x24LB.png);min-height:calc(100vh - 30px)}'

# *******************

def queryOpen(d, mode, ground):
    main = d.db.getDocumentByUNID(d.ref)
    makeDL(d, main)
    if mode == 'read' and d.SDLINK:    # d.SDLINK: OП-2042.1-17-39 17.10.2017|RF.AKK/OGI_2017&7CE8B2B9370F5D24232A640A7F5DC387
        dba, _, unid = d.SDLINK.partition('|')[2].partition('&')
        
        if profile(dba):
            dl = getDocByUnid(unid, dba, d.db.userName)
            if dl:
                return dl

        d.title += '. РКФ документа недоступна, т.к. находится в журнале другого подразделения'

# *** *** ***

def querySave(d, dic):
    if not d.sdLink:
        d.title = 'Закрытие документа' if d.finish else 'Отметка об исполнении'
    d.linkFD = ''
        
# *** *** ***

def page(dbAlias, mode, userName, multiPage):
    wl = '40mm'
    
    outlet = dict(
    
    style = {'height': 490, 'width': 785} if multiPage else {'width': 785},
    className = 'page',
    
    div = [

        docTitle('Ссылка на связанный документ', left=['FINISH', 'закрытие'], width='68%', classic=1, field='Title'),
        dl(wl),
 
        dict ( wl=wl, className='cellbg-green', div=_table(
            [{'rowStyle': {'width': 'auto'}}, label('Дата исполнения'), {'field': ('clsDa', 'dt'), **sw(33)}],
             [ label_('Отметки об исполнении'), {'field': cf.hist}],
             [ label_('Номера и даты ответов'), {'field': ('RENUM', 'tx')},],
             [ label('Дело № (том №, листы)'), {'field': ('fileNo', 'tx')},],
        )),
  
        dict ( wl=wl, className='cellbg-lite', div=_table(
            [ label_('Подписал'), {'field': cf.fromWho, 'saveAlias': 1}],
            [ label_('Подразделение'), {'field': cf.depName, 'saveAlias': 1}],
            [ label('Подготовил'), {'field': cf.whoRkcki, 'saveAlias': 1}], #whoRkcki
        )),
   
        dict ( wl=wl, className='cellbg-green', div=_table(
            [ label_('Корреспондент'), {'field': ('toCorr',  'tx')}],
            [ label_('Кому'), {'field': ('toName', 'lbsd', 'whoForDN', 'dName'), 'saveAlias': 1}],
            [ label_('Содержание'), {'field': ('subj',  'tx')}],
            [ label('Комментарий'), {'field': ('notes',  'tx')}],
        )),

        dict ( fileShow='FILES1_', wl='41mm', className='cellbg-green', label='вложения '),

        dict ( wl=wl, className='cellbg-green', div=_table([
             label(''),
             {'field': ('sstu', 'chb', 'Выгрузить информацию на портал ССТУ.РФ'), 'classic': 1, 'className': 'ttar',
              **style(padding=3, textAlign='left', font='bold 10pt Arial')}]
            )
        ),

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

        dict( name='cover', className='cellbg-green', div=[ {'field': ('BODYPRN', 'tx')} ] ),
        
        sent(),
    ]
)

    return dict(
        style(backgroundImage='url(/image?24x24LB.png)', overflow='hidden'),
        focus = 'ONASS',
        div = [toolbar.o(mode), outlet]
    )
# *******************
