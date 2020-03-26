window.sovaActions = window.sovaActions || {};
window.sovaActions.fm_manager = {
    init: doc => doc.changeDropList('SUBCAT'),

    //*** *** ***
  
    recalc: {
        CAT: (doc, label, opt, i) => {
            doc.changeDropList('SUBCAT');
            doc.setField( 'view1', i && label );
        },
        SUBCAT: (doc, label, opt, i) => doc.setField( 'view1', doc.getField('cat') + '|' + (i ? label : '') ),
    },
  
    cmd: {
    	logoff: doc => { window.location.href = '/logoff' },
        copy: (doc, unid) => {
            let act = ['copy?' + doc.dbAlias, unid].join('&');
            
            doc.util.serverAction(doc, act)
                .then( _ => doc.msg.box('Агент успешно запущен', 'Запуск сбора отчета') )
                .catch( e => doc.msg.error(e) );
        },
    },
};

// *** *** ***














