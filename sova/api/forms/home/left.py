# -*- coding: utf-8 -*-
'''
Created on 18 . 04 . 2018 

@author: aon
'''
from .... util.common import well
from ... views.viewTools import viewDiv
from ... forms.formTools import _div, style

def panel():
    return _div(
        **style(width=250),
        children = [ 
            viewDiv('slideBar',
                viewClass='Outline',
                **style(width=250, height='calc(100vh - 208px)', overflow='auto'),
                dbAlias=well('MAIN', 'BOOK'),
                toolbar='site',
                form='topic',
                title='Новый раздел',
        )]
    )
