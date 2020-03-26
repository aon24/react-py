# -*- coding: utf-8 -*-
import os, sys
pat = dict(globals()).get('__file__', '').partition('sovaApp.py')[0]

if pat:
    os.chdir(pat)
    sys.path.append(pat)

from sova.util.first import err, initLog
initLog(mainProcess=True, prpr=True)

from sova.util.common import toWell
from sova.util.username import getUserName, addSessionID
from sova.api.do_get import doGet, notFound
from sova.api.do_post import saveDoc
from sova.dbToolkit.upload import uploadFile
from sova.dbToolkit.download import downloadFile

import traceback
import email.utils
import urllib.parse
import time
import uuid
from hashlib import md5
import gzip

# *** *** ***

def application(environ, start_response):
    method = environ.get('REQUEST_METHOD', '')
    path = environ.get('PATH_INFO', '')[1:100]
    query = urllib.parse.unquote(environ.get('QUERY_STRING', '')[:10000])
    def do_Get():
        
        if environ.get('HTTP_HOST', '').partition('.')[0] == 'content':
            if not path:
                return doGet('content', '', '')
            elif path == 'topic':
                return doGet(path, query, '')
            
        if path == 'logoff':
            toWell('', 'fmArr') # убрать потом
            getUserName(environ, logoff=True)
            return homePage()
        if path == 'favicon.ico':
            return doGet('image', 'favicon.ico', '')
        if not query:
            return homePage(path)
        if path in ['image', 'js', 'jsv']:
            return doGet(path, query, '')

        userName = getUserName(environ)
        if not userName:
            return 401, # login
        userName += '::' + environ['REMOTE_ADDR']
        
        if path.startswith('download'):
            return downloadFile(query, userName)
        return doGet(path, query, userName)

    # *** *** ***

    def do_Post():
        userName = getUserName(environ)
        if not userName:
            return 401, # login
        userName += '::' + environ['REMOTE_ADDR']

        ln = int(environ.get('CONTENT_LENGTH', -1))
        buf = environ['wsgi.input'].read(ln)

        if path == 'upload':
            return uploadFile(query, userName, buf)

        if path == 'saveDoc':
            return saveDoc(query, buf.decode(), userName)

        return 501, None, 'Invalid request'

    # *** *** ***

    def http_err(ex):
        s = '500. Internal server error. Method: %s, path: %s, query: %s' % (method, path, query)
        s += '\n%r\n%r' % (ex, traceback.format_exc())
        err(s.replace('\\n', '\n'), cat='err-app-Exception')
        return 500, None, s.replace('\\n', '<br>')

    # *** *** ***

    def makeResponse(status, contentType=None, body=b''):
        header = []
        contentType = contentType or 'text/html; charset=UTF-8'

        if len(body) > 100 and any(c in contentType for c in ['/json', '/html', '/javascript', '/css']):
            try:
                body = gzip.compress( body.encode() if type(body) is str else body )
                header.append( ('Content-Encoding', 'gzip') )
            except Exception as ex:
                err(f'{contentType}, {status}, {ex}', cat='makeResponse')
                return

        if status == 401: # login
            sovaSystem = 'sova.online'
            sid = uuid.uuid4().hex.upper()
            addSessionID(sid, newSid={'tm': time.time()})
            header = []
            rsOpaque = md5(sovaSystem.encode()).hexdigest()

            s = 'Digest realm="%s", qop="auth", nonce="%s", opaque="%s"' % (sovaSystem, uuid.uuid4().hex, rsOpaque)
            body = '''<h2 align="center">Введите логин и пароль для доступа к системе <input type="button" value="Войти" onclick="window.location.href='/'"/></h2> '''.encode()
            header.append( ('WWW-Authenticate', s ) )
            header.append( ('content-type','text/html; charset=UTF-8' ) )
            header.append( ('Set-Cookie', 'sovasid=%s; Max-Age=%d; HttpOnly' % (sid, 60*60*24) ) )
            header.append( ('Content-length', str(len(body)) ) )
        
            return '401 Unauthorized', header, body
                    
        if not type(status) is int:
            status = f"500 Internal Server Error({method}). path:{path}, query:{query}, Error: {status or '-?-'}"
            body = b''
            
        if method == 'GET' and path in ['image', 'jsv', 'list', 'api.getc']:
            days = 15 if path == 'list' else 30

            maxAge = 60*60*24*days
            header.append( ('Expires', email.utils.formatdate( time.time() + maxAge, usegmt=True )) )
            header.append( ('Cache-Control', 'max-age=%d' % maxAge) )
        
        if type(body) is str:
            try:
                if status > 401:
                    try:
                        body.encode('latin-1', 'strict') # иначе ValueError: unicode object contains non latin-1 characters
                        status = f'{status} {body}'
                        body = b''
                    except:
                        body = body.encode()
                else:
                    body = body.encode()
            except:
                status = '500 sovaApp.py.makeResponse: encode-error'
                contentType = 'text/html; charset=UTF-8'
                body = b''

        lbody = len(body)
        if environ.get('HTTP_RANGE') and status == 200:
            status = '206 OK'
            header.append( ('Content-Range', 'bytes 0-%d/%d' % (lbody-1, lbody)) )

        header.append( ('content-type', contentType) )
        header.append( ('Content-length', str(lbody)) )
        
        return status if type(status) is str else (str(status) + ' OK'), header, body

    # *** *** ***
    # *** *** ***
    # *** *** ***

    try:
        if method == 'GET':
            status, header, body = makeResponse(*do_Get())
        elif method == 'POST':
            status, header, body = makeResponse(*do_Post())
        else:
            status, header, body = makeResponse('405 Allow: GET, POST')
    except Exception as ex:
        status, header, body = makeResponse(*http_err(ex))
    
    start_response(status, header)
    
    return body,

# *** *** ***

def homePage(page=''):
    try:
        p = page or 'arm'
        if '.' not in page:
            p += '.html'
        with open(f"./home/{p}", 'rb') as f:
            return 200, None, f.read()
    except:
        return 200, None, f'<h3>404<br>Page "{p}" not found</h3>'

# *** *** ***

from sova import profiles

# *** *** ***
