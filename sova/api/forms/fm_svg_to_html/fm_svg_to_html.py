# -*- coding: utf-8 -*- 
'''
Created on 11 apr 2019.

@author: aon
'''
# *** *** ***
 
from .. formTools import style, _div, _field
from .. fm_svg.svgTools import getStyle

import json


# *** *** ***

title = 'html'

def page(dbAlias, mode, userName, multiPage):
    return  _div( **style(height='100vh'), children=
                [ _field('python', 'rtf', **style(font='normal 14px Courier', whiteSpace='pre')) ]
            )

# *** *** ***

def queryOpen(d, mode, ground):
    js = css = ''
    if d.javaScriptUrl:
        for s in d.javaScriptUrl.split('\n'):
            js += f'    <script src="{s}"></script>\n'
    if d.cssUrl:
        for s in d.cssUrl.split('\n'):
            css += f'    <link rel="stylesheet" href="{s}"/>\n'
    title = d.title.partition(':')[2] or d.title or 'J.Darc'

    d.python = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
{js}{css}</head>
<body style="margin: 0">

{toHtml(json.loads(d.formMaker))}

<a href="content" target="_blank" title="site content" style="position: fixed; bottom:0; left: 0; z-index: 30000">&Xi;</a>
</body>
</html>
'''
# *** *** ***

def toHtml(svg, offset=0):

    el = ''
    attrSvg = svg.get('attributes', {})
    sett = svg.get('setting', {})

    x, y, w, h = [int(attrSvg.get(x, 0)) for x in ['x', 'y', 'w', 'h']]
    if sett.get('position') == 'abs':
        est = dict(position='absolute', left=x-5, top=y-5, width=w, height=h)
    elif sett.get('position') == 'rel':
        est = dict(position='relative', margin=f'{str(y-5)}px 0 0 {str(x-5)}px', width=w, height=h)
    else:
        est = None

    st = getStyle(sett.get('style')) or {}
    if est:
        est.update(st)
        st = est

    style = f''' style="{styleToStyle(st)}"''' if st else ''
    if sett.get('className'):
        attr = f''' class="{sett['className']}"'''
    else:
        attr = ''
        
    typ = sett.get('type')
    for k in ['name', 'id', 'title']:
        v = sett.get(k)
        if v:
            attr += f' {k}="{v}"'
        
    # ***
    if typ == 'svg':
        return '\n' + sett.get('text', '')
    
    # *** *** ***
    '''
    if typ == 'img':
        if sett.get('aImg') == '<a>':
            sett.get('href') and attr.update(href=sett['href'])
            sett.get('target') and attr.update(target='_blank')
            return _img(sett.get('src', ''), sett.get('text'), **attr)
        elif sett.get('aImg') == 'cmd':
            sett.get('cmd') and attr.update(cmd=sett['cmd'])
            sett.get('param') and attr.update(param='param')
            return _img(sett.get('src', ''), sett.get('label'), **attr)
        else:
            return _img(sett.get('src', ''), **attr)
    '''

    # ***
    if typ == 'a':
        if sett.get('href'):
            attr += f''' href="{sett['href']}"'''
        if sett.get('target'):
            attr += 'target="_blank"'
        return f"<a{attr}{style}>{sett.get('text', '')}</a>\n"


    # ***
    if typ == 'button':
        text = sett.get('text', ''),
        cmd = sett.get('cmd', '')

        if sett.get('btnType'): # teg <button>
            return f'''<button{attr}{style} onclick="{cmd}">{sett.get('text', '')}</button>\n'''
        else:                   # teg <div>
            return f'''<div{attr}{style} onclick="{cmd}">{sett.get('text', '')}</div>\n'''
        
    if typ == 'div':
        text = sett.get('text', '')
        if sett.get('br') and text:
            if sett['br'] == 'p':
                text = '\n<p>' + text.replace('\n', '</p>\n<p>') + '</p>\n'
            else:
                text = text.replace('\n', '<br>')
            
        el = f"\n{'    '*offset}<div{attr}{style}>{text}"
        # ***
        
        if svg.get('children'):
            for child in svg['children']:
                ch = toHtml(child, offset+1)
                if ch:
                    el += f"{'    '*offset}{ch}\n"
    
        return el + f"\n{'    '*offset}</div>"

    # ***
    if attrSvg.get('id', '') == 'main':
        el = f'<div{attr}{style}>'
        if svg.get('children'):
            for child in svg['children']:
                ch = toHtml(child, offset+1)
                if ch:
                    el += f"{'    '*offset}{ch}\n"
        return el + '\n</div>'

    print(f"sett.get('type') not def. Type={typ}, id={attrSvg.get('id', '--?--')}")

# *** *** ***

def styleToStyle(cls):
    nst = ''
    for k,v in cls.items():
        kk = ''
        for c in k:
            kk += f'-{c.lower()}' if c.isupper() else c
        nst += kk + (f': {v}px; ' if type(v) is int else f': {v}; ')
    return nst
    
# *** *** ***


