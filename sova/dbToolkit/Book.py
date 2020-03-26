# -*- coding: utf-8 -*-

from .Document import Document
from .DocumentCollection import DocumentCollection
from .. util.common import *
from .. util.first import *

import sqlite3 as sqldb
import uuid

def connectToSrv(dbAlias):
    dbPath = f"{os.getcwd()}/{well('path')}BOOKS/{tableName(dbAlias)}.rsf"
    try:
        return sqldb.connect(database=dbPath, timeout=10.0)
    except Exception as ex:
        err(f'SQLITE: {dbPath}\n{ex}', cat='error_connect')


def getDB(dbAlias, un=''):
    if dbAlias:
        dbAlias = dbAlias.upper()
        con = connectToSrv(dbAlias)
        if con:
            return Book(con, dbAlias, un)
        else:
            err('No connection to %s' % dbAlias, 'getDB')


def dbExists(dbAlias, cls=None):
    try:
        con = connectToSrv(dbAlias)
        if not con:
            return

        cur = con.cursor()
        cur.execute("SELECT unid FROM %s_docs limit 1;" % tableName(dbAlias))
        for row in cur:
            return True
    except Exception as ex:
        err('dbExists: %s' % ex)
    finally:
        try:
            cur.close()
        except:
            pass
        try:
            con.close()
        except:
            pass
        

# *** *** ***


def createDB(dbAlias):
    con = connectToSrv(dbAlias)
    if not con:
        raise Exception('Can not take connect to SQL server to create database "%s"' % dbAlias)

    sql = '''CREATE TABLE {0}_docs (
unid BINARY(16) NOT NULL,
xcrt TIMESTAMP NULL,
xnam TEXT(255) NOT NULL,
xval TEXT(65000) NULL,
xmdf TIMESTAMP NULL);
CREATE INDEX {0}_n ON {0}_docs (xnam, xmdf);
CREATE INDEX {0}_u ON {0}_docs (unid, xmdf);
CREATE INDEX {0}_m ON {0}_docs (xmdf);
CREATE INDEX {0}_m ON {0}_docs (xcrt);
'''
    db = Book(con, dbAlias, 'DB Creator')
    db.exx(sql.format(db.dbTable))
    db.con.commit()
    
    snd('Created database "%s"' % dbAlias)
    return db

# *** *** ***

class Book:
    def __init__(self, con, alias, un=''):
        self.alias = alias
        self.dbTable = tableName(alias)
        self.con = con
        self.userName = un or 'Anonymous'
        self.fileStores = [DC({'name':'Sova', 'path': well('path') + 'BOOKS/attachments'}), DC({'name':'file', 'path': well('path') + 'BOOKS/files'})] # файлохранилища могут со временем добавляться. Upload в самое первое 

    def exx(self, sql):
        flag = True
        cur = self.con.cursor()
        for s in sql.split(';\n'):
            if s:
                try:
                    cursorExecute(cur, s)
                except Exception as ex:
                    err('Database.exx(sql = %s)\nException: %s' % (sql, ex))
                    flag = False
        cur.close()
        return flag
    

    def deleteDocument(self, unid):
        try:
            d = self.getDocumentByUNID(unid)
            if d.eraser:
                raise Exception('The document has already been deleted')
            d.eraser = self.userName
            d.uneraser = ''
            if d.dir:
                d.oldDir = d.dir
                d.dir = 'D'
            if d.ref:
                d.deletedRef = d.ref
                d.ref = ''
            if d.save(True):
                return d
        except Exception as ex:
            err(f'Exception: deleteDocument(unid={unid})\n{ex}', cat='Book')
    
    def undeleteDocument(self, unid):
        try:
            d = self.getDocumentByUNID(unid)
            if not d.eraser:
                raise Exception('The document has not been deleted')
            d.eraser = ''
            d.uneraser = self.userName
            if d.oldDir:
                d.dir = d.oldDir
                d.oldDir = ''
            if d.deletedRef:
                d.ref = d.deletedRef
                d.deletedRef = ''
            if d.save(True):
                return d
        except Exception as ex:
            err(f'Exception: undeleteDocument(unid={unid})\n{ex}', cat='Book')
            return False



    def getResponses(self, unid):
        """возвращает коллекцию подчиненных документов"""
        sql = f"SELECT DISTINCT unid FROM {self.dbTable}_docs WHERE (xmdf IS NULL) AND (xnam='REF') AND (xval='{unid.upper()}')"
        return DocumentCollection(self, sql)
    
    
    
    def getDocumentByUNID(self, unid):
        """
        возвращает документ по unid. unid - текстовый hex
        """
        
        def er(msg):
            err(f'getDocumentByUNID({unid}), db: {self.alias}. Msg: {msg}', cat='Book')
        
        if not isHex(unid):
            return
        
        try:
            sql = "SELECT xnam, xval, xcrt FROM {0}_docs WHERE (unid = X'{1}') AND (xmdf IS NULL);"
            sql = sql.format(self.dbTable, unid)
            cur = self.con.cursor()
            try:
                cursorExecute(cur, sql)
            except Exception as ex:
                err(f'WARNING {self.alias} getDocumentByUNID({unid}): {ex}', cat='Book')
                return
            
            if not cur:
                return er('can not execute SQL')
            
            d = Document(self)
            
            modified = None
            created = None
            i = 0
            for row in cur:
                i += 1
                d.f[row[0].upper()] = row[1]
                if row[2]:
                    modified = row[2] if (not modified or modified < row[2]) else modified
                    created = row[2] if (not created or created > row[2]) else created
            
            if not i:
                return
            
            if modified and 'MODIFIED' not in d.f:
                d.f['MODIFIED'] = modified.partition('.')[0]
            
            if created and 'CREATED' not in d.f:
                d.f['CREATED'] = created.partition('.')[0]
            
            if 'UNID' not in d.f:
                d.f['UNID'] = unid
            
            return d
        
        except Exception as ex:
            er(ex)
        
        finally:
            try:
                cur.close()
            except:
                pass
    

    def getDocumentHistory(self, unid):
        """
        возвращает список [(xcrt, xnam, xval, xmdf), ...] по unid. unid - текстовый hex
        """
        try:
            sql = f"SELECT xcrt, xnam, xval, xmdf FROM {self.dbTable}_docs WHERE (unid = X'{unid}');"
            cur = self.con.cursor()
            cursorExecute(cur, sql)
            
            if cur:
                return [tuple(str(row[0]), row[1] or '', row[2] or '', str(row[3] or '')) for row in cur]

            err('can not execute SQL')
        
        except Exception as ex:
            err(f'ERROR Database.getDocumentHistory: {ex}\nSQL: {sql}', cat='Book')
            raise ex
        
        finally:
            try:
                cur.close()
            except:
                pass

    def allDocuments(self):
        """
        возвращает коллекцию всех документов БД
        """
        sql = f"SELECT DISTINCT unid FROM {self.dbTable}_docs WHERE (xmdf IS NULL)"
        return DocumentCollection(self, sql)
    
    
    def search(self, whereClosure):
        """
        возвращает коллекцию найденных в БД документов
        """
        sql = "SELECT DISTINCT unid FROM {0}_docs WHERE (xmdf IS NULL) AND (%s)" % whereClosure
        return DocumentCollection(self, sql)

    def searchUNIDs(self, whereClosure=''):
        """
        возвращает unid`ы найденных в БД документов
        """
        whcs = []
        if whereClosure:
            whcs += ['xmdf IS NULL', whereClosure]
        
        whcs += ["unid NOT IN (SELECT DISTINCT unid FROM {0}_docs WHERE (xmdf IS NULL) AND (xnam = 'ERASER') AND (xval != ''))"]
        
        sql = 'SELECT DISTINCT unid FROM {0}_docs'
        if whcs:
            sql += ' WHERE %s' % ' AND '.join('(%s)' % x for x in whcs)
        
        sql = sql.replace('{0}', self.dbTable)
        
        try:
            cur = self.con.cursor()
            cursorExecute(cur, sql)
            return [xunid(r[0]) for r in cur]
        except Exception as ex:
            err('Database.searchUNIDs(whereClosure=%r):\n  Exception: %s\n  sql=%s' % (whereClosure, ex, sql))
            return []
        finally:
            cur.close()
 
    def createDoc(self):
        d = Document(self)
        d.__dict__['isNew'] = True
        d.f['UNID'] = uuid.UUID(int=uuid.uuid1().int ^ uuid.uuid4().int).hex.upper()
        return d
    
    def __del__(self):
        try:
            self.con.close()
        except:
            pass

# *** *** ***

def getDocByUnid(unid, dbAlias, un=''):
    try:
        return getDB(dbAlias, un).getDocumentByUNID(unid)
    except:
        dbg(f'docopen?{dbAlias}&{unid}', 'exception getDocByUnid')

# *** *** ***

if __name__ == "__main__":
    pass