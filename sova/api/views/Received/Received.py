# -*- coding: utf-8 -*- 
'''
Created on 7 apr 2018

@author: aon

'''
from tools import *
from MrDB import getDB, dbExists, takeConnect
from api.forms.formTools import _div, _btnD, style, _field, _br
from api.classView import View

import json

# *** *** ***


def oneDB(dbAlias):
    cat = 'Recived.py.oneDB'
    conn = takeConnect(dbAlias)[1]
    if not conn:
        err('not connection to %s:' % dbAlias, cat=cat)
        return
    
    cur = conn.cursor()

    if '/OGTZ_' in dbAlias:
        _sql1 = """SELECT unid, unregfromno FROM {tal}_v_unreg ORDER BY unregfromno DESC LIMIT 51"""
    else:
        _sql1 = """SELECT unid, created FROM {tal}_v_unreg ORDER BY created DESC LIMIT 51"""
    
    _sql2 = """SELECT d.unid, v.vm FROM {tal}_docs AS d INNER JOIN 
    (SELECT unid AS vu, mdfdate AS vm FROM {tal}_v_bymodified WHERE form in ('rkckg', 'RKCKG') ORDER BY vm DESC LIMIT 500) AS v ON d.unid=v.vu 
    WHERE (d.xmdf IS NULL) AND (d.xnam='MODIFIER') AND (d.xval='Прием из СЭД (rsMail или VipNet)') ORDER BY v.vm DESC LIMIT 50;"""
    
    tal = tableName(dbAlias)

    try:
        s = _sql1.format(tal=tal)
        cursorExecute(cur, s)
        arr = [xunid(row[0]) for row in cur]

        s = _sql2.format(tal=tal)
        cursorExecute(cur, s)
        arr += [xunid(row[0]) for row in cur]

        with suppress(Exception): cur.close()
        with suppress(Exception): conn.close()
        return arr
        
        
    except Exception as ex:
        err('dbAlias="%s"\nException: %s' % (dbAlias, ex), cat=cat)
        with suppress(Exception): cur.close()
        with suppress(Exception): conn.close()
        return

# *** *** ***

class Received(View):
    def portion(self, dba, offset, limit, filtered, userName):
        count = int(limit)
        dn = dba.partition('/')[0]
    
        mains = {}
        
        for prof in well('dbByDN', dn):
            dbAlias = prof.dbAlias
            if ('/OG' not in dbAlias) or ('/OGI' in dbAlias):
                continue
            if not any( x in dbAlias for x in ('/OGKPI_', '/OGLP_', '_2019', '_2020') ):  # Шатохин 1743 от 05.09.2019
                continue
            
            try:
                if not dbExists(dbAlias):
                    continue

                arr = oneDB(dbAlias)
                if not arr:
                    continue
   
                db = getDB(dbAlias)
                j = 0
                for unid in arr:
                    d = db.getDocumentByUNID(unid)
                    # при приеме переметок/оутлетов MODIFIER='Прием из СЭД (rsMail или VipNet)'
                    # и РКЦК опять попадают в вид
                    if not d.SENTFROMDB or d.dir != '0': # or d.clsDa
                        continue
                    
                    if d.docNo:
                        sentFromDB_crt = 0
                        ls = d.db.getDocumentHistory(d.unid) # возвращает список [(xcrt, xnam, xval, xmdf), ...] по unid. unid - текстовый hex
                        for tup in ls:
                            if tup[1] == 'SENTFROMDB':
                                sentFromDB_crt = datetime.strptime(tup[0].partition('.')[0], '%Y-%m-%d %H:%M:%S')
                                break
                        mdf = datetime.strptime(d.MODIFIED, '%Y-%m-%d %H:%M:%S')
                        if (mdf - sentFromDB_crt).seconds > 30: # datetime.timedelta.seconds
                            continue # РК изменена переметкой или оутлетом, пришедешем снизу потом
    
                    d._run_ = dbAlias + ': ' + d.unid
                    d_key = (
                        d.MODIFIED or d.CREATED,
                        max(d.A('ADDDA')),
                        d.unid,
                    )
                    mains[d_key] = d
                    j += 1
                    if j > count:
                        break
            except Exception as ex:
                err(str(ex), cat='view-received')
        
        # ***
        
        i = 0
        plus = ''
        mainDocs = []
        refsDocs = {}
        url = '/newdoc?{0}&Переметка ОГ&{0}&{1}'
        
        for d_key in sorted(mains, reverse=True):
            i += 1
            if i > count:
                plus = '+'
                break

            d = mains[d_key]
            unid = d.unid
            if d.docNo:
                no = d.pref + d.docNo + d.suff
                dt = dateFromDB(d.docDa)
            else:
                no = d.A('addNo')[-1]
                dt = dateFromDB(d.A('addDa')[-1])
            row = [
                unid,
                {'rowStyle': {'background': 'rgba(221, 238, 255, 0.5)'}},
                _btnD( '%s\n%s' % (no, dt ),
                       'xopen', 'fulltextSearchWithNav?%s&bynum&unid=%s' % (d.db.alias, unid),
                       title='открыть в журнале',
                       s2=1, br=1,
                       className='mCell docNo',
                       **style(color= '#840' if d.docNo else '#77f', width='26mm')),
                _btnD( '%s\n(%s)' % (d.fromCorr, d.rnn ), 'docPreView', d.db.alias+'&'+unid, title='просмотреть', s2=1, className='mCell docNo', br=1, **style(color='#00008b') ),
                _btnD( d.subj[:100], 'docOpen', d.db.alias+'&'+unid+'&edit', title='редактировать (присвоить вх. номер)', className='mCell docNo', **style(color='#000') ),
                _div('%s\n%s' % (d.D('MODIFIED'), d.MODIFIED.partition(' ')[2]), className='mCell', **style(textAlign='right', color='#aaa'), br=1, s2=1),
            ]
            mainDocs.append(row)
        
            for o in d.getResponses(): # sorted( responses, key=lambda x: x.o_level ):
                if o.form == 'o':
                    row = [
                        o.unid,
                        {'rowStyle': {'background': 'rgba(255, 255, 255, 0.75)'}},
                        _div('\xa0', className='mCell'),
                        _btnD( o.fromWho, 'oPreView', o.db.alias+'&'+o.unid, title='просмотреть', className='mCell docNo'),
                        _div(o.res[:100] or 'без резолюции', className='mCell'),
                            _btnD( 'Перем', 'xopen', url.format(o.db.alias, o.unid), title='переметить', className='mCell docNo')
                                if d.docNo else 
                            _btnD( 'Регистрация', 'xopen', 'fulltextSearchWithNav?%s&bynum&unid=%s' % (d.db.alias, unid), title='открыть в журнале', className='mCell docNo'),
    
                    ]
                    refsDocs[unid] = [row]
                    break
    
        return 200, 'application/json', json.dumps({'mainDocs': mainDocs, 'refsDocs': refsDocs, 'setField': '%s_h|%d%s' % (self.fieldName, i, plus)}, ensure_ascii=False)

    # ***

    def header(self):
        return _div( **style(color='#048', background='rgba(238, 238, 238, 0.5)', width='100%', display='table'),
            className='header',
            children=[
            _div('№\nдата', br=1, style={'width': '28mm'}, className='hCell'),
            _div('ФИО\nзаявителя', br=1, style={'width': '60mm'}, className='hCell'),
            _div( **style(width='auto', display='table-cell'),
                  children=[
                    _div('краткое содержание', style={'display': 'block', 'width': 'auto', 'margin': 'auto'}, className='hCell'),
                    _btnD('(обновить список)', 'viewRefresh', self.fieldName, **style(display='block', textDecoration='underline', fontWeight='normal'), className='hCell')
                ]),
            _div(style={'width': '22mm'}, className='hCell',
                children=[
                    _div('получено'),
                    _field('%s_h' % self.fieldName, 'fd')
                ])
        ])
