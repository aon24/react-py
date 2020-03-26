# -*- coding: utf-8 -*-
from . first import snd, err

import re
from binascii import hexlify
import os, shutil
import time
from datetime import datetime
import traceback
import threading

# *** *** ***

class DC(object):
    def __init__(self, d = None):
        if d:
            if type(d) is dict:
                self.__dict__['f'] = {k.upper(): v for (k,v) in d.items()}
            else:
                self.__dict__['f'] = {k.upper(): v for (k,v) in d.f.items()}
        else:
            self.__dict__['f'] = {}
        
    def __getattr__(self, fieldName):
        return self.f.get(fieldName.upper(), '')
    
    def __setattr__(self, fieldName, fieldValue):
        fn = fieldName.upper()
        if fn != 'F':
            self.f[fn] = fieldValue
    
    def F(self, fieldName):
        return self.f.get(fieldName.upper(), '')
    
    def A(self, fieldName):
        return self.f.get(fieldName.upper(), '').split('\n')
    
    def S(self, fieldName, fieldValue):
        fn = fieldName.upper()
        if fn != 'F':
            self.f[fn] = fieldValue
            
    def D(self, fieldName):
        s = ''
        for k in self.f[fieldName.upper()].split('\n'):
            if k:
                try:
                    s += time.strftime('%d.%m.%Y\n', time.strptime(k.partition(' ')[0], '%Y-%m-%d'))
                except:
                    s += k + "\n"
        return s[:-1] if s else ''
        
    def __str__(self):
        return 'DC:\n' + '\n'.join( x[:200] for x in [k + ' = %r' % self.F(k) for k in sorted(self.f)] )

# *** *** ***

config = DC()
config.NotCachingReactForms = '[fm_svg][schedule][react_py]'
CLS = {}

# *** *** ***

def now(dlm = '.'):
    if dlm == '.':
        return datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    else:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# *** *** ***

def today(dlm = '.'):
    if dlm == '.':
        return datetime.today().strftime('%d.%m.%Y')
    else:
        return datetime.today().strftime('%Y-%m-%d')

# *** *** ***
def stackEx():
    return traceback.format_exc()

def httpError(ret='None'):
    """
    Декоратор, пищуий в журнал ошибки.
    """
    def _wrapper1(func):
        def _wrapper2(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                err(ex, cat=func.__name__)
                err(stackEx())
                if ret:
                    return ret, 'text/html; charset=UTF-8', '%s:%s' % (func.__name__, ex)
        return _wrapper2
    return _wrapper1

# *** *** ***

def well(*keys):
    cls = CLS
    for k in keys[:-1]:
        cls = cls.get(k)
        if not cls:
            return ''
    return cls.get(keys[-1], '')

def toWell(d, *keys):
    from .. dbToolkit.Document import Document

    cls = CLS
    for k in keys[:-1]:
        CLS[k] = cls.get(k, {})
        cls = CLS[k]

    cls[keys[-1]] = DC(d) if type(d) is Document else d
    
def appendWell(x, *keys):
    cls = CLS
    for k in keys[:-1]:
        CLS[k] = cls.get(k, {})
        cls = CLS[k]
    if not cls.get(keys[-1]):
        cls[keys[-1]] = []
    cls[keys[-1]].append(x)

# *** *** ***

def files(fn, key):
    fn = fn.lower()
    ff = (well('files') or {}).get(fn)

    return   ff.get(key, '')     if ff \
        else well('scripts', fn) if key == 'buf' \
        else well('verJS', fn)   if key == 'ver' \
        else ''
        
# *** *** ***

def liform(f, k):
    fo = well('otherForms').get(f.lower())
    return fo.F(k) if fo else ''

# *** *** ***

def chModOwn (f, mode=0o777):
    try:
        os.chmod( f, mode )
        shutil.chown( f, 'nobody', 'nogroup' )
    except:
        pass

# *** *** ***

def tryDecode(s):
    for x in ['utf-8', 'cp1251', 'cp437']:
        try:
            return s.decode(x), x
        except:
            pass
                
    return None, None

# *** *** ***

def tableName(dbAlias):
    return dbAlias.replace('.', '_').replace('/', '_')

# *** *** ***

def cursorExecute(cur, sql):
    tryNum = 0
    while 1:
        try:
            r = cur.execute(sql)
            return r
        except Exception as ex:
            s = str(ex).lower()
            dbIsLocked = ('database is locked' in s or 'deadlock' in s)
            if dbIsLocked and tryNum < 5:
                time.sleep(0.1)
                tryNum += 1
            else:
                if dbIsLocked and tryNum:
                    err(ex, cat = 'cursorExecute')
                raise

# *** *** ***

def xunid(s):
    return str(hexlify(s), 'ascii')

reHex = re.compile('(?:[0-9a-fA-F][0-9a-fA-F])+$')
def isHex(s):
    try:
        return not not reHex.match(s)
    except:
        return False

def profile(dbAlias):
    return CLS['profile'].get(dbAlias, '')

# *** *** ***

js_search = re.compile(r'((<script[\s]+src[\s]*)|(<link[\s]+rel[\s]*))=[\s]*[\'"][\s\S]+?(\.css"|\.js")', re.IGNORECASE | re.M | re.U)

def setVersionJS(bf):
    """
bf = 
...
<script src="jsv?lb.js"></script>
<link rel="stylesheet" href="jsv?std3d.css"/>

returned:
...
[
<script src="jsv?lb.js::2013-09-02 09:57:24"></script>
<link rel="stylesheet" href="jsv?std3d.css::2013-08-29 13:16:28"/>
, ver
]
    """
    
    itr = js_search.finditer(bf)
    l0 = 0
    bf2 = ''
    ver = ''
    for match in itr:
        s = match.group()
        if 'jsv?' in s:
            s = s[:-1]
            fn = well('path') + s.split('jsv?')[1].lower()
            if fn.endswith('.js') or fn.endswith('.css'):
                try:
                    stat = os.stat(fn)
                    v = datetime.fromtimestamp(stat.st_mtime).strftime('%d.%m.%Y-%H:%M:%S')
                    s += '::' + v
                    ver = max(ver, v)
                except:
                    s = s.replace('jsv?', 'js?')
            else:
                s = s.replace('jsv?', 'js?')

            s += '"'

        l1,l2 = match.span()
        bf2 += bf[l0:l1] + s
        l0 = l2
        
    return bf2 + bf[l0:], ver

# *** *** ***

# from django 

user_regex = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*$"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"$)', # quoted-string
    re.IGNORECASE)
domain_regex = re.compile(
    r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,})\.?$'  # domain
    # literal form, ipv4 address (SMTP 4.1.3)
    r'|^\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$',
    re.IGNORECASE)

def emailValidator(email):
    s = email.replace('\r', '').replace(',', '\n').replace(';', '\n')
    ls = [x.strip() for x in s.split('\n') if x.strip()]
    if not ls:
        return

    for s in ls:
        ss = s.rpartition('>')[2].rpartition(' ')[2]

        if not ss or '@' not in ss:
            return

        user_part, domain_part = ss.rsplit('@', 1)

        if not user_regex.match(user_part):
            return

        if domain_regex.match(domain_part):
            continue
        
        # Try for possible IDN domain-part
        try:
            if domain_regex.match(domain_part.encode('idna').decode('ascii')):
                continue
            else:
                return
        except:
            return

    return True

# *** *** ***

def setLevel(inh, d):
    def incAA(s): # увеличивает заданный в s o_level
        if len(s) < 3 or not('.aa' <= s < '.zz'):
            return '.aa'
        
        if ord(s[2]) < ord('z'):
            return '.' + s[1] + chr(ord(s[2]) + 1)
        else:
            return '.' + chr(ord(s[1]) + 1) + 'a'
    
    # *** *** ***
    
    dic = {}
    first = d.form[0].lower()

    for r in d.db.getResponses(d.ref):
        if r.form.split('.')[0] == d.form and r.o_level and r.dir != 'd':
            dic[r.o_level] = r

    if not dic:
        return first + '.aa'

    sk = sorted(dic.keys())
    
    if not (inh.ref and inh.o_level):
        return first + incAA(sk[-1][1:])
    
    io_level = inh.o_level
    lol = len(io_level)
    
    for i in range(len(sk)):
        if io_level == dic[sk[i]].o_level[:lol]: # ищем свою ветку
            
            while i < len(sk):
                if io_level != dic[sk[i]].o_level[:lol]: # своя ветка кончилась ?
                    if io_level == dic[sk[i-1]].F('o_level'):
                        return io_level + '.aa'
                    return io_level + incAA(sk[i-1][lol:])
                
                i += 1
                
            if io_level == dic[sk[i-1]].o_level:
                return io_level + '.aa'
            return io_level + incAA(sk[i-1][lol:])

    return first + incAA(sk[-1][1:])

# *** *** ***

def accessDenied(userName='-?-'):
    return 403, 'text/html; charset=UTF-8', f'Access denied for {userName}'

# *** *** ***

lockSno = {}

def snoDB(db):
    unid = '0005'*8
    
    if db.alias not in lockSno:
        lockSno[db.alias] = threading.Lock()
    
    for n in range(50):
        if lockSno[db.alias].acquire(False):
            try:
                d = db.getDocumentByUNID(unid)
                if not d:
                    d = db.createDoc()
                    d.unid = unid
                try:
                    n = int(d._DOCNO, 10)
                except:
                    n = 0
                num = str(n + 1)
                d._DOCNO = num
                d.save(True, False)
            except Exception as ex:
                err(ex, cat='Регистрация')
            lockSno[db.alias].release()
            snd(f'{db.userName} зарегистрировал номер {num} в {db.alias}', cat='Регистрация')
            return num
        
        time.sleep(0.05)
            
    lockSno[db.alias].release() # разблокировать полюбому
    return ''
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    