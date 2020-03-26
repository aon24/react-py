# -*- coding: utf-8 -*-

'''
Created on 17 авг. 2018 г.

@author: aon24
'''
from .common import well
from .first import snd

import re, time, threading
from hashlib import md5
import urllib.parse

sessionID = {}

reRealm = re.compile(r'realm="(.+?)"')
reUsername = re.compile(r'username="(.+?)"')
reNonce = re.compile(r'nonce="(.+?)"')
reCnonce = re.compile(r'cnonce="(.+?)"')
reUri = re.compile(r'uri="(.+?)"')
reOpaque = re.compile(r'opaque="(.+?)"')
reNc = re.compile(r'nc=(.+?),')
reResponse = re.compile(r'response="(.+?)"')

# *** *** ***

def getUserName(env, logoff=None):
    addr = env.get('REMOTE_ADDR', 'local')

    return 'Designer/SOVA'
    
    aut = env.get('HTTP_AUTHORIZATION')
    if aut:
        sid = env.get('HTTP_COOKIE', '').partition('sovasid=')[2][:32]
        if sid in sessionID:
            uname = checkPassword(aut, env.get('REQUEST_METHOD', ''))
            if uname:
                if logoff:
                    addSessionID(sid, newSid=None)
                else:
                    sessionID[sid]['tm'] = time.time()
                    if 'un' not in sessionID[sid]:
                        sessionID[sid]['un'] = uname
                        snd('%s:%s %s %s' % (uname, addr, env.get('PATH_INFO', '-?-')[1:100], urllib.parse.unquote(env.get('QUERY_STRING', '-?-')[:100])), cat = 'login')
                    return uname

# *** *** ***

def checkPassword(aut, method):
    m = reUsername.search(aut)
    if not m:
        return
    
    log_in = m.group(1)

    user = well('login', log_in)
    if not user:
        return

    m = reNonce.search(aut)
    nonce = (m and m.group(1)) or ''
    
    m = reCnonce.search(aut)
    cnonce = m.group(1) if m else ''

    m = reUri.search(aut)
    uri = m.group(1) if m else ''
    
    m = reNc.search(aut)
    nc = m.group(1) if m else ''
    
    m = reResponse.search(aut)
    response = m.group(1) if m else ''

    a2 = md5((method + ':' + uri).encode()).hexdigest()
    s = user.password + ':' + nonce + ':' + nc + ':' + cnonce + ':auth:'
    if md5( (s+a2).encode() ).hexdigest() == response:
        return '%s/%s' % (user.userName, user.DNAME)

    a2 = md5((method + ':' + uri.replace('\\\\', '\\')).encode()).hexdigest() # sucking chrome
    if md5( (s+a2).encode() ).hexdigest() == response:
        return '%s/%s' % (user.userName, user.DNAME)

# *** *** ***

lockSessID = threading.Lock()

# *** *** ***

def addSessionID(sid, newSid=None):
    for i in range(1, 100):
        if lockSessID.acquire(False):
            if newSid and sid not in sessionID:
                sessionID[sid] = newSid # login
                
            for k in list(sessionID):
                if k == sid:
                    if not newSid:
                        snd(f"{sessionID[k].get('un', '-?-')}, {time.time()-sessionID[k]['tm']:8.5}", cat='logoff')
                        del sessionID[k] # logoff
                else:
                    if 'un' in sessionID[k]:
                        if time.time() - sessionID[k]['tm'] > 3600*12:    # clearSession
                            del sessionID[k]
                    else:
                        if time.time() - sessionID[k]['tm'] > 300:
                            del sessionID[k]
            lockSessID.release()
            return
        else:
            time.sleep(0.05)

# *** *** ***
