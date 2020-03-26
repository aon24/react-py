# -*- coding: utf-8 -*- 
'''
Created on 21 jan 2018

@author: aon
'''
try:
    from .. util.common import well, toWell, config, profile
    from .. util.first import err
except:
    from toolsLC import err
    from tools import config, well, profile
    from common import toWell

import json
import importlib
from copy import deepcopy
from binascii import crc32
import traceback
from datetime import datetime
import os

# *** *** ***

def getFormObj(form, smartPhone):
    form = form.lower() or 'default'
    
    if '[%s]' % form in config.NotCachingReactForms.lower():
        return Form(form, smartPhone)

    form2 = form
    if smartPhone:
        form2 += '-' + smartPhone
    obf = well('forms', form2)

    if not obf:
        obf = Form(form, smartPhone)
        toWell(obf, 'forms', form2)

    return obf

# *** *** ***

class Form(object):
    '''
    module - питоновский модуль, 
    urlForms - словарь в форме, хранит url для форм. КЛЮЧ: path+form+mode, возвращает "apigetc?loadForm&outlet.gru::2113546371"
    form-json - в глобальном словаре готовый json. КЛЮЧ: 'form::CRC-СУММА'
    '''

    def __init__(self, form, smartPhone):
        self.form = form.replace('.', '_')
        self.smartPhone = smartPhone

        self.caching = not ('[%s]' % self.form in (config.NotCachingReactForms + '[arm]') )
        self.module = None
        self.queryOpen = None
        self.urlForms = {}
        self.title = None
        self.forPrint = ''
            
        pf = well('app') + 'api.forms'

        try:
            s = '%s.%s.%s' % (pf, self.form, self.form)
            self.module = importlib.import_module( s )
        except Exception as ex:
            s = 'Форма не найдена: %s\n%s\n%r' % (s, ex, traceback.format_exc())
            err(s.replace('\\n', '\n'), cat=self.form)
            self.form = 'default'
            s = '%s.%s.%s' % (pf, self.form, self.form)
            try:
                self.module = importlib.import_module(s)
            except Exception as ex:
                err('Форма не найдена: %s\n%s' % (s, ex), cat=self.form)
                raise Exception('Форма не найдена')
        
        ini = getattr(self.module, 'initForm', None)
        ini and ini()
            
        self.queryOpen = getattr(self.module, 'queryOpen', None)
        self.querySave = getattr(self.module, 'querySave', None)
        self.title = getattr(self.module, 'title', 'Sova')
        self.forPrint = getattr(self.module, 'forPrint', '')

        self.cssInline = getattr(self.module, 'cssInline', '')

        self.cssJsUrlDict = {'js': {}, 'css': {}}
        self.cssJsUrlDict['js']['all'] = getattr(self.module, 'jsUrl', None) or getattr(self.module, 'javaScriptUrl', None)
        self.cssJsUrlDict['js']['read'] =  getattr(self.module, 'jsUrlRead', None)
        self.cssJsUrlDict['js']['edit'] =  getattr(self.module, 'jsUrlEdit', None)
        self.cssJsUrlDict['js']['new']  =  getattr(self.module, 'jsUrlNew', None) or getattr(self.module, 'jsUrlEdit', None)
        self.cssJsUrlDict['js']['newSd']=  getattr(self.module, 'jsUrlNewSd', None) or getattr(self.module, 'jsUrlNew', None)

        self.cssJsUrlDict['css']['all'] = getattr(self.module, 'cssUrl', None)
        self.cssJsUrlDict['css']['read'] =  getattr(self.module, 'cssUrlRead', None)
        self.cssJsUrlDict['css']['edit'] =  getattr(self.module, 'cssUrlEdit', None)
        self.cssJsUrlDict['css']['new']  =  getattr(self.module, 'cssUrlNew', None) or getattr(self.module, 'cssUrlEdit', None)
        self.cssJsUrlDict['css']['newSd']=  getattr(self.module, 'cssUrlNewSd', None) or getattr(self.module, 'cssUrlNew', None)
        
    # *** *** ***
    
    def jsUrl(self, mode):
        return self.setVersionFiles(self.cssJsUrlDict['js'].get(mode) or self.cssJsUrlDict['js']['all'])
    def cssUrl(self, mode):
        return self.setVersionFiles(self.cssJsUrlDict['css'].get(mode) or self.cssJsUrlDict['css']['all'])
    
    # *** *** ***

    def getUrl(self, dbAlias, mode, userName, multiPage):
        dbAlias = dbAlias or '_'
        dbamode = dbAlias + '-' + mode + '-' + multiPage
        if self.caching and dbamode in self.urlForms:
            return self.urlForms[dbamode]
    
        self.module = importlib.reload(self.module)

        page = deepcopy(self.module.page(dbAlias, mode or 'read', userName, multiPage))
        page = self.parseCell(page, dbAlias, mode, userName)
        jsPage = json.dumps(page, ensure_ascii=False, sort_keys=True)
        crc = crc32(jsPage.encode(), 0)
        
        form2 = self.form
        if self.smartPhone:
            form2 += '-' + self.smartPhone
        
        if self.caching:
            urlForm = 'api.getc?loadForm&%s::%d' % (form2, crc)
        else:
            urlForm = 'api.get?loadForm&%s::%d' % (form2, crc)
        self.urlForms[dbamode] = urlForm
        toWell( jsPage, 'form-json', '%s::%d' % (form2, crc) )

        return urlForm

    # *** *** ***

    def parseRow(self, row, dbAlias, mode, userName):
        if not (row and type(row) is list):
            return []
        
        tr = []
        for cell in row:
            if type(cell) is dict and not cell.get('skip'):
                tr.append( self.parseCell(cell, dbAlias, mode, userName) )
        return tr
    
    # *** *** ***

    def parseCell(self, cell, dbAlias, mode, userName):
        if cell.get('div'):
            teg ={'_teg': 'div', 'attributes': { k: v for k, v in cell.items() if k !='div' } }
            if type(cell['div']) is str:
                teg['text'] = cell['div']
            else:
                teg['children'] = self.parseRow(cell['div'], dbAlias, mode, userName)
            return teg

        if cell.get('_teg') and type(cell.get('children')) is list:
            cell['children'] = self.parseRow(cell['children'], dbAlias, mode, userName)

        elif cell.get('field'):
            try:
                td = [*cell['field']] # в td массив: название, тип[, справочник[, формула]]
                td[0] = td[0].upper()
                cell['field'] = td # замена tuple to list
                
                
                if (td[1].startswith('lb') or td[1] == 'list') and type(td[2]) is not list and '|||' not in td[2]: # поле со сложным списком с url
                    url = td[2]
                    if len(td) > 3: # formula
                        dbProfile = profile(dbAlias)
                        dName = dbProfile.dName
                        if td[2]: # если == '', значит строка url в td[3]
                            url += '|'
                        url += eval(td[3])
                        del td[3]
            
                    if td[2]:
                        ver = well('lsVersions', url) or well('lsVersions', url.replace('|', '¤'))
                        if ver:
                            url = 'api.getc?loadDropList&%s::%s' % (url, ver) # api.getc - кэшируемый
                        else:
                            url = 'api.get?loadDropList&%s' % url # api.get - некэшируемый

                    td[2] = url
            except Exception as ex:
                err('classForm.parseCell: %s %s %r\n%s' % (self.form, dbAlias, cell.get('field'), ex), cat='Ошибка при парсинге полей')
                return 'error?classForm.parseCell: %s' % ex
    
        return cell
    
    # *** *** ***

    def printList(self, d):
        prof = d.db and profile(d.db.alias)
        if not prof:
            return ''
        
        forPr = prof.F(d.form.lower() + '.forPrint') if d.db else ''
        forPr = forPr or self.forPrint
    
        if not forPr and d.ref:
            dd = d.db.getDocumentByUNID(d.ref)
            if dd:
                form = dd.form.lower()
                forPr = prof.F(form + '.forPrint')
                if not forPr:
                    obf = well('forms', form)
                    if not obf:
                        obf = Form(form)
                        toWell(obf, 'forms', form)
                    forPr = obf.forPrint
        return ( (d.REF or d.UNID) + '¤' + forPr ) if forPr else ''

    # *** *** ***

    def qOpen(self, d, mode, ground):
        if self.queryOpen:
            rc = self.queryOpen(d, mode, ground)
            self.title = getattr(self.module, 'title', self.title)
            return rc
    # *** *** ***

    def qSave(self, d, dic):
        if self.querySave:
            try:
                self.querySave(d, dic)
            except Exception as ex:
                err(ex, cat='querySave %s' % self.form)
                return
        return True
    # *** *** ***

    def setVersionFiles(self, ls):
        ols = []
        if ls:
            if type(ls) is str:
                ls = [ls]
            for s in ls:
                if 'jsv?' not in s:
                    ols.append(s)
                else:
                    fn = well('path') + s.partition('jsv?')[2]
                    try:
                        stat = os.stat(fn)
                        v = datetime.fromtimestamp(stat.st_mtime).strftime('%d.%m.%Y-%H:%M:%S')
                        ols.append(s + '::' + v)
                    except:
                        err('js or css not found: ' + fn, cat=self.form)
        return ols



