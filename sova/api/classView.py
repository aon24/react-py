# -*- coding: utf-8 -*- 
'''
Created on 7 apr 2018

@author: aon
'''

try:
    from toolsLC import err, dbg
    from tools import well, profile, tableName, cursorExecute, xunid
    from MrDB import getDB
except:
    from .. util.common import well, profile, tableName, cursorExecute, xunid
    from .. util.first import err, dbg
    from .. dbToolkit.Book import getDB

import traceback
from contextlib import suppress

# *** *** ***

class View(object):
    def __init__(self, fieldName, viewClass, dbAlias, viewAlias=None):
        self.viewClass = viewClass
        self.fieldName = fieldName
        self.dbAlias = dbAlias
        
        try:
            sqlCols = well('views', profile(dbAlias).master)[viewAlias]['sqlCols']
        except Exception as ex:
            dbg('sqlCols не найден для %s-%s' % (dbAlias, viewAlias), cat='viewClass.py.init')
            return

        sort = 'ORDER BY '

        if sqlCols[0].get('cat'): # нулевой столбец м.б. категорией
            self.where = "WHERE %s='{filtered}'" %  sqlCols[0]['name']
            name = sqlCols[1]['name']
            sort += name # сортируем по 1-му столбцу (в нулевом категория)
            if sqlCols[1].get('sort', 0) < 0:
                sort += ' DESC'
        else:
            self.where = None
            name = sqlCols[0]['name']
            sort += name # сортируем по 0-му столбцу
            if sqlCols[0].get('sort', 0) < 0:
                sort += ' DESC'

        tnv = tableName(dbAlias) + '_v_' + viewAlias

        self.sql = 'SELECT unid, {name} FROM {tnv} %s {sort} LIMIT %s'.format(name=name, tnv=tnv, sort=sort)

        dbg(sort, cat='classView.sort')
        dbg(self.sql, cat='classView.sql')

    # ***

    def loadView(self, dbAlias, offset, limit, filtered, userName):
        cat = 'classView.py.loadView'
        if hasattr(self, 'portion'):
            return self.portion(dbAlias, offset, limit, filtered, userName)

        if filtered and self.where:
            where = self.where.format(filtered=filtered)
        else:
            where = ''
        sql = self.sql % (where, str(limit))
        dbg(sql, cat=cat)

        db = getDB(dbAlias)
        if not db.con:
            err('not connection to %s:' & dbAlias, cat=cat)
            return
        
        cur = db.con.cursor()
        try:
            arr = []
            cursorExecute(cur, sql)
            arr = [xunid(row[0]) for row in cur]
            with suppress(Exception): cur.close()
            with suppress(Exception): conn.close()
            return self.viewToJson(arr)
            
        except Exception:
            err('dbAlias="%s"\nException: %s' % (dbAlias, traceback.format_exc()), cat=cat)
            with suppress(Exception): cur.close()
            with suppress(Exception): conn.close()
            return
    
# *** *** ***

