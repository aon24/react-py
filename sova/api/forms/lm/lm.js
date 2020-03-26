window.sovaActions = window.sovaActions || {};
window.sovaActions.lm = {
    init: doc => doc.changeDropList('CAT'),
    recalc: {
        TYPE: (doc, label, alias) => {
            doc.changeDropList('CAT');
            getLogData(doc, alias + '|A L L');
        },
        CAT: (doc, label) => getLogData(doc, doc.getField('type_alias') + '|' + label),
    },
};

// *** *** ***

let getLogData = (doc, keys) => {
    fetch('api.get?getLogData&' + keys, {method: 'get', credentials: 'include'})
        .then( response => response.text() )
        .then( txt => doc.setField('msg', txt) )
        .catch( err => doc.setField('msg', err.message) );
};
