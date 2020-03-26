
// *** *** ***
window.sovaActions = window.sovaActions || {};
window.sovaActions.o = {
    
    // *** *** ***
    
    recalc: {
        PROJECTO: doc => doc.forceUpdate(),
        RES: (doc, v) => prjResolutionsParsing('RES', doc, v),
        RESPRJ1: (doc, v) => prjResolutionsParsing('RESPRJ1', doc, v),
        RESPRJ2: (doc, v) => prjResolutionsParsing('RESPRJ2', doc, v),
        RESPRJ3: (doc, v) => prjResolutionsParsing('RESPRJ3', doc, v),
        RESPRJ4: (doc, v) => prjResolutionsParsing('RESPRJ4', doc, v),
        RESPRJ5: (doc, v) => prjResolutionsParsing('RESPRJ5', doc, v),
        WHOPRJ1: doc => doc.forceUpdate(),
        WHOPRJ2: doc => doc.forceUpdate(),
        WHOPRJ3: doc => doc.forceUpdate(),
        WHOPRJ4: doc => doc.forceUpdate(),
        WHOPRJ5: doc => doc.forceUpdate(),
      },

    // *** *** ***
  
    hide: {
        firstRes: doc => !doc.fieldValues.DLMAINRESFD,
        project: doc => !doc.getField('projectO'),
        op: doc => doc.getField('projectO'),
        prj1: doc => !doc.getField('projectO'),
        prj2: doc => !doc.getField('projectO'),
        prj3: doc => !doc.getField('projectO') || (!doc.getField('whoPrj2') && !doc.getField('whoPrj3')),
        prj4: doc => !doc.getField('projectO') || (!doc.getField('whoPrj3') && !doc.getField('whoPrj4')),
        prj5: doc => !doc.getField('projectO') || (!doc.getField('whoPrj4') && !doc.getField('whoPrj5')),
      },

    // *** *** ***
  
    readOnly: {
        SENTOK: doc => !doc.fieldValues.MODIFIED,
        who: doc => doc.fieldValues.SENTFROMDB || doc.fieldValues.SENTOK || doc.fieldValues.SMTPSENTOK === '1',
        fromWho: doc => doc.fieldValues.SENTFROMDB || doc.fieldValues.SENTOK || doc.fieldValues.SMTPSENTOK === '1',
        files1: doc => doc.fieldValues.SENTFROMDB || doc.fieldValues.SENTOK || doc.fieldValues.SMTPSENTOK === '1',
        sendCCDa: doc => doc.fieldValues.SENTFROMDB || doc.fieldValues.SENTOK || doc.fieldValues.SMTPSENTOK === '1',
        prj1: doc => doc.fieldValues.SENTFROMDB || doc.fieldValues.SENTOK || doc.fieldValues.SMTPSENTOK === '1',
        prj2: doc => doc.fieldValues.SENTFROMDB || doc.fieldValues.SENTOK || doc.fieldValues.SMTPSENTOK === '1',
        prj3: doc => doc.fieldValues.SENTFROMDB || doc.fieldValues.SENTOK || doc.fieldValues.SMTPSENTOK === '1',
        prj4: doc => doc.fieldValues.SENTFROMDB || doc.fieldValues.SENTOK || doc.fieldValues.SMTPSENTOK === '1',
        prj5: doc => doc.fieldValues.SENTFROMDB || doc.fieldValues.SENTOK || doc.fieldValues.SMTPSENTOK === '1',
      },
  
    //*** *** ***
  
    validate: {
        who: doc => doc.getField('who') ? '' : 'Не заполнено поле "Кому направлено"',
        sendDa: doc => doc.getField('sendDa') ? '' : 'Не заполнено поле "Дата передачи"',

        form: doc => new Promise( (yes, no) => {
            let disableAutoOrder = doc.getField('ccType') === 'запрос';
            for (let i = 1; i <= 5; i++) {
                let val = doc.getField('RESPRJ' + i);
                if ( /за моей подписью/.test(val) && !/(сообщите|проинформируйте)\s+(каждому|каждого)?\s*заявител/.test(val) ) {
                    disableAutoOrder = true;
                }
            }
            disableAutoOrder && doc.setField('AUTOORDER', '');
            yes();
        }),
      },
      
    // *** *** ***
  
    cmd: {
        returnO: doc => {
            if ( doc.getField('SENTFROMDB') )
                doc.msg.box('\nОтправить результат\n\nв журнал отправителя переметки?', 
                        'Подтвердите отправку',
                        ['Отправить+|Y', 'Отмена'])
                    .then( _ => {
                        doc.setField('SENTOK', '');
                        doc.setField('FORSEND', '1');
                        doc.setField('RETURNAGAIN', '1');
                        doc.setField('MAINPOSTING', '1');
                        if ( !doc.getField('CLS2DA') )
                            doc.setField('CLS2DA', new Date());
                        doc.cmdSave(true);
                    })
                    .catch ( _ => {} );
            else
                doc.msg.box('Переметка создана в этом журнале.\n\nОтправка невозможна.', 'Предупреждение');
        },
    },
};

// *** *** ***
// *** *** ***

let prjResolutionsParsing = (fi, doc, v) => {
    let re = /_CCDA\/[\S]+_/gi;
	let arr = [
			[/_PAGES_/g, 'DLPAGES_FD'],
			[/_CCDA_/g, 'CCDA'],
			[/_THRU_/g, 'DLTHRU_FD'],
			[/_DOCNO_/g, 'DOCNO'],
			[/_DOCDA_/g, 'DOCDA'],
			[/_ADDNO_/g, 'DLADDNO_FD'],
			[/_LPINFO_/g, 'LPINFO'],
		];

    let res = v;
	arr.forEach( it => res = res.replace(it[0], doc.getField(it[1], true)) );
    let s = '';
    try {
        match = res.match(re);
        if (match) {
            let found = match[0];
            let i = found.indexOf('/');
            let days = found.slice(i+1, -1);
            let ls = doc.getField('ccDa').split('-');
			if ( ls.length > 2 ) {
				let da = new Date(+ls[0], +ls[1]-1, +ls[2]);
				s = doc.util.formatDate( new Date( da.valueOf() + 1000*60*60*24*days ) );
			}
        }
    }
    catch(ex) {
        console.log('prjResolutionsParsing', ex);
    }
    setTimeout( _ => doc.setField(fi, res.replace(re, s)), 100);
}

// *** *** ***
