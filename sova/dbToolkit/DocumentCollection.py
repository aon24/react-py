# -*- coding: utf-8 -*-

from .. util.common import xunid, cursorExecute
from .. util.first import err

class DocumentCollection:
    """коллекция документов (итератор)
    sql - должен возвращать unid в первом столбце"""
    
    def __init__(self, db, sql = 'SELECT DISTINCT unid FROM {0}_docs;', includeDeleted = False):
        self.db = db
        self.sql = sql.replace('{0}', db.dbTable)
        self.cur = db.con.cursor()
        self.index = 0
        self.empty = True
        self._unid0 = ''
        try:
            cursorExecute(self.cur, self.sql)
            row0 = self.cur.fetchone()
            if row0 and row0[0]:
                self.empty = False
                self._unid0 = xunid(row0[0])
        except Exception as ex:
            err('MrDB.py DocumentCollection.__init__(dba = %r, sql = %r) Exception: %s' % (db.alias, sql, ex))
            raise
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.empty:
            raise StopIteration
        
        while 1:
            if self.index == 0:
                unid = self._unid0
            else:
                row = self.cur.fetchone()
                if not row:
                    raise StopIteration
                unid = xunid(row[0])
            
            self.index += 1
            
            d = self.db.getDocumentByUNID(unid)
            if d and not d.ERASER:
                return d
    
    def __del__(self):
        try:
            self.cur.close()
        except:
            pass

# *** *** ***

if __name__ == "__main__":
    pass
