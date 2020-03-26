# -*- coding: utf-8 -*- 
'''
AON 20 apr 2017

'''
from .. toolbars import toolbar
from .. formTools import labField, style

# *******************

title = 'Default'
forPrint = ''

# *******************

def page(dbAlias, mode, userName, multiPage):

    return dict(
        div = [ \
            style(width='15cm'),
            toolbar.readOnly(mode),
            dict( wl='40mm', className='cellbg-blue', div=labField('Форма не найдена', 'ERROR') ),
        ]
)
    
# *** *** ***
