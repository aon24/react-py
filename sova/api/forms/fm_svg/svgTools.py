# -*- coding: utf-8 -*-
'''
Created on 24 dec 2018.

@author: aon
'''
from .. formTools import style, _div, _field, _button, _btnD, _a, _img, labField, _form, _teg

try:
    from .... util.first import snd, err, dbg
    from .... dbToolkit.Book import getDocByUnid
    import sova.api.forms.fm_svg.pyComponent as pyComponent
except:
    from toolsLC import snd, err
    from MrDB import getDocByUnid
    import api.forms.fm_svg.pyComponent as pyComponent

from xml.dom.minidom import parseString
from pprint import pprint
import json
import traceback

# *** *** ***

def insertSvgItem(par, un):
    dbAlias, typ, comp = par.split('&')[0:3]

    cn, _, it = comp.partition('|')

    if typ == 'lsField':
        if it == 'btn':
            svg = {'_teg': 'svgBox', **style('setting', type='button', cmd='cmd', text='button', title='title', className='svTop') }
        elif it == 'fileShow':
            svg = {'_teg': 'svgBox', **style('setting', type='field', fn='FILES1_', ft=it, param='wl: 40mm', className='cellbg-green', label='files', labelClassName='label') }
        else:
            svg = {'_teg': 'svgBox', **style('setting', type='field', fn='noname', ft=it, text=f'noname({it})', labelClassName='label')}
        return 200, None, json.dumps(svg, ensure_ascii=False)
    
    if typ == 'lsDiv':
        if it == 'aText':
            svg = {'_teg': 'svgBox', 'setting': {'type': 'a+', 'text': 'link'}}
        elif it == 'aImg':
            svg = {'_teg': 'svgBox', 'setting': {'type': 'img'}}
        elif it == 'allTegs':
            svg = {'_teg': 'svgBox', 'setting': {'type': '_'}}
        else:
            svg = {'_teg': 'svgBox', 'setting': {'type': 'div'}}
        return 200, None, json.dumps(svg)
    
    if typ == 'lsSvg':
        svg = {'_teg': 'svgBox', 'setting': {'type': 'svg', 'text': _svgItems[it]}}
        return 200, None, json.dumps(svg, ensure_ascii=False)
    
    if typ == 'lsHtml':
        d = getDocByUnid(it, dbAlias, un)
        if d:
            try:
                children = json.loads(d.FORMMAKER)['children']
                for x in children:
                    if x.get('_teg') == 'svgBox':
                        return 200, None, json.dumps(x, ensure_ascii=False)
            except Exception as ex:
                err(f'doc: {dbAlias} & lsHtml & {comp}\n{ex!r}', cat='svgTools.loadSvgItem.py')

        return 404, None, f'{dbAlias}&{it} not found'
        
    if typ == 'lsComp':
        f = pyComponent.__dict__.get(cn)
        svg = {'_teg': 'svgBox', 'setting': {'type': 'pyComponent', 'text': cn, '_doc_': f.__doc__}}
        return 200, None, json.dumps(svg, ensure_ascii=False)
    if typ == 'lsMore':
        svg = dictToSvg(pyComponent.__dict__[it]())
        return 200, None, json.dumps(svg, ensure_ascii=False)

    else:
        svg = ''
    return 200, None, svg

# *** *** ***

def parsePage(main):
    sett = main.get('setting')

    children = []
    for child in main.get('children', []):
        ch = parseElement(child)
        ch and children.append(ch)
            
    tBG = sett.get('bgType')
    vBG = sett.get('bgValue', '')

    if tBG == 'video' and vBG:
        pg = _div(
            **style(height='100vh', paddingTop=30, overflow='hidden'),
            children=[
                {'video': 'vi', 'id': 'vi', 'preload': 'auto', 'src': vBG, 'loop':'loop', 'muted': 'muted', 'autoPlay': 'autoplay',
                    **style(position='absolute', zIndex=-1, left=0, top=-200,
                            height='calc(100vh + 240px)', minHeight=854, width='100vw', minWidth=1519)
                },
                *children
            ]
            )
    else:
        st = {'height': '100vh', 'overflow': 'hidden'}
        if tBG == 'img' and vBG:
            st['backgroundImage'] = vBG
            st['backgroundSize'] = '100% 100%'
        elif tBG == 'color' and vBG:
            st['backgroundColor'] = vBG

        cls = getStyle(sett.get('style'))
        cls and st.update(cls)
        attr = {'style': st}
        sett.get('className') and attr.update(className=sett['className'])
        pg = _div( **attr, children=[*children] )
        pg['editMode'] = sett.get('editMode', False)
    return pg
    
# *** ** ***

def parseElement(svg):
    try:
        el = None
        attrSvg = svg.get('attributes', {})
        sett = svg.get('setting', {})
    
        svgId = attrSvg.get('id')
        if not ( svgId and svgId.startswith('box_') ):
            return
    
        x = int(float(attrSvg.get('x', 0)))
        y = int(float(attrSvg.get('y', 0)))
        w = int(float(attrSvg.get('w', 0)))
        h = int(float(attrSvg.get('h', 0)))
    
        typ = sett.get('type')
        attr = {}
    
        v = getStyle(sett.get('style'))
        v and attr.update(style=v)
    
        for k in ['title', 'className', 'name']:
            v = sett.get(k)
            v and attr.update({k: v})
    
        # ***
        
        if typ == 'svg':
            return svgToPy(sett.get('text',{}))
    
        # ***
        
        if typ == 'pyComponent':
            comp = sett.get('text', '_')
            f = pyComponent.__dict__.get(comp)
            if not f:
                return _div(f'pyComponent "{comp}" not found')
            
            p, kv = None, {}
            param = sett.get('param')
            if param:
                p = [x.strip() for x in param.split(',')]
                
            param = sett.get('paramKV')
            if param and len(param) > 2:
                def _evalS(s):
                    if len(s) < 3:
                        return s
                    if s[0] in '"\'':
                        return s[1:-1]
                    if s[0] == '[':
                        return [x.strip() for x in s[1:-1].split(',')]
                    if s[0] == '{':
                        kv2 = {}
                        for it2 in s[1:-1].split(','):
                            k2, _, v2 = it2.partition(':')
                            kv2[k2.strip()] = _evalS(v2.strip())
                        return kv2
                    return s
                
                for it in param.split(','):
                    k, _, v = it.partition('=')
                    kv[k.strip()] = _evalS(v.strip())
            try:
                if p:
                    return f(*p, **kv) if kv else f(*p)
                else:
                    return f(**kv) if kv else f()
            except Exception as ex:
                return _div(f'Error in function "{comp}"\n{ex}', br=1)
            
        # ***
    
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
    
    
        # ***

        if typ == 'button':
            p = [sett.get('text', 'label'), sett.get('cmd', 'cmd')]
            sett.get('param') and p.append(sett['param'])
                
            if sett.get('btnType'): # teg <button>
                attr['type'] = 'submit' if sett.get('submit') else 'button'
                return _button(*p, **attr)
            else:                   # teg <div>
                return _button(*p, div=True, **attr)
    

        # ***
        
        elif typ == 'field':
            fn = sett.get('fn', 'noname')
            ft = sett.get('ft', 'tx')
            
            param = getStyle(sett.get('param'))
    
            # ***
            if ft == 'fileShow':
                param and param.get('wl') and attr.update(wl=param['wl'])
                sett.get('ttaClassName') and attr.update(ttaFileShow=sett['ttaClassName'])
                sett.get('label') and attr.update(label=sett['label'])
                return dict(fileShow=fn, **attr)
            
            
            # ***
            if param:
                for k,v in param.items():
                    v and attr.update({k: v})
            
            v = getStyle(sett.get('ttaStyle'))
            v and attr.update(ttaStyle=v)
    
            sett.get('ttaClassName') and attr.update(ttaClassName=sett['ttaClassName'])
                
            if ft in ['lbsd', 'lbse', 'lbmd', 'lbme', 'chb', 'chb3', 'list']:
                s = sett.get('dropList', '').strip()
                try:
                    ls = eval(s) if s.startswith('[') else s
                except:
                    ls = []
                attr['dropList'] = ls
                
            if sett.get('labfield'):
                children =  [
                                _div(
                                    sett.get('label', ''),
                                    className=sett.get('labelClassName', 'label'),
                                    style=getStyle(sett.get('labelStyle'))
                                ),
                                _field(fn, ft, **attr)
                            ]
                if sett.get('labfield') == 'up':
                    return _div(**style(display='block'), children=children)
                else:
                    c = sett.get('labelStyle', {})
                    c.update({'display': 'table-cell'})
                    children[0]['attributes']['style'] = c
                    return _div(**style(display='table-row'), children=children)
            else:
                return _field(fn, ft, **attr)
    
    
        
        # ***
        
        htmlAttr = getHtmlAttr(sett.get('htmlAttr'))
        htmlAttr.update(attr)
        
        if typ == 'input':
            return {'_teg': typ, 'attributes': htmlAttr}
    
        
        if typ in ['textarea']:
            el = {'_teg': typ, 'attributes': htmlAttr}
            sett.get('text') and el.update(text=sett['text'])
            return el
        
        
        if typ in ['div', 'form', 'span', 'b', 'i', 'p', 'ol', 'ul', 'a', 'a+', 'label']:
            el = {'_teg': 'a' if typ == 'a+' else typ}
            sett.get('text') and el.update(text=sett['text'])
            sett.get('href') and htmlAttr.update(href=sett['href'])
            sett.get('target') and htmlAttr.update(target='_blank')

            if sett.get('position') == 'abs':
                est = dict(position='absolute', left=x-5, top=y-5, width=w, height=h)
            elif sett.get('position') == 'rel':
                est = dict(position='relative', margin=f'{str(y-5)}px 0 0 {str(x-5)}px', width=w, height=h)
            else:
                est = None
                    
            if est:
                st = htmlAttr.get('style', {})
                est.update(**st)
                htmlAttr['style'] = est
    
            for k in ['br', 'id']:
                v = sett.get(k)
                v and htmlAttr.update({k: v})
                
            el['attributes'] = htmlAttr
    
            # ***
        
            children = []
            
            for child in svg.get('children', []):
                ch = parseElement(child)
                ch and children.append(ch)
             
            if children:
                el['children'] = children
        
            return el
        
    except Exception as ex:
        print(traceback.format_exc())
    # ***
    print('sett.get("type") not def', typ)

# *** *** ***

def getStyle(cls):
    if cls:
        ls = cls.replace('\n', ' ').replace("'", ' ').split(';')
        nst = {}
        for x in ls:
            k, _, v = x.partition(':')
            l, _, r = k.partition('-')
            if r:
                k = f'{l}{r[0].upper()}{r[1:]}' 
            v = v.strip()
            if v:
                nst[k.strip()] = int(v) if v.isdecimal() else v
        return nst
    return {}
# *** *** ***

def getHtmlAttr(attr):
    if attr:
        ls = attr.split('\n')
        nst = {}
        for x in ls:
            k, _, v = x.partition('=')
            v = v.strip()
            if v:
                nst[k.strip()] = v
        return nst    
    return {}
    
    
def svgToPy(s):
    def childNode(n):
        def sU(a, c):
            l, _, r = a.partition(c)
            return (l + r[0].upper() + r[1:] if r else a).strip()
        # ***

        svgEl = {'_teg': n.nodeName}
        if n.attributes:
            attributes = {}
            for k, v in n.attributes.items():
                if k == 'style':
                    style = {}
                    for s in v.split(';'):
                        l, _, r = s.partition(':')
                        style[sU(l, '-')] = r.strip()
                    attributes['style'] = style
                elif k == 'class':
                    attributes['className'] = v
                else:
                    attributes[sU( sU(k, ':'), '-' )] = v
            if attributes:
                svgEl['attributes'] = attributes
            
        if n.childNodes:
            chNo = []
            tx = ''
            for child in n.childNodes:
                if  child.nodeName == '#text':
                    tx += child.nodeValue
                else:
                    chNo.append( childNode(child) )
            tx = tx.replace('\n', ' ').strip()
            if tx:
                svgEl['text'] = tx
            if chNo:
                svgEl['children'] = chNo
        return svgEl
    # *** ***
    
    try:
        s = s.replace('xlink:href', 'xlinkHref')
        svg = childNode(parseString(s).childNodes[0])
        return svg
    except Exception as ex:
        return {'ERROR': str(ex)}
    
# *** *** ***

_svgItems = {
    'ellipse':
'''<svg height="130" width="500">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:rgb(255,255,0);stop-opacity:1" />
      <stop offset="100%" style="stop-color:rgb(255,0,0);stop-opacity:1" />
    </linearGradient>
  </defs>
  <ellipse cx="100" cy="70" rx="85" ry="55" fill="url(#grad1)" />
  <text fill="#ffffff" font-size="45" font-family="Verdana" x="50" y="86">SVG</text>
</svg>''',
    
    'textPath':
'''<svg height="130" width="500">
    <defs><path id="myTextPath" d="M75,20 a1,1 0 0,0 100,0"/></defs>
    <text x="10" y="100" style="stroke: #000000;">
      <textPath xlink:href="#myTextPath" >
            Sova.online - step to
      </textPath>
    </text>
</svg>''',

    'polygon':
'''<svg width="230" height="140">
    <polygon points="5,135 115,5 225,135" fill="violet" stroke="purple" stroke-width="5" />
</svg>'''
}
# *** *** ***

def dictToSvg(elem, i=0):
    if not (type(elem) is dict):
        return
    teg = elem.get('_teg')
    if not teg:
        return
    
    svg = {'_teg': 'svgBox'}
    svg['attributes'] = { 'x': 10+i, 'y': 10+i, 'w': '150px', 'h': 140}
    sett = {'type': teg}
    for k,v in elem.get('attributes', {}).items():
        if type(v) is dict:
            sett[k] = '; '.join([f'{kk}: {vv}' for kk,vv in v.items()])
        else:
            sett[k] = v
            
    sett['text'] = elem.get('text', '')
    sett['cmd'] = elem.get('_cmd', '')
    sett['param'] = elem.get('_param', '')
    svg['setting'] = sett
    
    child = []
    i = 0
    for c in elem.get('children', []):
        ch = dictToSvg(c, i)
        if ch:
            child.append(ch)
            i += 10
    if child:
        svg['children'] = child
        
#     pprint(svg)
    return svg

# *** *** ***
