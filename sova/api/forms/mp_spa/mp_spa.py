# -*- coding: utf-8 -*- 
'''
Created on 16.05.2018

@author: aon
'''
from .. .. api.forms.formTools import style, _div, _btnD

cssUrl = ['jsv?api/forms/home/home.css']

jsUrl = [ 'jsv?api/forms/mp_spa/multipage.js',
    'jsv?api/forms/rkckg/rkckg.js',
    'jsv?api/forms/outlet_gru/outlet_gru.js',
    'jsv?api/forms/outlet/outlet.js',
    'jsv?api/forms/o/o.js',
    ]
     
title = 'Multiwindow page'

def page(dbAlias, mode, userName, multiPage):
    return _div(
        **style(overflow='auto', padding=10, height='100wv', width=1100),
        className = 'page',
        children=[ _div(className='topnav', **style(float='right'), children=[_btnD('log', 'newDoc', '&lm', title='Application log')])]
    )

# *** *** ***    

def queryOpen(d, mode, ground):
    d._page_ = '1'

# *** *** ***    
    
