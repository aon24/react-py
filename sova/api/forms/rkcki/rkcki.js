// *** *** ***

window.sovaActions = window.sovaActions || {};
window.sovaActions.rkcki = {
    init: doc => {
        return; // № 1548-ТО от 24.08.2018 Просьба по умолчанию блок "Сопроводительное письмо" для "СД-Ответ на ОГ" сделать раскрытым
        
        doc.fieldValues['HIDECOVER.FD'] = doc.fieldValues.BODYPRN ? '' : '1';

        for ( let fi in doc.fieldValues )
            if ( fi.startsWith('FILES2_') )
                doc.fieldValues['HIDECOVER.FD'] = '';
    },
	// *** *** ***
  
    recalc: {
        TEMPLATE_2: (doc, value) => getTemplateText(doc, value),
        DEPNAME: (doc, value, alias) => doc.changeDropList('WHO', alias),
        'HIDECOVER.FD': (doc, value) => {
            if ( !value )
                return doc.forceUpdate();
            if ( doc.getField('BODYPRN') || doc.fileShow['FILES2_'].hasAtt() )
                return setTimeout( _ => doc.setField('HIDECOVER.FD', 0), 100);
            doc.forceUpdate();
        },
    },

    //**********
  
    hide: {
        cover: doc => doc.getField('hideCover.FD'),
    },

  //**********
  
    validate: {
        hist: doc => {
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
        form: doc => new Promise( (yes, no) => {
            if ( doc.getField('email') && !doc.getField('smtpSentOK') ) {
                let att = doc.fileShow['FILES1_'].hasAtt();
                if ( att ) { // есть вложения, включая несохраненные
                    let mess = `Адрес: ${doc.getField('email')}\n\n` + 
                        'Тема письма: Ответ на Ваше обращение ' +
                        `${doc.getField('GROUNDS').split('|')[0].replace(/ /, ' от ')}\n\n` +
                        'Текст письма: Информация во вложении.\n\n' +
                        `Вложение: ${att}\n\n`;
                        
                    doc.msg.box(mess,
                        'Подтвердите отправку|Отправить ответ с вложениями на указанный адрес электронной почты?', ['Да+|Y', 'Нет|N', 'Отмена'],
                        {color: '#c00'}
                    )
                        .then( yn => {
                            if ( yn === 'Y' ) {
                                doc.setField('FORSEND', '1');       
                                doc.setField('EMAILPOSTING', '1');
                            }
                            yes();
                        })
                        .catch ( _ => no() );
                }
                else
    // 1353-ТО от 23.11.2017 проверить наличие вложения перед предложением отправки документа на e-mail.
                    doc.msg.box('\nПоле E-MAIL заполнено, но вложение отсутствует.\n\nСохранить без отправки ответа на E-MAIL ?',
                            'Подтвердите сохранение',
                            ['Сохранить+|Y', 'Отмена'])
                        .then( _ => yes() )
                        .catch ( _ => no() );
            }
            else
                yes();
            }),
    },
  
    // *** *** ***
};



