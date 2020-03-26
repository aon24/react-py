# -*- coding: utf-8 -*- 
"""
AON 19 mar 2018

"""

from .. util.common import *
from .. util.first import snd, err, dbg
from .. util.checkRights import *
from .. dbToolkit.Document import Document
from .. dbToolkit.Book import getDocByUnid, getDB

from .forms.fm_svg.svgTools import insertSvgItem
from .classForm import getFormObj

from mimetypes import guess_type
import json

# *** *** ***

def badReq(par, userName=None):
    dbg('param: %s' % par, cat='badReq')
    return homePage(par, userName)
    return accessDenied(userName)

def notFound(s):
    snd(s, cat='page not found')
    return 404, None, f'{s} not found'

# *** *** ***

def doGet(fn, param, userName):
    dbg(f'fn: {fn} param: {param}, userName: {userName}', cat='doGet')
    
    if fn.endswith('.html'):
        try:
            with open('html/' + fn.replace('..', 'xx').replace('//', 'xx'), 'rb') as f:
                snd(f'{fn} {userName}', cat='get file')
                return 200, None, tryDecode(f.read())[0]
        except:
            return notFound(fn)
            
    handler = _keyList.get(fn, badReq)
    return handler(param, userName)

# *** *** ***

# *** *** ***

def getImage(par, un=None):
    try:
        with open(well('path') + 'images/' + par.replace('..', 'xx').replace('//', 'xx'), 'rb') as f:
            return 200, guess_type(par)[0], f.read()
    except:
        return notFound(par)

# *** *** ***

def getScript(par, un=None):
    pr = well('path') + par.partition('::')[0].strip().replace('..', 'xx').replace('//', 'xx')
    ext = pr.rpartition('.')[2].lower()
    
    if ext in ['js', 'css', 'html']:
        try:
            mimeType = guess_type('x.'+ext, False)[0] + '; charset=UTF-8'
            with open(pr, 'rb') as f:
                return 200, mimeType, f.read()
        except Exception as ex:
            err(f'getScript: {ex}', cat='do_get.py')

    return notFound(pr)

# *** *** ***

@httpError(501)
def homePage(smartPhone, userName):
    mode = 'edit' if mainAdmin(userName) else 'read'

    db = getDB(well('MAIN', 'BOOK'), userName)
    if not db:
        return notFound( well('MAIN', 'BOOK') )
    
    d = db.getDocumentByUNID('1111'*8)
    if not d:
        d = Document(db)
        d.unid = '1111'*8
    else:
        mode = 'read'
    d.form = 'home'
    
    return openForm(d, mode, None, smartPhone)

# *** *** ***

@httpError(501)
def newDoc(par, userName):
    dbAlias, form, dbaGr, unidGr, smartPhone = (par.split('&') + [None, None, None, None])[:5]
    if not dbAlias:
        return openForm(DC({'FORM': form}), 'new', None, smartPhone)
    
    if notReader(dbAlias, userName):      #  д.б. notCreator(dbAlias, userName)
        return accessDenied(userName)
    
    db = getDB(dbAlias or dbaGr, userName)
    if db:
        d = db.createDoc()
        d.FORM = form
        if not unidGr:
            return openForm(d, 'new', None, smartPhone)
        
        ground = getDocByUnid(unidGr, dbaGr, userName)
        if ground:
            return openForm(d, 'newSd', ground, smartPhone)
        
    return badReq(par, userName)

# *** *** ***

def apiDoGet(param, userName):
    """
    param - dbAlias и параметры, разделенные '&'
    0-й параметр - всегда имя функции.
    1-й параметр как правило dbAlias.
    В конце строки справа от :: дата-время версии ИЛИ контр. сумма ИЛИ нет.
    Пример: 'loadForm&outlet.gru::804597279', 'user/SOVA'
    """
    # *** *** ***

    fn, _, par = param.partition('&')

    dbg(f'param: {param}, userName: {userName}', cat='apiDoGet')

    right, handler = _apiGetList.get(fn, (isReader, badReq))
    
    if not right or right(par.partition('&')[0], userName): # проверка прав доступа
        return handler(par, userName)
    else:
        return accessDenied(userName)

# *** *** ***

@httpError(501)
def loadReadyList(par, userName):
    return 200, 'application/x-javascript; charset=UTF-8', well('readyLists', par.partition('::')[0])

# *** *** ***

@httpError(501)
def loadDropList(par, userName):
    listName = par.partition('::')[0]
    if '|' in listName:
        ls = well(*listName.split('|')[:2])
    else:
        ls = well('classifier', listName)
        if not ls:
            ls = well(listName)
            if type(ls) is dict:
                ls = list(ls.keys())
    if ls:
        ls = json.dumps(ls, ensure_ascii=False)

    return 200, 'application/json', ls or '[]'

# *** *** ***

def loadForm(formAndCRC, userName):
    return 200, 'application/json', well('form-json', formAndCRC) or '"{}"' # при перезагрузки форма может исчезнуть

# *** *** ***

@httpError(501)
def loadDoc(par, userName):
    '''
    вызывется из xhr для показа в pageFrame
    '''
    dbAlias, unid, mode, smartPhone = (par.split('&') + [None, None])[:4]
    mode, _, multiPage  = mode.partition('|')
    d = getDocByUnid(unid, dbAlias, userName)
    
    if d:
        obf = getFormObj(d.form, smartPhone)
        dl = obf.qOpen(d, mode, None)
        if dl and type(dl) is Document:              # qOpen может изменить документ
            d = dl
            obf = getFormObj(d.form, smartPhone)
            obf.qOpen(d, mode, None)
            
        dic = setDocProps(d, mode, obf, multiPage)
        
    else:
        dic = dict(
                data = {'FORM':'default', 'ERROR': f'Документ не найден (docopen?{dbAlias}&{unid})'},
                rsMode = 'read',
                dbAlias = dbAlias,
                unid = unid,
            )
    return 200, 'application/json', json.dumps(dic, ensure_ascii=False).replace('\u2028', ' ').replace('\u2029', ' ')


# *** *** ***

@httpError(501)
def newForm(par, userName):
    '''
    открывает форму без документа. Нужна при разработки новых форм
    '''
    dbAlias, form, mode, smartPhone = (par.split('&') + [None, None])[:4]
    mode = mode or 'read'
    mode, _, multiPage  = mode.partition('|')
    dbg(par, cat='newForm')
    
    obf = getFormObj(form, smartPhone)
    d = getDB(dbAlias, userName).createDoc()
    dl = obf.qOpen(d, mode, None)
    if dl and type(dl) is Document:              # qOpen может изменить документ
        d = dl
        obf = getFormObj(d.form, smartPhone)
        obf.qOpen(d, mode, None)
        dic = setDocProps(d, mode, obf, multiPage)
    else:
        data = { x:d.f[x] for x in d.f if 'PASSW' not in x and d.f[x] }
        data['FORM'] = form
        dic = dict(
                data = data,
                rsMode = mode,
                dbAlias = dbAlias,
                unid = 'unid',
                urlForm = obf.getUrl(dbAlias, mode, userName, multiPage),
                multiPage = multiPage,
                smartPhone = smartPhone,
                cssJsUrl = obf.cssUrl(mode) + obf.jsUrl(mode),
            )
        dbg(dic, cat='newForm')
    return 200, 'application/json', json.dumps(dic, ensure_ascii=False).replace('\u2028', ' ').replace('\u2029', ' ')


# *** *** ***

@httpError(501)
def loadView(par, userName):
    '''
    
    '''
    s = ''
    try:
        dbAlias, fieldName, viewClass, offset, limit, filtered = par.split('&')[:6]
        s = viewClass + '-' + fieldName + '-' + dbAlias
        view = well('viewClass', s)
        if view:
            return view.loadView(dbAlias, offset, limit, filtered, userName)
        else:
            err('invalid view:' + s, cat='do_get.py.loadView')
            return 511, None, 'loadView-error'

    except Exception as ex:
        err('%s\n%s\npar:%s' % (ex, s, par), cat='do_get.py.loadView')
        return 512, None, 'loadView-error: %s\npar:%s' % (s, par)

# *** *** ***

def setDocProps(d, mode, obf, multiPage=''):
    '''
    вызывется из loadDoc(xhr-loadDoc => api.loadDoc() ) или из вида(get-docopen => SrvTools.docOpen() => api.openDoc() )
    '''
    if d.db:
        dbAlias = d.db.alias
        userName = d.db.userName
    else:
        dbAlias = ''
        userName = ''
        
    return dict(
        rsMode = 'edit' if mode in ['new', 'newSd'] else mode,
        dbAlias = dbAlias,
        unid = d.unid,
        printList = obf.printList(d),
        data = { x:d.f[x] for x in d.f if 'PASSW' not in x and d.f[x] },
        urlForm = obf.getUrl(dbAlias, mode, userName, multiPage),
        multiPage = multiPage,
        userName = userName,
        cssJsUrl = obf.cssUrl(mode) + obf.jsUrl(mode),
    )
    
# *** *** ***

def openForm(d, mode, ground=None, smartPhone=None):
    '''
    вызывется из вида при открытии документа по команде docOpen или при создании документа по команде newDoc
    '''
    obf = getFormObj(d.form, smartPhone)

    dl = obf.qOpen(d, mode, ground) # qOpen может изменить документ
    if dl and type(dl) is Document:
        d = dl
        obf = getFormObj(d.form, smartPhone)
        obf.qOpen(d, mode, ground)

    dic = setDocProps(d, mode, obf)
    s = json.dumps(dic, ensure_ascii=False).replace('<s','<"+"s').replace('</s','</"+"s').replace('<S','<"+"S').replace('</S','</"+"S').replace('\u2028', ' ').replace('\u2029', ' ')
    
    if d.form.lower().startswith('rk') and d.docNo:
        title = d.pref + d.docNo + d.suff + ' ' + d.D('docDa')
    else:
        title = obf.title or 'Документ'

    html = liform('index', 'html') % title

    script = f'<script>window.jsDoc={s};</script>'
    if obf.cssInline:
        script = f'<style>{obf.cssInline}</style>\n{script}'
    
    html = html.replace('</head>', f'{script}\n</head>', 1)
    html = setVersionJS(html)[0]

    return 200, 'text/html; charset=UTF-8', html 
 
# *** *** ***

def docOpen(param, un): # param: dbAlias & unid & mode & withForm & titleForEasyPrintForm
    if '&' not in param:
        return badReq(param)
    
    if param.startswith('download/'):
        fn = param.split('?')[0].split('download/')[1]
        return 200, None, liform('download', 'html') % (fn, param)
    else:
        ls = param.split('&')
        if len(ls) < 3:
            mode = 'read'
            smartPhone = None
        else:
            mode, _, smartPhone = ls[2].partition('|')
            mode = mode or 'read'

    if mode not in ['read', 'readOnly', 'edit', 'info', 'zoom', 'print', 'download', 'summary']:
        return badReq(param)
    
    dbAlias, unid = ls[:2]
    
    if notReader(dbAlias, un):
        return accessDenied(un)

    d = getDocByUnid(unid, dbAlias, un)
    if not d:
        return badReq(param)
    
    if (d.autoOpenBlob and mode != 'info') or mode == 'download':
        return openDownload(d, mode, param)
    
    if mode == 'edit' and ( d.readOnly or notEditor(dbAlias, un) ):
        mode = 'read'
    
#     if len(ls) == 5:
#         d.form = ls[3]
#         tuningPrint(d)
#         return forms.openEasyForm(d, ls[4])
    
    if mode == 'info':
        d.formBeforeOpening = d.form
        if notAdmin(dbAlias, un):
            d.form = 'default'
            mode = 'read'
        else:
            d.form = 'info'
            mode = 'edit'
        return openForm(d, mode, None, smartPhone)
    
#     if mode == 'print':
#         forPr = liform(d.form.lower(), 'forPrint')
#         if forPr:
#             d.form = (forPr.split('¤')[0]).split('|')[-1]
#             if '&' in d.form:
#                 d.form, x, title = d.form.partition('&')
#                 tuningPrint(d)
#                 return forms.openEasyForm(d, title)
#             
#             return forms.openForm(d, 'read')
#         else:
#             return 200, 'text/html; charset=UTF-8', 'Для выделенного документа форма для печати не предусмотрена'
    
    if len(ls) == 4:
        d.formBeforeOpening = d.form
        d.form = ls[3]
        
    return openForm(d, mode, None, smartPhone)

# *** *** ***

def openDownload(d, mode, param):
    html = liform('rreport', 'html')
    fnam = d.attFields()
    if fnam:
        try:
            fsName, fzip, fn, ctype, flen, tm = d.F(fnam[0]).split('|')
            idbl = fnam[0].partition('_')[2]
            downloadUrl = '/download/' + fn + '?' + '&'.join([d.db.alias, d.unid, idbl, fsName, fzip, ctype, flen])
            excel = f'/download/{fn}.xls?' + '&'.join([d.db.alias, d.unid, idbl, fsName, fzip, 'application/x-excel', flen])
            word = f'/download/{fn}.doc?' + '&'.join([d.db.alias, d.unid, idbl, fsName, fzip, 'application/msword', flen])
            html = html.replace('src=""', f'src="{downloadUrl}"').replace('openExcel', excel).replace('openWord', word)
        except Exception as ex:
            html = html.replace('src=""', f'srcdoc="{ex}"')
    else:
        html = html.replace('src=""', 'srcdoc="Отсутствует вложение"')
    return 200, None, html

# *** *** ***

_contentCount = 0
def content(par, un):
    global _contentCount
    _contentCount += 1 
    snd(f'contentCount: {_contentCount}', cat='content')
    return 200, None, liform('content', 'html') % well('content')

# *** *** ***

def topic(par, un):
    return 200, None, well('topic', par)
# *** *** ***

def getLogData(par, un):
    lg, _, cat = par.partition('|')
    msg = well('logger_' + lg, cat)
    return 200, None, '\n'.join(reversed(msg))
    
# *** *** ***
 
_keyList = {
    'topic': topic,
    'content': content,
    'image': getImage,
    'newdoc': newDoc,
    'js': getScript, # не кэшируем
    'jsv': getScript,
    'api.get': apiDoGet,
    'api.getc': apiDoGet,
    'home': homePage,
    'docopen': docOpen,
    'list':  loadDropList,
    'readyList':  loadReadyList,
}

_apiGetList = {
    'loadForm': (None, loadForm),
    'loadDoc':  (isReader, loadDoc),
    'loadDropList':  (None, loadDropList),
    'loadView': (isReader, loadView),
    'getLogData': (None, getLogData),
    'newForm': (isAdmin, newForm),
    'insertSvgItem': (isReader, insertSvgItem),
}

# *** *** ***
