# -*- coding: utf-8 -*- 
'''
Created on 7 apr 2018

@author: aon

'''
try:
    from tools import well
    from api.forms.formTools import _div, style, _button, _btnD
    from api.classView import View
except:
    from .... util.common import well
    from sova.api.forms.formTools import _div, style, _button, _btnD
    from sova.api.classView import View



import json

# *** *** ***

class FM(View):
    def portion(self, dbAlias, offset, limit, filtered, userName):
        mainDocs = []
        i = 0
        filCat, _, filSubCat = (filtered or '').partition('|')
        filCat = filCat.replace('* All', '')
        filSubCat = filSubCat.replace('* All', '')
    
        for d in well('fmArr'):
            if filCat and d.CAT!= filCat:
                continue
            if filSubCat and d.SUBCAT != filSubCat:
                continue
    
            row = [
                d.unid,
                style('rowStyle', background='rgba(221, 238, 255, 0.5)'),
                _div(f'{d.docNo}\n{d.D("docDa")}', className='mCell', **style(color='#aaa', width='25mm'), br=1, s2=1),
                _div(className='mCell', children=[
                    _btnD( f'{d.formName} [{d.cat} / {d.subcat}]', 'docOpen', dbAlias+'&'+d.unid, title='show the result', className='docNo', br=1, **style(color='#00008b') ),
                    _btnD(d.notes or 'no comment', 'docPreView', dbAlias+'&'+d.unid, title='fast preview', **style(color='#aaa'))
                ]),
                _div(className='mCell', **style(width='35mm'), children=[
                    _button( 'show', 'docOpen', dbAlias+'&'+d.unid, **style(display='table-cell', width='15mm', marginRight=10) ),
                    _button( 'edit', 'docOpen', dbAlias+'&'+d.unid+'&edit', **style(display='table-cell', width='15mm') ),
                ]),
                _div(f'{d.D("MODIFIED")}\n{d.MODIFIER}', className='mCell', **style(width='5cm', textAlign='right', color='#aaa'), br=1, s2=1),
            ]
            mainDocs.append(row)
            i += 1
    
        header = [ style('rowStyle', color='#048', background='rgba(238, 238, 238, 0.5)'),
            _div('№\nдата', br=1, **style(width='22mm'), className='hCell'),
            _div('form', br=1, className='hCell'),
            _div('', **style(width='40mm'), className='hCell'),
            _div('counter: %d' % i, **style(width='30mm'), className='hCell'),
        ]
        
        return 200, 'application/json', json.dumps({'mainDocs': mainDocs, 'header': header}, ensure_ascii=False)

