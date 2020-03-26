# -*- coding: utf-8 -*- 
'''
AON 19 apr 2018

'''
from ..forms.formTools import _div, style, _btnD

# *** *** ***

def viewToolbar(tb, dbAlias='', form='', title=''):   
    newDoc = _btnD('\xa0', 'newDoc', dbAlias+'&'+form, title=title, className='tb-new' )
    home = _btnD('home', 'newDoc', 'RF.AKK.MOTIHOR.PSNR/FM_2019&home', title='sova.online', className='armMenuItem', **style(width=40, display='inline') )
    logoff = _btnD('logoff', 'logoff', className='armMenuItem', **style(width=40, display='inline') )
    newSubtopic = _btnD('\xa0', 'newSubtopic', dbAlias+'&subtopic', title='Новый подраздел', className='tb-new',
                   **style(backgroundImage='url(image?rs012.png)', backgroundRepeat='no-repeat') )
    prn = _btnD('\xa0', 'prn', title='[ Ctrl-P ] Печать документа', className='tb-prn')
    
    if tb == 'site':
        return _div(children=[newDoc, newSubtopic, prn], **style(position='relative'), className='toolbar')
    if tb == 'fm':
        return _div(children=[home, newDoc, logoff], **style(position='relative'), className='toolbar')

# *** *** ***
