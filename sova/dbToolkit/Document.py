# -*- coding: utf-8 -*-
from .. util.common import *
from .. util.first import *
from .DocumentCollection import DocumentCollection

import time

class Document(object):
    """
    документ. поля в словаре f
    """
    
    def __init__(self, db):
        self.__dict__['db'] = db
        self.__dict__['isNew'] = False
        self.__dict__['f'] = {}
    
    def __getattr__(self, fieldName):
        return self.f.get(fieldName.upper(), '')
    
    def __setattr__(self, fieldName, fieldValue):
        if fieldName not in ['db', 'f', 'isNew']:
            self.f[fieldName.upper()] = str(fieldValue)
    
    def F(self, fieldName):
        return self.f.get(fieldName.upper(), '')
    
    def A(self, fieldName):
        return self.f.get(fieldName.upper(), '').split('\n')
    
    def S(self, fieldName, fieldValue):
        if fieldName not in ['db', 'f', 'isNew']:
            self.f[fieldName.upper()] = str(fieldValue)
            
    def D(self, fieldName):
        s = ''
        for k in self.f.get(fieldName.upper(), '').split('\n'):
            if k:
                try:
                    s += time.strftime('%d.%m.%Y\n', time.strptime(k.partition(' ')[0], '%Y-%m-%d'))
                except:
                    s += k + "\n"
        return s[:-1] if s else ''

    
    def __str__(self):
        return 'Document:\n' + '\n'.join(
            x[:200] + '..."' if len(x) > 200 else x for x in (
                k + ' = "%s"' % '\n\t'.join('\n'.join(self.A(k)).split('\n')) for k in sorted(self.f)
            )
        )
        
    def getResponses(self):
        """возвращает коллекцию подчиненных документов"""
        sql = "SELECT DISTINCT unid FROM %s_docs WHERE (xmdf IS NULL) AND (xnam = 'REF') AND (xval = '%s')" % (self.db.dbTable, self.UNID)
        return DocumentCollection(self.db, sql)
    
    def save(self, commit = False, existF = None):
        def bad(fval):
            return any(c in fval for c in "\\\"()'[] \t\r\n") # check for SQL injection

        def _exx(st):
            try:
                cursorExecute(cur, st)
                return True
            except Exception as ex:
                err('SQL %s\n%s' % (ex, st), 'Document.save()')
                try:
                    cur.close()
                except:
                    pass
                return False

        unid = self.UNID
        if unid == '' or bad(unid):
            err('invalid unid "%s"' % unid, 'Document.save()')
            return False
        xunid = "X'%s'" % unid
        
        tm = "'%s'" % datetime.now()
# перевести в историю старые значения полей
        sqlUpd = "UPDATE {0}_docs SET xmdf = {2} WHERE (unid = {1}) AND (xmdf IS NULL) AND (%s);".format(self.db.dbTable, xunid, tm)
# вставить новые значения полей
        sqlIns = "INSERT INTO {0}_docs (unid, xcrt, xnam, xval) VALUES ({1}, {2}, '%s', '%s');".format(self.db.dbTable, xunid, tm)
# обновить значения служебных полей (restricted fields)
        sqlRest = "UPDATE {0}_docs SET xcrt = {2}, xval = '%s' WHERE (unid = {1}) AND (xnam = '%s');".format(self.db.dbTable, xunid, tm)
        
        if self.isNew:
            df = {}
        elif existF:
            df = existF
        else:
            dd = self.db.getDocumentByUNID(unid)
            if not dd:
                dbg('Документ исчез', 'doc.save')
                return False
            df = dd.f
        
        histFi = []
        chFi = []
        restFi = []
        
        un = self.db.userName.replace("'", "''")
        
        if df: # не новый документ
            for k in self.f:
                if k in ['CREATOR', 'CREATED', 'MODIFIER', 'MODIFIED', 'UNID', 'ISNEW'] or bad(k):
                    continue
                if (k[0] == '_') and (k in df) and (df[k] != self.f[k]): # сущ. служ. поле с новым знач.
                    restFi.append(k)
                elif k not in df:           # новое поле
                    if self.f[k] != '':     # с непустым знач.
                        chFi.append(k)
                elif df[k] != self.f[k]:    # сущ. поле с новым знач.
                    histFi.append(k)
                    chFi.append(k)
            if (chFi or histFi) and self.MODIFIER != un:  # есть изм. в неслуж. полях, новый modifier
                self.MODIFIER = un
                histFi.append('MODIFIER')
                chFi.append('MODIFIER')
        else: # новый документ
            for k in self.f:
                if k in ['CREATOR', 'CREATED', 'MODIFIER', 'MODIFIED', 'ISNEW'] or bad(k):
                    continue
                if self.f[k]:
                    chFi.append(k)
            if chFi:
                self.CREATOR = un
                chFi.append('CREATOR')
                self.__dict__['isNew'] = False
        
        if chFi or histFi or restFi:        # есть изм.
            sql = []
            
            if histFi:
                sql.append( sqlUpd % " OR ".join("(xnam = '%s')" % fn for fn in histFi) )
            for k in chFi:
                sql.append( sqlIns % (k, self.f[k].replace("'", "''")) )
            for k in restFi:
                sql.append( sqlRest % (self.f[k].replace("'", "''"), k) )
            
            cur = self.db.con.cursor()
            for s in sql:
                if not _exx(s):
                    self.db.con.rollback()
                    return False
            cur.close()
            
            if commit:
                self.db.con.commit()
        
        return True
    
    def attDescrs(self):
        return [
            self.f[k].split('|')
            for k in self.attFields()
        ]
    
    def attFields(self, arr = []):
        return [
            k for k in self.f
            if k.startswith('FILES')
            and ((k.split('_')[0] in arr) if arr else ('_' in k))
            and self.f[k].count('|') > 1
        ]
    
    def clearAttFields(self, attF = None):
        for fname in self.attFields(attF):
            self.S(fname, '')
                
# *** *** ***

if __name__ == "__main__":
    pass
