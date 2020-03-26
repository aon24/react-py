# -*- coding: utf-8 -*- 
'''
AON 9 mar 2018

'''
try:
    from tools import well
    from toolsLC import config, DC
    from common import toWell
    from MrDB import getDB
except:
    from .... util.common import well, toWell, DC, config
    from .... dbToolkit.Book import getDB
    
from .. formTools import _table, _div, style, label, _field, labField
from ...views.viewTools import viewDiv

from importlib import import_module, reload

# *******************

def initForm():
    pass

# *** *** ***

title = 'fm'
cssUrl = ['jsv?api/views/view.css', 'jsv?api/forms/fm_manager/fm_manager.css']
javaScriptUrl = 'jsv?api/forms/fm_manager/fm_manager.js'

# **** *** ***

def page(dbAlias, mode, userName, multiPage):
    return _div(
    
    **style(backgroundImage='url(/image?bg51.jpg)', backgroundSize='100% 100%'),
    focus='cat',
    children = [
        _div( 
            **style(maxWidth=1000),
            className='row',
            children=[
                style('rowStyle', width='auto', margin='auto'),
                _div( **style(width='50mm', height='100vh', paddingRight=5),
                      className='cellbg-green',
                      children=_table(
                        [_div('repository', **style(font='normal 12px Verdana', color='#048'))],
                        [_field('repository', 'repository', readOnly=1,  **style('ttaStyle', font='normal 11px/1.4 Verdana'))],
                        [label()],
                        [_field('cat', 'list', 'lsCat')],
                        [label()],
                        [_field('subCat', 'list', 'CAT|||api.get?loadDropList&lsCat|{FIELD}',
                                **style(width='90%', margin='auto', display='block'),
                                saveAlias=1,
                                listItemClassName='repName',
                                listItemSelClassName='repNameSel',)],
                    )),
                viewDiv(
                    fieldName = 'view1',
                    viewClass='FM',
                    **style(height='calc(100vh - 35px)', background='#fff'),
                    dbAlias=dbAlias,
                    toolbar='fm',
                    form='fm_svg',
                    title='new form',
                )
            ]
        )
    ]
)
    
# *** *** ***

def queryOpen(d, mode, ground):
    d.cat = '* All'
    d.repository = d.db.alias.lower();
    if well('fmArr'):
        return
    
    db = getDB(d.db.alias, d.db.userName)
    
    s2 = "SELECT unid FROM %s_docs WHERE (xmdf IS NULL) AND (xnam='FORM') AND (xval='fm_svg')" % db.dbTable
    cnd = "(xnam='MAIN') AND (xval='1') AND (unid IN (%s))" % s2

    mains = {}
    fmArr = []
    lsCat = {'* All': ['* All']}
    lsComp = []
    lsHtml = []
    lsSvg = []
    for dd in db.search(cnd):
        mains['%7s' % dd.docNo + dd.unid] = DC(dd)

    for x in sorted(mains, reverse=True):
        dc = mains[x]
        fmArr.append(dc)
        
        toWell(dc, 'fmByUnid', dc.unid)
        dc.cat = dc.cat or '<empty>'
        dc.subCat = dc.subCat or '<empty>'

        toWell(dc.unid, 'fmByCat', '* All', '* All')
        toWell(dc.unid, 'fmByCat', dc.cat, '* All')
        toWell(dc.unid, 'fmByCat', dc.cat, dc.subCat)
        ls = lsCat.get(dc.cat, ['* All'])
        if dc.subCat not in ls:
            ls.append(dc.subCat)
            lsCat[dc.cat] = ls
        if dc.subCat not in lsCat['* All']:
            lsCat['* All'].append(dc.subCat)
            
        if dc.cat == 'HTML-fragment':
            lsHtml.append(dc.formName + '|' + dc.unid)
        elif dc.cat == 'SVG':
            lsSvg.append(dc.formName + '|' + dc.unid)
        
    lsCat = { k: lsCat[k] for k in sorted(lsCat) }
        
    toWell(fmArr, 'fmArr')
    toWell(lsCat, 'lsCat')
    toWell(lsHtml, 'lsHtml')
#     toWell(lsSvg, 'lsSvg')
    
# *** *** ***









