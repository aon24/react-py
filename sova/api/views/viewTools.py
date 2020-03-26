# -*- coding: utf-8 -*-
'''
Created on 27 дек. 2019 г.

@author: aon
'''
from .. forms.formTools import _div
from .toolbars import viewToolbar
try:
    from ... util.first import err
    from ... util.common import well, toWell
except:
    from toolsLC import err
    from tools import well
    from common import toWell

import importlib

# *** *** ***

def viewDiv(fieldName, viewClass, style={}, toolbar=None, title=None, form=None, **par):
    fieldName = fieldName.upper()
    fi = {'field': (fieldName, 'view')}
    divStyle = {'overflow': 'hidden auto', 'display': 'block'}
    divStyle.update(style)
    for k, v in par.items():
        fi[k] = v # стиль вида задается параметром viewStyle={'background': '#fff'...} или **style('viewStyle', background='#fff')

    fi['viewClass'] = viewClass
    if 'dbAlias' in fi:
        dbAlias = fi.get('dbAlias')
    else:
        s = 'dbAlias не указан для вида "%s"' % viewClass
        err(s, cat='viewTools.py.viewDiv')
        return _div('viewTools.py.viewDiv: %s' % s)

    s = 'viewClass', viewClass + '-' + fieldName + '-' + dbAlias
    view = well(s)
    if not view:
        view = makeViewClass(fieldName, viewClass, dbAlias, fi.get('viewAlias'))
    if not view:
        s = 'not view for viewClass "%s"' % viewClass
        err(s, cat='viewTools.py.viewDiv')
        return _div('viewTools.py.viewDiv: %s' % s)

    ls = []
    if toolbar:
        ls.append(viewToolbar(toolbar, dbAlias=dbAlias, form=form, title=title))
    if hasattr(view, 'header'):
        ls.append(view.header())
    ls.append(_div( style=divStyle, children=[fi] ))
    return _div(children=ls)

# *** *** ***

def makeViewClass(fieldName, viewClass, dbAlias, viewAlias):
    s1 = 'api.views.%s.%s' % (viewClass, viewClass)
    s2 = 'sova.api.views.%s.%s' % (viewClass, viewClass)
    try:
        try:
            module = importlib.reload(importlib.import_module(s1))
        except:
            module = importlib.reload(importlib.import_module(s2))
        view = getattr(module, viewClass)(fieldName, viewClass, dbAlias, viewAlias)
        toWell(view, 'viewClass', viewClass + '-' + fieldName + '-' + dbAlias)
        return view
    except Exception as ex:
        err('viewClass "%s"\n%s' % (viewClass, ex), cat='viewTools.py.makeViewClass')

# *** *** ***


