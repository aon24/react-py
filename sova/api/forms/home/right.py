# -*- coding: utf-8 -*-
'''
Created on 18 . 04 . 2018 

@author: aon
'''
from .. formTools import style

def panel():
    return dict (
        className = 'cellTitle',
        div = [
            { 'iframe': ' ', 'name':'article',
             **style(width='99.5%',
                    height='calc(100vh - 180px)',
                    margin=0,
                    border='1px solid #aaa',
                    )
            }
        ]
    )
