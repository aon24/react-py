# -*- coding: utf-8 -*- 
'''
AON 9 mar 2018

'''
from .. formTools import style, _div
from .... util.common import well

import importlib

# *******************

def initForm():
    pass

# *** *** ***

title = 'React-py'
cssUrl = ['jsv?api/views/Outline/outline.css', 'jsv?api/forms/home/home.css']
jsUrl = ['jsv?api/forms/home/home.js']

# *** *** ***

def page(dbAlias, mode, userName, multiPage):
    s = well('app') + 'api.forms.home.'
    subFormTop = importlib.reload( importlib.import_module(s + 'top') ) 
    subFormLeft = importlib.reload( importlib.import_module(s + 'left') )
    subFormRight = importlib.reload( importlib.import_module(s + 'right') )
#     subFormDown = importlib.reload( importlib.import_module(s + 'down') )
    
    return _div(
        children = [
            _div( **style(width=1000, margin='auto', paddingTop=10, height='calc(100wh - 10px', overflow='hidden'),
                children=[
                    _div( children=[*subFormTop.panel()] ),
                    _div( children=[subFormLeft.panel(), subFormRight.panel()], className='row'),
# #                     { 'div': [subFormDown.panel()] },
            ]),
        ]
    )

# *** *** ***

def queryOpen(d, mode, ground):
    d._page_ = '1'

# *** *** ***









