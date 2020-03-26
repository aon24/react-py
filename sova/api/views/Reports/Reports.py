# -*- coding: utf-8 -*- 
'''
Created on 7 apr 2018

@author: aon

'''
try:
    from .... dbToolkit.Book import getDB
    from util.first import err
except:
    from MrDB import getDB
    from toolsLC import err

from ...forms.formTools import _btnD, _div
from api.classView import View

import json
import time

# *** *** ***

class Reports(View):
    def __init__(self, fieldName, viewClass, dbAlias, viewAlias):
        View.__init__(self, fieldName, viewClass, dbAlias, viewAlias)

    # ***
    
    def viewToJson(self, arr):
        
        w = [{'width': '22mm'}, {}, {'width': '22mm'}, {'width': '22mm'}, {'width': '10mm'}]
        mainDocs = []
        refsDocs = {}
        
        db = getDB(self.dbAlias)
        for unid in arr:
            dl = db.getDocWithResponses(unid)
            if not dl:
                continue
            
            d = dl[0]
            if d._ENDTIME:
                s = '%Y-%m-%d %H:%M:%S'
                try:
                    delta = time.mktime(time.strptime(d._ENDTIME, s)) - time.mktime(time.strptime(d._STARTINGTIME, s))
                except:
                    s = '%d.%m.%Y %H:%M:%S'
                    delta = time.mktime(time.strptime(d._ENDTIME, s)) - time.mktime(time.strptime(d._STARTINGTIME, s))
                d._run_ = ' [ %s, время %d:%02d ]' % ( d.CREATOR.split()[0], int(delta/60), int(delta%60))
                
            else:
                d._run_ = ' [ %s, выполняется ]' % d.CREATOR.split()[0]
            
            responses = dl[1:]
        
            nn = 0
        
            if responses:
                refs = []
                for dd in sorted( responses, key=lambda x: x.o_level ):
                    if dd.ref:
                        row = [
                        dd.unid,
                        _div('\xa0', className='mCell', style=w[0]),
                        _btnD(dd.CATNAME, 'docOpen', self.dbAlias+'&'+dd.unid, className='mCell docNo', style=w[1]),
                        _div('\xa0', className='mCell', style=w[2]),
                        _div('\xa0', className='mCell', style=w[3]),
                        _div(dd.N or '\xa0', className='mCell', style=w[4]),
                        ]
                        refs.append(row)
                        nn += int(dd.N or 0)
                    
                if refs:
                    refsDocs[unid] = refs
            
            row = [
                unid,
                _btnD('%s\n%s' % (d.docNo, d.D('docDa') ), 'docPreView', self.dbAlias+'&'+unid, s2=1, className='mCell docNo', style=w[0], br=1),
                _div('%s\n%s\n%s' % (d.REPORTCAT, d.REPORTNAME, d._run_), className='mCell', style=w[1], s2=1, br=1),
                _div('%s\n%s' % (d.DT1, d.DT3), className='mCell', style=w[2], s2=1, br=1),
                _div('%s\n%s' % (d.DT2, d.DT4), className='mCell', style=w[3], s2=1, br=1),
                _div(str(nn), className='mCell', style=w[4]),
            ]
            mainDocs.append(row)
    
        header = [
                    _div('№', style=w[0], className= 'hCell'),
                    _div('отчет', style=w[1], className= 'hCell'),
                    _div('начало', style=w[2], className= 'hCell'),
                    _div('конец', style=w[3], className= 'hCell'),
                    _div('\xa0', style=w[4], className= 'hCell'),
                ]
        
        return 200, 'application/json', json.dumps({'mainDocs': mainDocs, 'refsDocs': refsDocs, 'header': None}, ensure_ascii=False)

