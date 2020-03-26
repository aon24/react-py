window.sovaActions = window.sovaActions || {};
window.sovaActions['outlet.gru'] = {
	recalc: {
        TEMPLATE: (doc, value) => getTemplateText(doc, value),
        WHO: (doc, value) => setTimeout( _ => { doc.setField('WHO', value.replace(/дминистрация/g, 'дминистрацию')) }, 50 ),
    },

    // *** *** ***

    validate: {
        form: doc => new Promise( (yes, no) => {
                return yes();
            }),
    },

    // *** *** ***
};

// *** *** ***

function getTemplateText(doc, value) {
	if (!value)
		return doc.setField('BODYPRN', '');
	
	let fromNo = doc.getField('FROMNO') || doc.getField('ADDNO');
    let fromDa = doc.getField('FROMDA', true) || doc.getField('ADDDA', true); // в русском формате
    let thru   = doc.getField('THRU');
	
    let ls = ['с сайта главы администрации (губернатора) Краснодарского края', 'с сайта администрации Краснодарского края', 'из социальных сетей'];
    ls.forEach( it => { if ( thru.includes(it) ) fromNo = null } );
	
    ls = [	['THRU', ' ', fromNo ? ' (' + fromNo + ' от ' + fromDa + ')' : ''],
			['ONASS', ' по поручению '],
			['WHO'],['THRU2'],['PAGES'],['CCDA'],['APPLICANT'],['ORGNAMEVP'] ];

	fetch('action', { method: 'post', body: 'getTemplateText?ОГ_' + value + ' текст', credentials: 'include' } )
		.then ( response => response.text()	)// тоже промис
		.then ( txt => {
			let s = txt;
			ls.forEach( it => {
				let vl = doc.getField(it[0], true);

				if (it[0] === 'WHO' ) {
					let who = doc.getField('WHO').replace(/¤/g, ', ').replace(/\n/g, ', ');
					let who_soisp = doc.getField('WHO_SOISP').replace(/¤/g, ', ').replace(/\n/g, ', ').replace(/администрация /g, 'администрацию ');
					if (who_soisp)
						who_soisp = ' с запросом информации в ' + who_soisp;
					if ( s.includes('{WHO_SOISP}') )
						s = s.replace('{WHO_SOISP}', who + who_soisp);
					else
						s = s.replace('{WHO}', who);
				}
				else {
					if (vl)
						vl = (it[1] || '') + vl + (it[2] || '');

					while ( s.includes('{' + it[0] + '}') )	// TO DO: заменить цикл на регулярный replace
						s = s.replace('{' + it[0] + '}', vl);
				}
			});
			doc.setField('BODYPRN', s);
		})
		.catch();
}

// *** *** ***

