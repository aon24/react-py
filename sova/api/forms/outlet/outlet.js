// *** *** ***

window.sovaActions = window.sovaActions || {};
window.sovaActions.outlet = {
    init: doc => {
        doc.fieldValues['HIDECOVER.FD'] = doc.fieldValues.BODYPRN ? '' : '1';

        for ( let fi in doc.fieldValues )
            if ( fi.startsWith('FILES2_') )
                doc.fieldValues['HIDECOVER.FD'] = '';
    },
	// *** *** ***
	
    hide: {
        cover: doc => doc.getField('hideCover.FD'),
		firstRes: doc => !doc.fieldValues.DLMAINRES_FD,
    },
  
    // *** *** ***

    recalc: {
        TEMPLATE_2: (doc, value) => getTemplateText(doc, value),
        DEPNAME: (doc, value, alias) => doc.changeDropList('WHO', alias),
        'HIDECOVER.FD': (doc, value) => {
            if ( value && (doc.getField('BODYPRN') || doc.fileShow['FILES2_'].hasAtt()) )
                return setTimeout( _ => doc.setField('HIDECOVER.FD', 0), 100);
            doc.forceUpdate();
        },
    },
    
    // *** *** ***

    validate: {
        hist: doc => {
            if ( !doc.getField('FINISH') )
                return;
    
            let sstu = ["Меры приняты", "Поддержано", "Разъяснено", "Оставлено без ответа автору", "Не поддержано", "Дан ответ автору"];
            let sstul = sstu.map( it => it.toLowerCase() );
            let hist = doc.getField('hist');
            let ls = hist.split('\n');
            
            if ( !hist )
                return 'Не заполнено поле "Отметки об исполнении".\n\nСписок для ССТУ:\n-------------\n"' + sstu.join('"\n"') + '"';
            
            if ( !doc.getField('sstu') )
                return; // OK
            
            if ( !ls.filter( it => sstul.includes(it.trim().toLowerCase()) ).length )
                return 'Для выгрузки на ССТУ не выбраны нужные значения:\n\n"' + sstu.join('"\n"') + '"';
    
            if ( hist.toLowerCase().includes('оставлено без ответа автору') )
                return;
            
            if ( !doc.fileShow['FILES1_'].hasAtt() && !doc.dbAlias.startsWith('RF.AKK.MOKRASG.') )
                return 'Для выгрузки на ССТУ\nнеобходимо присоединить файл\n(секция "Ответ заявителю").\n' + 
                        '\nФайлы из секции\n"Сопроводительное письмо"\nна ССТУ не выгружаются.';
        },
        
        // *** *** ***
        
        form: doc => new Promise( (yes, no) => {
			let ls = doc.getField('DLDOCDA_FD').split('-');
            let docDa = +new Date(ls[0], +ls[1] - 1, ls[2]);
            
            ls = doc.getField('CLSDA').split('-');
            let clsDa = +new Date(ls[0], +ls[1] - 1, ls[2]);

			if( clsDa-docDa < 30*1000*3600*24 )
                return yes();
			
            doc.msg.box('\nВнимание!\n\nПроизошел выход за пределы 30 дневного срока исполнения.\nВы можете изменить дату закрытия в соответствии с ч.2 ст.12 Федерального закона от 02.05.2006 № 59-ФЗ',
                        'Предупреждение', ['Сохранить+|Y', 'изменить'])
                    .then( yes )
                    .catch( no );
        }),
    },
    // *** *** ***
};

