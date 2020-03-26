# -*- coding: utf-8 -*- 
'''
AON 20 apr 2017

'''
import re

# *** *** ***

def _div(tx=None, **kv): return _teg('div', tx, **kv)
def _form(**kv): return _teg('form', **kv)
def _input(**kv): return _teg('input', **kv)
def _textarea(tx, **kv): return _teg('textarea', tx, **kv)
def _b(tx=None, **kv): return _teg('b', tx, **kv)
def _i(tx=None, **kv): return _teg('i', tx, **kv)
def _p(tx=None, **kv): return _teg('p', tx, **kv)
def _span(tx=None, **kv): return _teg('span', tx, **kv)
def _ul(tx=None, **kv): return _teg('ul', tx, **kv)
def _ol(tx=None, **kv): return _teg('ol', tx, **kv)
def _a(tx=None, **kv): return _teg('a', tx, **kv)

def _teg(teg, text=None, **kv):
    tg = {'_teg': teg}
    if text:
        tg['text'] = text
    attr = {}
    for k, v in kv.items():
        if v:
            if k == 'children':
                tg['children'] = v
            else:
                attr[k] = v
    if attr:
        tg['attributes'] = attr
    return tg


def _btnD(*p, **kv):
    return _button(*p, div=True, **kv)

def _button(*p, div=None, **kv):
    bt = {'_teg': 'button', 'text': p[0], '_cmd': p[1], 'attributes': { k: v for k, v in kv.items() if v }}
    if div:
        bt['_div'] = 1
    if len(p) > 2:
        bt['_param'] = p[2]
    return bt

def _img(src, text=None, **attr):
    return {'_teg': 'img', 'text': text, 'attributes': {'src': src, **attr} }

def _h2(tx, **attr):
    return _div(tx, className='h2', **attr)

def _h3(tx, **attr):
    return _div(tx, className='h3', **attr)

def _br():
    return {'_teg': 'br'}

def _table( *rows):
    for row in rows:
        if type(row) is list:
            rowClassName = None 
            for it in row:
                rowClassName = rowClassName or (type(it) is dict and it.get('rowClassName', None))
            if not rowClassName:
                row.append({'rowClassName': 'rowf'})
    return [{'div': r} for r in rows]

def _row(*p, **kv):
    return {'_teg': 'div', 'attributes': {**kv}, 'children': [*p]}


def style(s='style', **par):
    return {s: {**par}}

def viewDiv(fiName, **par):
    from .. views.toolbars import viewToolbar
    
    fi = {'field': (fiName, 'view')}
    divStyle = { 'width': '100%'}
    viewStyle = { 'overflowY': 'scroll', 'overflowX': 'hidden', 'width': '100%', 'height': '99vh'}
    toolbar = None
    dba = form = title = ''
    
    for k, v in par.items():
        if k == 'divStyle':
            divStyle.update(v)
        elif k == 'viewStyle':
            viewStyle.update(v)
        elif k == 'toolbar':
            toolbar = v
        elif k == 'title':
            title = v
        elif k == 'dbAlias':
            dba = v
            fi[k] = v
        elif k == 'form':
            form = v
        else:
            fi[k] = v
            
    
    fi['style'] = viewStyle
    if toolbar:
        view = { 'style': divStyle, 'div': [viewToolbar(toolbar, dbAlias=dba, form=form, title=title), {'div': [fi]}] }
    else:
        view = { 'style': divStyle, 'div': [{'div': [fi]}] }
    return view


def label(l=None, width=None, style=None, className='label', name=None):
    dic = {'className': className}
    if name:
        dic['name'] = name
    if style:
        dic['style'] = style
        if width:
            dic['style']['width'] = width
    elif width:
        dic['style'] = {'width': width}
    return _div(l or '\xa0', **dic)


def label_(l=None, width=None, style=None, className='label_'):
    return label(l, width, style, className)


def labField(l, fname, ftype='tx', flab=None, **par):
    return [label(l), _lbf(fname, ftype, flab, **par)]

def labField_(l, fname, ftype='tx', flab=None, **par):
    return [label_(l), _lbf(fname, ftype, flab, **par)]

def _lbf(fname, ftype='tx', flab=None, **par):
    if 'dropList' in par:    
        f = {'field': (fname, ftype or 'lbsd', par['dropList'])}
    elif flab:
        f = {'field': (fname, ftype, flab)}
    else:
        f = {'field': (fname, ftype)}
    for k, v in par.items():
        if k != 'dropList':
            f[k] = v
    
    return f

def _field(*p, **dp):
    return _lbf(*p, **dp)

def _field4(fn, ft, dl1, dl2, **kv):
    return {'field': (fn, ft, dl1, dl2), **kv}

# *** *** ***

def showCode(plain):
    '''
    Наипримитивнейший раскрасчик кода.
    Заменяет строки, комментарии и ключевые слова на элементы дизайна "div".
    Границами нового элемента служат сочетания "{_" и "_}" без пробела.
    '''
    code = re.search('CODE__([\\s\\S]+)__CODE', plain)
    if not code:
        return plain

    s = code.group(1).replace('{_', '{ _').replace('_}', '_ }').replace('\\', '\\\\').replace('"', '\\"').replace('\\"\'', '"\'').replace('\'\\"', '\'"')
    
    i = 0
    ls = []
    for c in set(re.findall("'''[\\s\\S]+?'''", s)):   # убираем из кода многостроки в массив ls
        ls.append('{_{"div": "%s", "style": {"color": "green", "display":"inline", "fontWeight": "bold"}}_}' % c.replace('\n', '\\n'))
        s = s.replace(c, '___%d___' % i)
        i += 1
    for c in set(re.findall("'[\\s\\S]*?'", s)):   # убираем из кода строки в массив ls
        ls.append('{_{"div": "%s", "style": {"color": "green", "display":"inline", "fontWeight": "bold"}}_}' % c)
        s = s.replace(c, '___%d___' % i)
        i += 1
    for c in set(re.findall('#[\\s\\S]+?\n', s)):    # убираем из кода комментарии в массив ls (лучший цвет - красный)
        ls.append('{_{"div": "%s", "style": {"color": "red", "display":"inline", "fontWeight": "bold"}}_}\n' % c[0:-1])
        s = s.replace(c, '___%d___' % i)
        i += 1
    for c in set(re.findall('//[\\s\\S]+?\n', s)):    # убираем из кода комментарии в массив ls (лучший цвет - красный)
        ls.append('{_{"div": "%s", "style": {"color": "red", "display":"inline", "fontWeight": "bold"}}_}\n' % c[0:-1])
        s = s.replace(c, '___%d___' % i)
        i += 1

    # теперь можно раскрасить синтаксис
    for c in ['let', 'None', 'true', 'window','class', 'from', 'import', 'set', 'list', 'dict', 'def', 'for', 'in', 'if', 'elif', 'else', 'return', 'and', 'or', 'not']:
        s = re.sub ('\\b%s\\b' % c, '{_{"div": "%s", "style": {"color": "blue", "display":"inline", "fontWeight": "bold"}}_}' % c, s)

    for j in range(i):  # восстанавливаем строки и комментарии с новым окрасом
        s = s.replace('___%d___' % j, ls[j])
        
    return plain.replace(code.group(0), s)

# *** *** ***

