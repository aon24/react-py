# -*- coding: utf-8 -*- 
'''
Created on 7 apr 2018

@author: aon

'''
from ... forms.formTools import _div, style, _button, _btnD

from .. .. util.first import err
from .. .. dbToolkit.Book import getDB
from ... classView import View

import json

# *** *** ***
class Outline(View):
    def portion(self, dbAlias, offset, limit, filtered, userName):
        count = int(limit)
    
        db = getDB(dbAlias)
        if not db:
            err('DB not open: %s' % dbAlias)
            return 400, 'text/html; charset=UTF-8', 'DB not open: %s' % dbAlias
        
        mains = {}
        
        for d in db.search( "(xnam='FORM') AND (xval = 'topic')" ):
            mains[d.title] = d
        
        i = 0
        mainDocs = []
        refsDocs = {}
        for title in sorted(mains):
            d = mains[title]
            unid = d.unid
            row = [
                unid,
                _btnD(title, 'docInIframe', dbAlias+'&'+unid, s2=0, className='mCell', **style(width=200)),
            ]
            mainDocs.append(row)
    
            responses = db.getResponses(d.unid)
            if responses:
                refs = []
                for d in sorted( responses, key=lambda x: x.o_level ):
                    if d.dir != 'd':
                        add = '- ' if d.o_level.count('.') < 2 else ('\xa0' + ' └─ ')
                        row = [
                            d.unid,
                            _btnD( add + d.title, 'docInIframe', dbAlias+'&'+d.unid, className='rCell', **style(fontFamily='Arial', width=200)),
                        ] # └─
                        refs.append(row)
                    
                if refs:
                    refsDocs[unid] = refs
            
            i += 1
            if i >= count:
                break
    
        return 200, 'application/json', json.dumps({'mainDocs': mainDocs, 'refsDocs': refsDocs}, ensure_ascii=False)

