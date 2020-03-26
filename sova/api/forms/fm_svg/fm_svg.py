# -*- coding: utf-8 -*- 
'''
Created on 24 dec 2018.

@author: aon
'''
try:
    from tools import well
    from toolsLC import today
    from sd import snoDB
except:
    from .... util.common import well, today, snoDB

from .. toolbars import toolbar
from .. formTools import style, _div, _field
from .. dialogs import *
from . svgTools import svgToPy, parsePage
from . pyComponent import lsComp

import json

# *** *** ***

title = 'Sova'
cssUrl = ['jsv?api/views/Outline/outline.css', 'jsv?api/forms/_css/landing.css']

jsUrlEdit = 'jsv?api/forms/fm_svg/fm_svg_edit.js'
jsUrlRead = ['jsv?api/forms/fm_svg/fm_svg_show.js', 'jsv?api/forms/fm_svg/countdown.js']

forPrint = 'Show python|fm_svg_print¤Show HTML|fm_svg_to_html'

cssInline = '''
.contextMenu {
    width: 200px;
    height: 170px;
    position: absolute;
    top: 100px;
    left: 100px;
    background: white;
    padding: 7px;
    border-radius: 7px;
    box-shadow: 0 0 15px 0 #aaa;
}
'''
# *** *** ***

def initForm():
    toWell([
        'button|btn',
        'text|tx',
        'date|dt',
        'droplist|lbsd',
        'checkbox|chb',
        'fileshow|fileShow',
        'list|list',
        'for display only|fd',
        'view|view',
        'json|json',
        'rtf|rtf',
        'table|table',
        'checkbox3|chb3',
            ], 'lsField')
    toWell([
        '<div>',
        '<a+> text </a+>|aText',
        '<img>, <a><img/> text </a>|aImg',
        '<textarea>, <ol>, <ul> |oulta',
        'other teg|allTegs',
            ], 'lsDiv')
    toWell([
        'textPath|textPath',
        'ellipse|ellipse',
        'polygon|polygon',
        ], 'lsSvg')
    toWell(lsComp, 'lsComp')

# *** *** ***
def page(dbAlias, mode, userName, multiPage):
    if mode in ['read', 'preview']:
        return _div( **style(height='100vh'), children=[_field('show', 'json')] )

    return _div(
        className = 'page',
        **style(overflow='hidden', height='100vh'),
        children = [
            toolbar.svg(mode),
            _div(**style(position='relative', height='calc(100vh - 30px)', overflow='auto'), children = [
                _field('formMaker', 'svg', **style(height=4000, width='100vw', background='transparent')),
                _field('cmInsert_FD', 'list', [
                                                    'insert <div>, <a>, etc...|lsDiv',
                                                    'insert HTML-fragment|lsHtml',
                                                    'insert button / field|lsField',
                                                    'insert component|lsComp',
                                                    'insert SVG|lsSvg',

                                                ],
                       name='cmInsert', className='contextMenu', evenColor=1),
                ]
            )
        ]
    )

# *** *** ***

def queryOpen(d, mode, ground):
    global title
    d.webSocketServer = well('webSocketServer')

    if mode in ['read', 'preview']:
        page = parsePage( json.loads(d.formMaker) )
        d.show = json.dumps([page], ensure_ascii=False)
        d.pageProps_fd = d.divProps_fd = d.divMB_fd = d.pageMB_fd = d.formMaker = ''
        title = d.title or 'J.Darc'
    else:
        if mode == 'new':
            d.formMaker = json.dumps(svgToPy(_svgNew), ensure_ascii=False)
            d.main = '1'
            d.dir = '0'

        d.pageProps_fd = json.dumps(pageProps(), ensure_ascii=False)
        d.pageMB_fd = json.dumps(pageMB(), ensure_ascii=False)
        d.divProps_fd = json.dumps(divProps(), ensure_ascii=False)
        d.divMB_fd = json.dumps(divMB(), ensure_ascii=False)
        d.btnProps_fd = json.dumps(btnProps(), ensure_ascii=False)
        d.btnMB_fd = json.dumps(btnMB(), ensure_ascii=False)
        d.fieldProps_fd = json.dumps(fieldProps(), ensure_ascii=False)
        d.fieldMB_fd = json.dumps(fieldMB(), ensure_ascii=False)
        d.aTextProps_fd = json.dumps(aTextProps(), ensure_ascii=False)
        d.aTextMB_fd = json.dumps(aTextMB(), ensure_ascii=False)
        d.imgProps_fd = json.dumps(imgProps(), ensure_ascii=False)
        d.imgMB_fd = json.dumps(imgMB(), ensure_ascii=False)
        d.svgProps_fd = json.dumps(svgProps(), ensure_ascii=False)
        d.svgMB_fd = json.dumps(svgMB(), ensure_ascii=False)
        d.compProps_fd = json.dumps(compProps(), ensure_ascii=False)
        d.tegProps_fd = json.dumps(tegProps(), ensure_ascii=False)
        d.tegMB_fd = json.dumps(tegMB(), ensure_ascii=False)
        d.title = f'{d.docNo}:{d.title}'

# *** *** ***

def querySave(d, dic=None):
    if not d.docNo:
        d.docNo = snoDB(d.db)
    if not d.docDa:
        d.docDa = today('-')
    return True

# *** *** ***
_svgNew = '''
    <svgBox id="main" x="0" y="0" w="0" h="0">
        <svgLine x="0" y="30"/>
        <svgLine x="30" y="0"/>
    </svgBox>
'''
_svg = '''
    <svgBox id="main" x="0" y="0" w="0" h="0">
        <svgLine id="HL" x="0" y="30"/>
        <svgLine id="VL" x="30" y="0"/>

        <svgBox x="150" y="50" w="170" h="200">
            <svgLine id="HL" x="0" y="15"/>
            <svgLine id="VL" x="30" y="0"/>
            <svgBox x="50" y="20" w="70" h="150">
                <svgLine id="HL" x="0" y="15"/>
                <svgLine id="VL" x="30" y="0"/>
                </svgBox>
        </svgBox>
    </svgBox>
'''

# *** *** ***
