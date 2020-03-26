# -*- coding: utf-8 -*- 
'''
AON 18 apr 2017

'''
try:
    from .. .. util.common import *
except:
    from tools import *
    from common import *
    import docTools
    
from .. toolbars import toolbar
from .. formTools import style, label, label_, _table, _div, _field, _field4, _btnD
from .. cf import sw, dl, docTitle, sent, makeDL

# *** *** ***

title = 'Отметка о передаче'
forPrint = 'Резолюция|o.project&Резолюция'
javaScriptUrl = 'jsv?api/forms/o/o.js'
cssInline = '#root{min-height:100vh}'

# *** *** ***

def prjO(i):
    
    return _div(
            name = 'prj%d' % i,
            wl = '33mm',
            className = 'cellbg-green',
            **style(borderColor='#889fb7', borderWidth='0 1px 2px'),
            children = _table(
                        [{'rowStyle': {'width': 'auto', 'position': 'relative'}},
                          label(str(i), className='prj', style={'width': '5mm', 'margin':0}),
                          label_('Исполнители', style={'width': '33mm', 'margin':0}),
                         _field4('whoPrj%d' % i, 'lbmd', 'whoForDN', 'dbProfile.whoGroup or dbProfile.dName', **sw(134), saveAlias=1),
                         label('', style={'width': 2, 'fontSize': 1, 'padding': 0, 'border': 0} ),
                         _field('prjDa%d' % i, 'dt', **sw(33))
                        ],
                        [{'rowStyle': {'width': 'auto'}},
                          label_('Резолюция'),
                         _field4('resPrj%d' % i, 'lbse', 'Резолюции', "(dbProfile.prjRes or 'ОГ') + (':%s' % dbProfile.dName if well('Резолюции', '%s:%s' % (dbProfile.prjRes or 'ОГ', dbProfile.dName) ) else '')", **sw(134), alias=1),
                         label('', style={'width': 2, 'fontSize': 1, 'padding': 0, 'border': 0} ),
                         _field('prjDa%d2' % i, 'dt', **sw(33))
                        ],
                        [{'rowStyle': {'width': 'auto'}},
                          label('Направлено'),
                         _field('prjWhoType%d' % i, 'lbsd', 'Направлено (проект)', **sw(134), saveAlias=1),
                          label('', '34mm')
                        ],
                    )
        )
    
#*** *** ***
    
def page(dbAlias, mode, userName, multiPage):
    wl = '33mm'

    o = dict(
        style = {'height': 490, 'width': 785} if multiPage else {'width': 785},
        className = 'page',
        
        div = [
        docTitle('Отметка о передаче', left=['urgent', 'срочно'], right=['sentOk', 'отправлено'], width='68%', classic=1),
        dl(wl),
 
        dict ( wl=wl, name='who', className='cellbg-lite', div=_table(
            [ label('Кому направлено'), {'rowStyle': {'width': 'auto'}},
             _field4('who', 'lbmd', 'whoForDN', 'dbProfile.whoGroup or dbProfile.dName', **sw(134), saveAlias=1),
             _field('projectO', 'chb', 'проект', **style(width='33mm', paddingLeft=10, font='bold 9pt Arial', color='#048'))
            ],
        )),


        docTitle('Проект поручения', name='project'),

        *[prjO(i) for i in range(1, 6)],

        dict ( wl=wl, name='fromWho', className='cellbg-lite', div=_table(
            [ label_('Резолюция'), {'rowStyle': {'width': 'auto'}},
             _field4('res', 'lbse', 'Резолюции', "(dbProfile.prjRes or 'ОГ') + (':%s' % dbProfile.dName if well('Резолюции', '%s:%s' % (dbProfile.prjRes or 'ОГ', dbProfile.dName) ) else '')", **sw(134), alias=1),
             _field('notSend', 'chb', 'не отпр.', **style(width='33mm', paddingLeft=10, font='bold 9pt Arial', color='#048')),
            ],
            [ label_('Кто направил'), {'rowStyle': {'width': 'auto'}},
             _field4('fromWho', 'lbsd', 'whoSign', 'dbProfile.o_fromWho or dbProfile.dName', **sw(134), saveAlias=1),
              label('', '33mm'),
            ],
            [ label('Направлено'), {'rowStyle': {'width': 'auto'}},
             _field('whoType', 'lbsd', 'Направлено', **sw(134)),
              label('', '33mm'),
            ],
        )),

        dict ( fileShow='FILES1_', name='files1', wl='34mm', className='cellbg-lite', label='файлы ' ),
           
        dict ( wl=wl, name='sendDa', className='cellbg-lite', div=_table(
            [
             {'rowStyle': {'width': 'auto'}},
              label(''),
              label('Дата передачи', '33mm', className='labell'),
              label('', '10mm'),
              label('Исполнить до', '33mm', className='labell'),
              label('', '10mm'),
              label('Дата возврата (факт)', '40mm', className='labell'),
              label(''),
            ],                            
            [
             {'rowStyle': {'width': 'auto'}},
              label(''),
             _field('sendDa', 'dt', **sw(33)),
              label('', '10mm'),
             _field('ccDa', 'dt', **sw(33)),
              label('','10mm'),
             _field('clsDa', 'dt', **sw(33)),
              label(''),
            ],
        )),
        
        docTitle('Отметка об исполнении', right=['op', 'получено'], width='68%', classic=1, name='op'),

        
        dict ( name='op', wl=wl, className='cellbg-lite', div=_table(
            [ {'rowStyle': {'width': '99.3%'}},
              label_('Дата возврата'),
              _field('cls2Da', 'dt', **sw(33)),
              label('', 'auto'),
              _btnD('отправить', 'returnO', className='svTop', **sw(32)) if mode == 'edit' else None,
            ],
            
            [ label_('Результат'),
              _field4('result', 'lbme', 'Результат обращения', "(dbProfile.prjRes or 'ОГ') + \
                    (':%s' % dName if well('Результат обращения', '%s:%s' % (dbProfile.prjRes or 'ОГ', dName) ) else '')"
            )],
            
            [ label_('Номера и даты исх'), _field('renum', 'tx')],
            [ label_('Кто подписал'), _field4('rtfWho', 'lbsd', 'whoSign', 'dbProfile.dName', saveAlias=1)],
            [ label('Комментарий'), {'field':('notes', 'tx')}],
                    )
            ),
   
        dict ( fileShow='FILES2_', name='op', wl='34mm', className='cellbg-lite', label='файлы ' ),

        sent(),
        
        _div ( wl=wl, children=[
            _field('readOnly', 'chb', 'запрет редактирования', classic=1, **style(color='#048', font='normal 9pt Verdana')),
        ]),
    ] )

    return _div(
        **style(backgroundImage='url(/image?24x24LB.png)', overflow='hidden'),
        focus='who',
        children=[toolbar.o(mode), o]
    )


# *** *** ***

def queryOpen(d, mode, ground):
    if not d.ref:
        return
    
    main = d.db.getDocumentByUNID(d.ref)
    if not main:
        return
    
    makeDL(d, main)

    d.docda = main.docda
    d.docno = main.pref + main.docno + main.suff
    d.ccType = main.ccType
    if "Личный прием высшими должностными лицами субъекта Российской Федерации" in main.rgAsk or "Личный приём высшими должностными лицами субъекта Российской Федерации" in main.rgAsk:
        d.lpinfo = "Заявитель проинформирован о порядке приема граждан в администрации Краснодарского края."
    else:
        d.lpinfo = " "

    if d.db.alias.startswith('RF.AKK.IOGZHI/'):
        d.PROJECTO = '1'
    
# *** *** ***

def querySave(d, dic):
    try:
        import forms
        forms.testWho(d)
        forms.testPrjDa(d)
    except:
        pass
    
    if '¤' not in d.who and d.whoType == 'Ответственный исполнитель + соисполнители':
        d.whoType = 'Ответственный исполнитель'
    
    if '¤' in d.who and not d.notSend:
        d.createPacket = d.who
        if 'соисп' in d.whoType.lower() or 'свод' in d.whoType.lower() or not d.db.alias.startswith('RF.AKK/OG'):
            d.whoTypeNext = 'Соисполнитель'
        else:
            d.whoTypeNext = 'Ответственный исполнитель'
    
    if d.projectO and d.whoPrj1 and (d.whoPrj2 or d.whoPrj3):
        if not d.linkRule.endswith('. Проект'):
            d.linkRule += '. Проект'
    else:
        d.linkRule = d.linkRule.split('. Проект')[0]
    
    medoProf = well('classifier', 'MEDO-config')
    main = dic.get(d.REF)
    ou = well('ouByDName', d.who_alias)
    
    if (d.who_alias != well('MAIN', 'DNAME')) and ou and main and medoProf and ou.MEDOADDRESS and not d.medoResponseDone:
        if main.MEDOREPLAYTO and main.dir == '0':
            if main.MEDOREPLAYTO in ou.A('MEDOADDRESS'):
                if d.attFields(): # без вложения не отправлять!
                    d.medoresponse = 'R23' # ответ
            else:
                d.medoresponse = 'R24' # пересылка по принадлежности
        elif ou.MEDOADDRESS:
            d.medoresponse = 'R25' # инициативная отправка
    
    if d.ccType == 'запрос':
        d.AUTOORDER = ''

# *** *** ***
