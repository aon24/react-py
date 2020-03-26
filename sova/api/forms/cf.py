# -*- coding: utf-8 -*- 
'''
AON 20 apr 2017

'''
# *** *** ***
# cf - common fields etc
# *** *** ***
try:
    from ...util.common import well
except:
    from tools import well

from .formTools import label, style, _table, _a, _div, _btnD

import re
import json

# *** *** ***

def sw(w):
    return {'style': {'width': '%dmm' % w}}

# *** *** ***

class CF(object):
    def __init__(self):
        self.__dict__['f'] = {}
    
    def __getattr__(self, fieldName):
        return self.f.get(fieldName.upper())
    
    def __setattr__(self, fieldName, fieldValue):
        self.f[fieldName.upper()] = fieldValue
    
# *** *** ***

def docTitle(title, left=None, right=None, width='66%', name=None, classic=None, field=None):
    if left:
        lch = { 'field': (left[0], 'chb', left[1]), 'name': left[0].upper()}
        if classic:
            lch['classic'] = 1
            lch['className'] = 'ttar'
    else:
        lch =  _div('\xa0')

    if right:
        rch = { 'field': (right[0], 'chb', right[1]), 'name': right[0].upper()}
        if classic:
            rch['classic'] = 1
            rch['className'] = 'ttar'
        else:
            rch['style'] = {'textAlign': 'right'}
    else:
        rch =  _div('\xa0')
        
    if field:
        center = { 'field': (field, 'fd'), 'style': { 'width': width }}
    else:
        center = label(title, className=' ', width=width)
   
    return _div( className='cell-title row', **style(padding=2), name=name, children=[lch, center, rch] )

# *** *** ***

def dl(wl):
    return dict ( className='cellbg-blue', wl=wl, div=_table(
        [ label('документ', style={'padding':'0 4px'}), {'field': ('DLDOC_FD', 'json'), 'className':'text-dl'}],
        [ label('заявитель', style={'padding':'0 4px'}), {'field': ('DLCORR_FD', 'fd'), 'className':'text-dl'}],
        [ label('содержание', style={'padding':'0 4px'}), {'field': ('DLSUBJ_FD', 'fd'), 'className':'text-dl'}],
        [ label('первая резолюция', style={'padding':'0 4px'}, name='firstRes'), {'field': ('DLMAINRES_FD', 'fd'), 'className':'text-dl', 'name':'firstRes'}],
    ))

# *** *** ***

def makeDL(d, main):
    d._SENT = d._SENT.replace('<br>', '¤')

    if main:
        dldoc_FD = [_btnD('%s%s%s от %s' % (main.pref, main.docNo, main.suff, main.D('docDa') ), 'docPreview', '%s&%s' % (main.db.alias, main.unid),
                    **style(color='blue', font='bold 10pt Courier'))]
        ls = []
        for dupl in main.getResponses():
            if dupl.main == 'dublicate':
                s = dupl.pref + dupl.docNo + dupl.suff
                dldoc_FD += [_btnD('Дубликат: %s от %s' % (s, dupl.D('docDa') ), 'docPreview', '%s&%s' % (dupl.db.alias, dupl.unid),
                             **style(color='blue', font='normal 10pt Courier'))]
                ls.append(s)
                
        d.dublicates   = '¤'.join(ls)
        d.dldoc_FD     = json.dumps(dldoc_FD, ensure_ascii=False)
        d.dlcorr_FD    = main.fromCorr or main.toCorr or main.corr or main.client
        d.dlcorrLab_FD = 'заявитель' if main.form.lower() == 'rkckg' else 'корреспондент' if d.dlcorrFD else ''
        d.dlsubj_FD    = main.subj[:160]
        d.dlinres_FD   = main.inRes
        d.dlmainres_FD = (main.mainWho + ': ' + main.mainRes) if main.mainWho or main.mainRes else ''
        d.dlmrlab_FD   = 'первая резолюция' if d.dlmainresFD else ''
        d.dlpages_FD   = main.pages
        d.dlthru_FD    = main.thru
        d.dlccDa_FD      = main.ccDa
        d.dldocDa_FD     = main.docDa

        for x in main.A('ADDNO'):
            if x.startswith('Т-') or x.startswith('П-'):
                d.dlAddNo_FD = x
                break
        d.dlAddNo_FD = d.dlAddNo_FD or main.addNo.replace('¤', ' ')
    else:
        d.form += ' Lost ref'
        d.lostRef = d.ref
        d.ref = ''

# *** *** ***

def sent():
    return {'div': [
        {'field': ('_sent', 'fd'), 'style': {'font': 'normal 8pt Courier'}, 'br':'br'},
        {'field': ('_log', 'fd'), 'style': {'font': 'normal 8pt Courier'}, 'br':'br'},
        {'field': ('sent', 'fd'), 'style': {'font': 'normal 8pt Courier'}, 'br':'br'},
    ]}

# *** *** ***
'''
вместо URL может быть строка:
имяПоля|||шаблонURL
пример:
'DEPNAME_ALIAS|||api.getc?loadDropList?whoMade¤_cats_¤{FIELD}¤{FIELD}.*::%s' % well('lsVersions', 'whoByDN¤' + well('MAIN', 'DNAME'))
сформированная url:
"api.getc?loadDropList?whoMade¤_cats_¤RF.AKK.GUPKAD¤RF.AKK.GUPKAD.*::2017-09-07 15:57:55"
well('lsVersions', 'lastVersionWho') - возвращает дату послед изм исполнителя 
'''
cf = CF()

cf.email = {'field': ('email', 'tx'), 'ttaStyle':{'color': '#840'}}

cf.whoRkcki = (
    'who', 'lbsd', '', '"DEPNAME_ALIAS|||' + \
    'list?whoMade¤_cats_¤{FIELD}¤{FIELD}.*::%s"' % well('lsVersions', 'lastVersionWho')
    )

cf.depName = ('depName', 'lbsd', 'dnTitles', "well('MAIN', 'DNAME')" )
 
cf.thru = ('THRU', 'lbme', 'ОГ_поступившее из',
             "(dbProfile.addThru or dbProfile.prjRes or 'ОГ') + \
             (':%s' % dName if well('ОГ_поступившее из', '%s:%s' % (dbProfile.addThru or dbProfile.prjRes or 'ОГ', dName) ) else '')"
            )

cf.hist = ('HIST', 'lbme', 'Результат обращения',
             "(dbProfile.prjRes or 'ОГ') + \
             (':%s' % dName if well('Результат обращения', '%s:%s' % (dbProfile.prjRes or 'ОГ', dName) ) else '')"
            )

cf.thru2 = ('THRU2', 'lbsd', 'ОГ_поступившее через',
             "(dbProfile.addThru or dbProfile.prjRes or 'ОГ') + \
             (':%s' % dName if well('ОГ_поступившее через', '%s:%s' % (dbProfile.addThru or dbProfile.prjRes or 'ОГ', dName) ) else '')"
            )

cf.titleRkckg = ('title', 'lbsd', 'ОГ_вид обращения', 'dbProfile.prjRes')

cf.fromWho = ('FROMWHO', 'lbsd', 'whoSign', 'dName')
cf.visa = ('VISA', 'lbme', 'whoSign', 'dName')

cf.toName = ('TONAME', 'lbsd', 'whoSign', 'dbProfile.toName or dName')

cf.ccType = ('CCTYPE', 'lbsd', 'Вид контроля',
             "(dbProfile.addThru or dbProfile.prjRes or 'ОГ') + \
             (':%s' % dbProfile.dName if well('Вид контроля', '%s:%s' % (dbProfile.addThru or dbProfile.prjRes or 'ОГ', dbProfile.dName) ) \
              else '')"
            )

# *** *** ***

