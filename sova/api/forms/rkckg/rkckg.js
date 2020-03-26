window.sovaActions = window.sovaActions || {};
window.sovaActions.rkckg = {
    recalc: {
        RNN:  doc => window.rnnGroup(doc),
        TOWN: doc => window.rnnGroup(doc),
        RGCODE: (doc, value, i) => {
            if ( value ) {
                
            }
            else {
                ['RGPART', 'RGTHEME', 'RGSUBJ', 'RGASK'].forEach( it => {
                    let ls = doc.getField(it).split('\n');
                    ls = ls.filter( (x, j) => i !== j );
                    doc.setField(it, ls.join('\n'));
                });
            }
        },
    },
};

// *** *** ***

window.rnnGroup = (doc, fill) => {	// из recalc для полей RNN и TOWN , from  fillFields

	// для МО город Краснодар формирует постфикс и из первой буквы поселения (округа)
	if ( doc.dbAlias.startsWith('RF.AKK.MOKRASG/') )
		return doc.setField('SUFF', '-' + doc.getField('TOWN').charAt(0) );

	// Для АКК:
	// формирует поле rnnGroup, суффикс номера и адрес по району
	// ta - поле "район" или "поселение"
	// ls формируется из алиаса района:  [ФИО_главы, почт_индекс, rnnGroup]
	// fill - true, если функция вызвана после заполнения полей, адрес менять не надо

	let rnn  = doc.getField('RNN').trim();
	let rnAl = doc.getField('RNN_ALIAS');
	if ( !rnAl )
		return;

	let ls = rnAl.split('|');

	if ( ls.length > 1 && !fill && ( doc.isNew || !doc.getField('FROMADDRESS') || doc.getField('_IMAPUID') ) ) // очень сложно
		doc.setField('FROMADDRESS', ls[1] + ', ' + rnn + (rnn.endsWith('й') ? ' район, ' : ', ') );

	if ( ls.length > 2 ) {
		let fio = doc.getField('FROMCORR').trim().slice(0,1).toUpperCase();
		let rnnGr = ls[2];
		if (rnn === "Краснодар") {
			rnnGr = "31";  // Default value
			if (fio >= "А" && fio <= "Й") rnnGr = "31";
			if (fio >= "К" && fio <= "О") rnnGr = "34";
			if (fio >= "П" && fio <= "Я") rnnGr = "36";
		}

		doc.setField('RNNGROUP', rnnGr);

		let suff = doc.getField('SUFF');
		suff = suff.slice(-2) === '-0' ? suff + '0' : suff;
		if  ( suff.length > 5 && suff.slice(-3, -2) === '-' )
			doc.setField( 'SUFF', suff.slice(0, -2) + ('xx' + rnnGr).slice(-2) );

		// заявка № 1056 -ТО от 03.03.2017: при регистрации в журнале КПИ, если обращение поступило не по телефону...
		else if ( doc.getField('THRU').indexOf('по телефону администрации Краснодарского края') < 0 && doc.dbAlias.startsWith('RF.AKK/OGKPI') )
			doc.setField( 'SUFF', suff + '-' + rnnGr );
	}
}
// *** *** ***


