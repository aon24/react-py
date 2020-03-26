//
// AON 10 mar 2018
//
// *** *** ***

window.sovaActions = window.sovaActions || {};
window.sovaActions.mp_spa = {
    init: doc => {
        let tm = 100;
        let props1 = {
            page: 'rkckg',
            title: 'Обращение (сделано на Питоне)',
            dbAlias: 'SOVA/SITE',
            unid: '5E592E3BBAEC5E74240FCF656A0250D3',
            frameStyle: {width: 1000, height: 550, top:67, left:10},
            rsMode: 'read|mp',
        };
        setTimeout( _ => doc.addPage(props1), 10);
        
        let props3 = {
                page: 'outlet.gru',
                title: 'Уведомление (made on Python)',
                dbAlias: 'SOVA/SITE',
                unid: '1BFA4B6247D951460EDD070F283DFFEF',
                frameStyle: {width: 790, height: 550, top:170, left:210},
                rsMode: 'read|mp',
            };
        setTimeout( _ => doc.addPage(props3), tm);
        
        let props4 = {
                page: 'outlet',
                title: 'Закрытие (made on Python)',
                dbAlias: 'SOVA/SITE',
                unid: '0F8FDE80554D54B015FEEB90A9458160',
                frameStyle: {width: 790, height: 550, top:240, left:125},
                rsMode: 'readOnly|mp',
            };
        setTimeout( _ => doc.addPage(props4), tm*2);
    
        let props2 = {
                page: 'o',
                title: 'Отметка о передаче (made on Python)',
                dbAlias: 'SOVA/SITE',
                unid: '5C6945A82CB55D8E314456DA2FAB9A38',
                frameStyle: {width: 795, height: 550, top:110, left:260},
                rsMode: 'edit|mp',
            };
        setTimeout( _ => doc.addPage(props2), tm*3);
        
    },

    cmd: {
        download: (doc) => {
            let props = {
                    page: 'download',
                    title: 'Проект Сова',
                    dbAlias: 'SOVA/SITE',
                    unid: '300507B99F5A55B73A14798AFCB7D812',
                    frameStyle: {width: 700, height: 450, top:190, left: 200},
                    rsMode: 'read|mp',
                };
                doc.addPage(props);
        },
        logoff: doc => { window.location.href = '/logoff' },
    },
};

// *** *** ***

