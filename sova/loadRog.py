# -*- coding: utf-8 -*-

from .dbToolkit.Book import getDB, dbExists
from .api.forms.formTools import _div, style, _btnD
from .util.common import DC, well, toWell, appendWell

import json

def loadRog(dbAlias):
    if not (dbAlias and dbExists(dbAlias)):
        return

    db = getDB(dbAlias, None)
    
    rogView = {}
    rogDC = {}
    
    for d in db.allDocuments():
        if d.form.lower() != 'askrog':
            continue
        
        o = {}
        for x in ['RGAKK', 'RGASK', 'RGASK2', 'RGCODE', 'RGPART', 'RGSUBJ', 'RGTHEME']:
            o[x] = d.F(x)
        rogDC[d.unid] = o
        
        if d.rgAsk2:
            s = '+...' + d.rgCode[10:24]
            ask = d.rgAsk.lower()
            r = [
                    _div( '└──', className='mCell', **style(color='#048', width=38)),
                    _btnD( d.rgCode[20:24] + '.' + d.rgAsk2, 'showAsk', d.unid, className='mCell', title='+'+d.rgCode, **style(color='#048', font='normal 9pt Arial', textDecoration='underline') ),
                ]
        else:
            s = '+' + d.rgCode
            ask = ''
            r = [
                    _div( d.rgCode[15:19] + '. ', className='mCell', **style(fontWeight='bold', color='#048', border=0, width=38)),
                    _btnD( d.rgAsk, 'showAsk', d.unid, className='mCell', **style(fontWeight='bold', color='#55f', textDecoration='underline') ),
                ]
        r.append(_btnD(s, 'addAsk', d.unid, className='rgCode', title='добавить вопрос'))

        fts = '=' + d.rgCode[15:19] + '=' + d.RGSUBJ.lower() + ask # + RGAKK + RGTHEME
        rogView[ d.rgCode[15:24] ] = [d.unid, fts] + r
        
        
        toWell(d, 'rgCode', d.rgCode)
        toWell(d.rgCode[:19], 'rgCode18', d.rgCode[15:19])
        version(d, 'verRubrOG')
        
        rgc = d.rgCode[:10] + '0000.0000'
        if not well('rgCode', rgc):
            dc = DC(d)
            dc.RGSUBJ = ''
            d.RGASK   = ''
            d.RGASK2  = ''
            toWell(dc, 'rgCode', rgc)
            
        rgc = d.rgCode[:15] + '0000'
        if not well('rgCode', rgc):
            dc = DC(d)
            d.RGASK   = ''
            d.RGASK2  = ''
            toWell(dc, 'rgCode', rgc)
            
        
        rgPart = d.rgCode[3:5] + ' ' + d.rgPart
        rgTheme = d.rgCode[7:10] + ' ' + d.rgTheme
        rgSubj = d.rgCode[12:16] + ' ' + d.rgSubj

        if rgPart  not in well('rgPartList'):
            appendWell(rgPart, 'rgPartList')
        if rgTheme not in well('rgThemeList', rgPart):
            appendWell(rgTheme, 'rgThemeList', rgPart)
            appendWell(rgTheme, 'rgThemeList+000' + rgPart[0])
        if rgSubj not in well('rgSubjList', rgPart, rgTheme):
            appendWell(rgSubj, 'rgrgSubjList', rgPart, rgTheme)

    rog = db.getDocumentByUNID('1718'*8)
    dic1718 = eval(rog.dic1718) if rog and rog.dic1718 else {}
    toWell(dic1718, 'dic1718')
    
    ls = [rogView[x] for x in sorted(rogView)]
    o = json.dumps(ls, ensure_ascii=False).replace('], [', '],\n[')
    toWell(o, 'readyLists', 'rogView')

    o = json.dumps(rogDC, ensure_ascii=False)
    toWell(o, 'readyLists', 'rogDC')
    
# *** *** ***

def version(d, s):
    if not well(s) or d.modified > well(s):
        toWell(s, d.modified)

# *** *** ***
