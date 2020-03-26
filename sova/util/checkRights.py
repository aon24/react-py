# -*- coding: utf-8 -*- 
"""
AON 19 mar 2019

"""
from . common import well
from . first import snd

# *** *** ***

def mainAdmin(userName):
    return userName in ['Designer/SOVA']
    
# *** *** ***

def checkRights(dbAlias, userName, right, form=None):
    un = userName.partition('::')[0]
    if mainAdmin(un):
        return True
    
    acr = well('acr', dbAlias)
    if acr:
        if form and isRole(acr, un, 'no.' + form):
            return
        
        if 'default' in acr and any(c in acr['default'] for c in right):
            return True

        if un in acr and any(c in acr[un] for c in right):
            return True
                
        for a in acr:
            if '/&' in a:
                continue
            if acr[a][0] == 'G':
                if un in well('acrGroups', a) and any(c in acr[a] for c in right):
                    return True
                uDn = un.partition('/')[2] # домен пользователя
                grn, _, grDn = a.partition('/') # имя группы , домен группы из ACR
                if uDn == grDn and un in well('acrGroups', grn) and any(c in acr[a] for c in right):
                    return True
    else:
        snd('util.checkRights: no acr for dbAlias: %s (%s)' % (dbAlias, un))



def isRole(dba, un, role):
    
    acr = well('acr', dba) if type(dba) is str else dba
    
    if acr:
        if 'default' in acr and role in acr['default']:
            return True

        if un in acr and role in acr[un]:
            return True
                
        for a in acr:
            if '/&' in a:
                continue
            if acr[a][0] == 'G' and un in well('acrGroups', a) and role in acr[a]:
                return True

# *** *** ***                

def isReader(dbAlias, un):
    return checkRights(dbAlias, un, ['admin', 'creator', 'controller', 'editor', 'reader'])

def isEditor(dbAlias, un):
    return checkRights(dbAlias, un, ['admin', 'creator', 'controller', 'editor'])

def isCreator(dbAlias, un, form=None):
    return checkRights(dbAlias, un, ['admin', 'creator'], form)

def isEraser(dbAlias, un):
    return checkRights(dbAlias, un, ['admin', 'eraser'])

def isAdmin(dbAlias, un):
    return checkRights(dbAlias, un, ['admin'])

# *** *** ***

def notReader(dbAlias, un):
    return not checkRights(dbAlias, un, ['admin', 'creator', 'controller', 'editor', 'reader'])

def notEditor(dbAlias, un):
    return not checkRights(dbAlias, un, ['admin', 'creator', 'controller', 'editor'])

def notCreator(dbAlias, un, form=None):
    return not checkRights(dbAlias, un, ['admin', 'creator'], form)

def notEraser(dbAlias, un):
    return not checkRights(dbAlias, un, ['admin', 'eraser'])

def notAdmin(dbAlias, un):
    return not checkRights(dbAlias, un, ['admin'])

# *** *** ***
