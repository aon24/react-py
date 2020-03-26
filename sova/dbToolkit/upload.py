from .. util.common import now
from .. util.first import err

from .. util.checkRights import notEditor
from .Book import getDB

import zlib, uuid, os

_noCompress = 'compressed|.jpg|.jpeg|.gif|.pdf|.png|.arj|octet-stream|.zip|.rar|.7z|.dll|.exe|.avi|.mkv|.mp3|.mp4'.split('|')

# *** *** ***

def uploadFile(query, userName, buf):
    def _err(s):
        err(s, cat='error-upload.py')
        return 400, None, s

    try:
        dbAlias, slen, tm, unid = query.split('&')
        flen = int(slen, 10)

        if notEditor(dbAlias, userName):
            return _err('uploadFile: Access denied for user %s' % userName)

        db = getDB(dbAlias, userName)
        if not db:
            return _err('uploadFile: Can not get database %s' % dbAlias)

        tm = '%s_%s' % (now('-'), tm)
        path = db.fileStores[0].path.replace('\\', '/')
        path += ('' if path.endswith('/') else '/') + tm.split()[0]

        brCount = i = 0
        while brCount < 2:
            if buf[i] == 10:   # LF \n
                brCount += 1
            elif buf[i] != 13: # CR \r
                brCount = 0
            i += 1
            if i > 1000:
                return _err('invalid rfile-header')

        rfileHeader = buf[:i].decode().lower()

        if any(c in rfileHeader for c in _noCompress) or flen > 10000000:
            bf = buf[i:i+flen]
            fzip = '0'
        else:
            bf = zlib.compress(buf[i:i+flen])
            fzip = 'Z'

        os.makedirs(path, exist_ok=True)

        idbl = uuid.uuid4().hex.upper()
        with open(path + '/' + unid + '_' + idbl, 'bw') as f:
            f.write(bf)

        return 200, 'text/plain; charset=UTF-8', '&'.join([idbl, db.fileStores[0].name, tm, fzip])

    except Exception as ex:
        return _err('Exception: %s' % ex)

# *** *** ***
