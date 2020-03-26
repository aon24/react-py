# -*- coding: utf-8 -*-

'''
Created on 04 mar 2019

@author: aon
'''

from . fm_manager import setList

def reportList(dbAlias):
    return {

    'Лидинговые формы|Лидинговые формы':
        setList(dbAlias, 1, ['Ф.01|l-01','l-02',], comment='Формы 1.01...',),

    'Формы главных документов|РКФ':
        setList(dbAlias, 2, ['Ф.02|rk-02','rk-02',], comment='Формы 2.01...',),

    'Формы подчиненных документов|o':
        setList(dbAlias, 3, ['Ф.03|o-01','o-02',], comment='Формы 3.01...',),

    'Справочники|cls':
        setList(dbAlias, 4, ['Ф.04|cls-01','cls-02',], comment='Формы 3.01...',),
    }
