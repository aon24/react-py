# -*- coding: utf-8 -*- 
'''
AON 19 jan 2018

'''
from . formTools import style, _div, _btnD

# *** *** ***

class Toolbar(object):
    
    close = _btnD('З А К Р Ы Т Ь'.replace(' ', '\u00a0'), 'close', title='[Esc] - закрыть окно', className='toolbar-button', **style(width='37mm') )
    prn =   _btnD('\u00a0', 'prn', title='Ctrl+P', className='tb-prn')
    edit =  _btnD('Р Е Д А К Т И Р О В А Т Ь'.replace(' ', '\u00a0'), 'edit', title='[Ctrl-Enter] - перейти в режим редактирования', className='toolbar-button', **style(width='67mm') )
    saveClose = _btnD('С О Х Р А Н И Т Ь  И  З А К Р Ы Т Ь'.replace(' ', '\u00a0'), 'saveClose',
                  title='[Shift+Esc] - сохранить и закрыть, [Ctrl-S] - только сохранить', className='toolbar-button', **style(width='67mm') )
    docSN = _btnD('\u2116 п/п', 'docSN', title='[Alt-1] Присвоить очередной № (для настройки нажмите кнопку при заполненном поле номера)', className='toolbar-button', **style(width='16mm') )
    searchByCorr = _btnD('Поиск', 'searchByCorr', title='Поиск обращений по заявителю и району', className='toolbar-button', **style(width='16mm') )

    red =   _btnD('\u00a0', 'setRed', **style(background='red', width=20), className='toolbar-button')
    green = _btnD('\u00a0', 'setGreen', **style(background='green', width=20), className='toolbar-button')
    blue =  _btnD('\u00a0', 'setBlue', **style(background='blue', width=20), className='toolbar-button')
    black = _btnD('B', 'setBlack', **style(background='#aaa', width=20), className='toolbar-button')
    commentR = _btnD('Div', 'setDivR', **style(background='#fde', width=40), className='toolbar-button')
    commentB = _btnD('Div', 'setDivB', **style(background='#def', width=40), className='toolbar-button')
    
    close = _btnD('З А К Р Ы Т Ь'.replace(' ', '\u00a0'), 'close', title='[Esc] - закрыть окно', className='toolbar-button', **style(width='67mm') )

    save2 = _btnD('   S A V E   '.replace(' ', '\u00a0'), 'save', title='Ctrl+S', className='toolbar-button')
    saveClose2 = _btnD(' S A V E   A N D   C L O S E '.replace(' ', '\u00a0'), 'saveClose', title='Shift+Esc', className='toolbar-button')
    close2 = _btnD(' C L O S E '.replace(' ', '\u00a0'), 'close', title='Esc', className='toolbar-button')
    
    # *** *** ***
    
    def svg(self, mode):
        return _div(className='toolbar', children=[self.save2, self.saveClose2, self.close2, self.prn])
    
    def rkck(self, mode):
        if mode == 'preview':
            return 0
        
        elif mode == 'read':
            buttons = [self.edit, self.close, self.prn]

        elif mode in ['edit', 'new', 'newSd']:
            buttons = [self.docSN, self.saveClose, self.searchByCorr, self.close, self.prn]

        else: # mode == 'readOnly':
            buttons = [self.close, self.prn]

        return _div(className='toolbar', children=buttons)
        
    # *** *** ***
    
    def o(self, mode):
        if mode == 'preview':
            return 0
        
        elif mode == 'read':
            buttons = [self.edit, self.close, self.prn]

        elif mode in ['edit', 'new']:
            buttons = [self.saveClose, self.close, self.prn]

        else: # mode == 'readOnly':
            buttons = [self.close, self.prn]

        return _div(className='toolbar', children=buttons)
        
    # *** *** ***

    def readOnly(self, mode):
        if mode == 'preview':
            return 0
            
        return _div(className='toolbar', children=[self.close])
        
    # *** *** ***
    
    def rgb(self, mode='edit'):
        return _div(className='toolbar', children=[self.saveClose, self.red, self.green, self.blue, self.black, self.commentR, self.commentB, self.close])
        
# *** *** ***

toolbar = Toolbar()
