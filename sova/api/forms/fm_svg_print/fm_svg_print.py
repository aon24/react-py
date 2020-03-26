# -*- coding: utf-8 -*- 
'''
Created on 11 apr 2019.

@author: aon
'''
# *** *** ***
try:
    from toolsLC import today
except:
    from .... util.common import today
    
from .. formTools import style, _div, _field, showCode
from .. fm_svg.svgTools import parsePage

import pprint
import json
import sys, io

# *** *** ***

title = 'python'

def page(dbAlias, mode, userName, multiPage):
    pg = _div( **style(height='100vh'),
            children=[ _field('python', 'rtf', **style(font='normal 14px Courier', whiteSpace='pre'))
#                  _field('python', 'fd', br=1,
#                         **style(font='normal 10pt courier', whiteSpace='pre'))
            ] )
    return pg

# *** *** ***

def queryOpen(d, mode, ground):
    myStdout = io.StringIO()
    pprint.pprint( parsePage(json.loads(d.formMaker)), stream=myStdout, width=100000, compact=True )
    form = d.formName or 'formName'
    s = f"""# -*- coding: utf-8 -*- 
'''
Created: {today('-')}

@author: {d.db.userName}

file: api/forms/{form}/{form}.py

'''
# *** *** ***

title = '{d.title}'
javaScriptUrl = ['{d.javaScriptUrl}']
cssUrl = ['{d.cssUrl}']

def initForm():
    pass

# *** *** ***

def page(dbAlias, mode, userName, multiPage):
    pg = {myStdout.getvalue()}
    return pg

# *** *** ***

def queryOpen(d, mode, ground):
    pass
    
# *** *** ***

def querySave(d, dic):
    pass
    
# *** *** ***
# *** *** ***
# *** *** ***

"""
    ss = s.replace('\'"', '\' "').replace('"\'', '" \'')
    d.python = showCode(f"""CODE__{ss}__CODE\n{s}""")
    
# *** *** ***