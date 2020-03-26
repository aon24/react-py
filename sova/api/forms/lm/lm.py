# -*- coding: utf-8 -*- 
'''
logManager

AON 9 mar 2018

'''
try:
    from .... util.first import sovaLogger
    from .... util.common import well, toWell
except:
    from tools import well
    from common import toWell
    from first import sovaLogger

from .. formTools import style, _field, _div

import re
# *** *** ***

title = 'log'
javaScriptUrl = 'jsv?api/forms/lm/lm.js'

cssInline = '''
.repName {
    background-color: #fff;
    border: 0 solid #ccc;
    border-bottom-width: 1px;
    font: normal 10pt Arial;
    padding: 4px;
    cursor: pointer;
}
.repNameSel {
    background-color: rgb(0, 168, 94);
    border-bottom-color: transparent;
    color: white;
}
'''

# *** *** ***

def page(dbAlias, mode, userName, multiPage):
    
    return _div(
        **style(background='url(/image?bg51.jpg)', backgroundSize='100% 100%'),
        children=[
            _div(
                **style(width=200, float='left', background='rgba(210,218,203, 0.5)', padding='0 5px'),
                children=[
                    _field('type', 'list', ['Весь журнал|all', 'Ошибки|err', 'Сообщения|info', 'Отладка|debug'],
                           saveAlias=1,
                           **style(margin='10px auto', width=170, height=110)
                    ),
    
                    _field('cat', 'list', 'TYPE_ALIAS|||api.get?loadDropList&logger|keys_{FIELD}',
                           listItemClassName='repName',
                           listItemSelClassName='repNameSel',
                           **style(height='calc(100vh - 133px)', overflow='auto')
                    )
                ],
            ),
    
            _field('msg', 'fd',
                   br=1,
                   **style(overflow='auto', height='100vh', font='bold 12px Courier', background='rgba(255,255,255, 0.8)')
            ),
        ]
    )
    
# *** *** ***

def queryOpen(d, mode, ground):
    logParser()
    ls = well('logger_all', 'A L L')
    s = '\n'.join(reversed(ls))
    d.msg = s
    d.type_alias = 'all'
    
# *** *** ***

reItr = re.compile(r'\n\d\d\.\d\d\.\d\d\d\d ')
reCat = re.compile(r'\[(.+?)\]')
    
def logParser():
    lsAll = {'A L L': []}
    lsErr = {'A L L': []}
    lsInf = {'A L L': []}
    lsDbg = {'A L L': []}

    with open(sovaLogger.logFileName, 'rt', encoding='utf-8', errors='ignore') as f:
        buf = f.read()
        buf += '00.00.0000 '   # чтобы последнее сообщение не потерялось
        
    itr = re.finditer(reItr, buf)
    i1 = 0
    for it in itr:
        i2 = it.span()[0]
        if i2:
            s = buf[i1:i2]
            lsAll['A L L'].append(s)
            if ' DEBUG [' in s:
                ls = lsDbg
            elif ' ERROR [' in s:
                ls = lsErr
            else:
                ls = lsInf
            ls['A L L'].append(s)
            m = re.search(reCat, s)
            cat = m.group(1) if m else '-?-'
            ls[cat] = ls.get(cat, [])
            ls[cat].append(s)
            lsAll[cat] = lsAll.get(cat, [])
            lsAll[cat].append(s)
            i1 = i2+1

    toWell(lsAll, 'logger_all')
    toWell(lsErr, 'logger_err')
    toWell(lsInf, 'logger_info')
    toWell(lsDbg, 'logger_debug')
    
    toWell( sorted(lsErr.keys()), 'logger', 'keys_err')
    toWell( sorted(lsInf.keys()), 'logger', 'keys_info')
    toWell( sorted(lsDbg.keys()), 'logger', 'keys_debug')
    toWell( sorted(set( list(lsDbg.keys()) + list(lsInf.keys()) + list(lsErr.keys())) ), 'logger', 'keys_all')
    
# *** *** ***
