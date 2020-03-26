from .. util.first import err, snd
from .. util.checkRights import notReader
from .Book import getDocByUnid

import zlib

# *** *** ***

def downloadFile(par, un):
    def _err(s):
        err(s, cat='error-download.py')
        return 400, None, s

    snd('%s [%s]' % (par, un), cat='downloadFile')
    try:
        ls = par.split('&')
        dbAlias, unid, idbl, fileStoreName, fzip, mimetype = ls[:6]
        if 'charset' not in mimetype and len(ls) > 7:
            mimetype += '; charset=' + ls[7]

        if notReader(dbAlias, un):
            return _err('Access denied for user %s' % un)

        d = getDocByUnid(unid, dbAlias)
        if not d:
            return _err('Can not get document: %s&%s' % (dbAlias, unid))

        path = None
        for fs in d.db.fileStores:
            if fs.name.lower() == fileStoreName.lower():
                path = fs.path
                break
        if not path:
            return _err('Can not find filestore "%s"' % fileStoreName)

        tm = None
        for k in d.f:
            if k.startswith('FILES') and k.endswith(idbl):
                tm = d.f[k].split('|')[5].split()[0]
                break
        if not tm:
            return _err('Invalid file-id: "%s"' % idbl)

        path = path.replace('\\', '/')
        path += ('' if path.endswith('/') else '/') + tm

        fullname = path + '/%s_%s' % (d.ref or d.unid, idbl)
        with open(fullname, 'rb') as f:
            buf = f.read()

        if not buf:
            return _err('Zero-length file')

        if fzip[0] == 'Z':
            buf = zlib.decompress(buf)

        return 200, mimetype or 'Application/attachment', buf

    except Exception as ex:
        return _err('Exception(par=%s): %s' % (par, ex))

# *** *** ***
