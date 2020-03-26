# -*- coding: utf-8 -*- 
"""
AON 20 apr 2018

"""

from .. util.common import well, httpError, emailValidator, accessDenied
from .. util.first import snd, err
from .. util.checkRights import notEditor, notCreator
from .. dbToolkit.Book import getDB
from .classForm import getFormObj

import json

# *** *** ***

@httpError(501)
def saveDoc(query, rData, userName):
    cat = 'do_post.py.saveDoc'
    dbAlias, force, smartPhone = (query.split('&') + [None, None])[:3]

    try:
        oldF = {}
        newF = {}
        jsonO = json.loads(rData)
        for k in jsonO:
            oldF[k], newF[k] = jsonO[k]
            
    except Exception as ex:
        err(f'Exception by save: json.loads() - error: \n{ex}\n{rData}', cat=cat)
        return 400, None, f'DocSave error: json.loads() - exception:\n{ex}'
        
    db = getDB(dbAlias, userName)
    d = db.getDocumentByUNID(newF['UNID'])
    if d:
        if notEditor(dbAlias, userName):
            snd('Not editor %r' % userName, cat=cat)
            return accessDenied(userName)
    else:
        if notCreator(dbAlias, userName):
            snd('Not creator %r' % userName, cat=cat)
            return accessDenied(userName)
    
    dic = {}
    if 'REF' in newF:
        coll = db.getResponses(newF['REF'])
        for r in coll:
            dic[r.unid] = r
    
        if d:
            dic[d.unid] = d     # если d был удален другим оператором, его не будет в подчиненных 

    if 'EMAIL' in newF and not force and not emailValidator(newF['EMAIL']):
        return 449, None, 'В поле E_MAIL недействительный эл. адрес:\n\n' + newF['EMAIL']

    if d:
        existF = d.f.copy()
        
        if force:
            if d.ERASER:
                newF['ERASER'] = ''
                if d.OLDDIR:
                    newF['DIR'] = d.OLDDIR
                    newF['OLDDIR'] = ''
                if d.DELETEDREF:
                    newF['REF'] = d.DELETEDREF
                    newF['DELETEDREF'] = ''
        else:
            if d.ERASER:
                s = '\nДокумент был удален.\nУдалил: %s\n\nОтменить удаление и сохранить?' % d.ERASER
                err(s, cat=cat)
                return 409, None, s
            
            for k in oldF:
                if oldF[k] != d.F(k) \
                    and newF[k] != d.F(k) \
                    and oldF[k].replace('\r', '') != d.F(k).replace('\r', '').replace('\n', '¤').replace('\u2028', ' ').replace('\u2029', ' '):
                        s = 'ИМЯ ПОЛЯ: %s\n\nНОВОЕ ЗНАЧЕНИЕ:\n"%s"\n\nСТАРОЕ ЗНАЧЕНИЕ:\n"%s"\n\nКОНФЛИКТНОЕ ЗНАЧЕНИЕ:\n"%s"' % \
                            ( k, newF[k], oldF[k], d.F(k).replace('\r', '').replace('\n', '¤') )
                        err(s, cat=cat)
                        return 409, None, s
    else:
        d = db.createDoc()
        existF = None
    
    d.f.update(newF)
    
    obf = getFormObj(d.form, smartPhone)
    
    if not obf.qSave(d, dic):
        err('obf.qSave', cat=cat)
        return 400, None, 'BeforeSave error'

    if d.noSave or d.save(True, existF):
        return 200, None, 'OK'
    
    err('doc-save Error', cat=cat)
    return 400, None, 'doc.save() Error'

# *** *** ***
