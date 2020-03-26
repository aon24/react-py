//
// AON 10 mar 2018
//
// *** *** ***

window.sovaActions = window.sovaActions || {};
window.sovaActions.home = {
    init: doc => {},

    cmd: {
        about: doc => doc.msg.box('This is a prototype.\nFor the development of the system young self-confident impudents are needed, who will say:\n"Everything is wrong, everything needs to be redone".\n\nI agree with them: let them do it.\nI am ready to transfer the rights.\n\nYou can write to e-mail:  aon24@mail.ru\n\n or call +7-921-9935515\n\nRegards, Alexey Nosikov', 'response'),
        
        help: doc => doc.msg.box('но много денег все равно никто не даст,\n\nа мало денег у меня и так есть.', 'Помощь|Мне нужна ваша помощь, '),
        
        viewLoaded: (doc, param) => {
            let [view, dbaUnid] = param.split('|');
            if (view === 'SLIDEBAR' && dbaUnid)
                doc.setField('article', 'docopen?' + dbaUnid);
        },
    
        docInIframe: (doc, dbaUnid, ctrl) => ctrl ?
            window.open('docopen?' + dbaUnid + '&edit')
            :
            doc.setField('article', 'docopen?' + dbaUnid),

        newSubtopic: (doc, dbaUnid) => doc.setField('article', 'newdoc?&subtopic&' + doc.getField('SLIDEBAR')),
        
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

