'''
subtopic.py

Created on 20 апр. 2018 г.

@author: aon
'''
from .... util import common
from .. topic import topic
from .. import formTools
from ... views.viewTools import viewDiv

# *** *** ***

cssUrl = ['jsv?api/forms/topic/topic.css', 'jsv?api/views/Outline/outline.css']
jsUrl = 'jsv?api/forms/topic/topic.js'

# *** *** ***

def page(dbAlias, mode, userName, multiPage):
    return topic.page(dbAlias, mode, userName, multiPage)
        
# *** *** ***

def queryOpen(d, mode, ground):
    global title
    title = d.title
        
    if mode == 'newSd':   # режим создания нового документа, подчиненного ground
        d.ref = ground.ref or ground.unid # служебное поле для создания иерархии
        d.o_level = common.setLevel(ground, d) # служебное поле для сортировки при отображении списка
    elif mode == 'read':
        rtf = formTools.showCode(d.rtf)
        d.rtf = rtf
        d.rgCode = '0002.0004.0051.0239¤0001.0001.0007.0020¤0003.0008.0078.0465¤0002.0004.0048.0232¤0003.0008.0079.0504¤0001.0001.0006.0018.0074'

# *** *** ***
    
