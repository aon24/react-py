// *** *** ***

window.sovaActions = window.sovaActions || {};
window.sovaActions.topic = {
    recalc: {
        ABC: doc => doc.forceUpdate(), // ABC - имя поля переключателя на CSS (на голубом фоне)
    },
    // *** *** ***
    
    hide: {
        CH2: doc => doc.getField('abc'), // CH2 - параметр "name":"CH2" в описании флажка "только чтение"
    },
    // *** *** ***
    
    cmd: {
        setRed:   doc => addColorForFD(doc, 'R:'),
        setGreen: doc => addColorForFD(doc, 'G:'),
        setBlue:  doc => addColorForFD(doc, 'B:'),
        setBlack: doc => addColorForFD(doc, 'C+'),
        setDivR:  doc => addDivForRTF(doc, 'red'),
        setDivB:  doc => addDivForRTF(doc, 'blue'),
    },
};

let addColorForFD = (doc, c) => {
    let ls = doc.getField('content', 'list');
    (ls[1] !== ls[2]) && doc.setField('content', ls[0].slice(0,ls[1]) + '<<' + c + ls[0].slice(ls[1], ls[2]) + '>>' + ls[0].slice(ls[2]));
};
    
let addDivForRTF = (doc, color) => {
    let ls = doc.getField('rtf', 'list');
    if (ls[1] !== ls[2]) {
        let s1 = '{_ {"div":"';
        let s2 = ls[0].slice(ls[1], ls[2]).replace(/"/g, '\\"').replace(/\n/g, '\\n');
        let s3 = '", "style":{"color":"' + color + '", "fontWeight": "bold"}} _}';
        doc.setField('rtf', ls[0].slice(0,ls[1]) + s1 + s2 + s3 + ls[0].slice(ls[2]));
    }
};
window.sovaActions.subtopic = window.sovaActions.topic;
window.sovaActions.about = window.sovaActions.topic;
