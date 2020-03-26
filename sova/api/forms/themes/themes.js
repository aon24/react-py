// *** *** ***
var _readyList = [];
var _rogDC = {};
var _filt_ = '';
var _filt1P = '';
var _filt2T = '';

window.sovaActions = window.sovaActions || {};
window.sovaActions.themes = {

	init2: doc => {
		if ( _readyList.length === 0 )
			fetch(doc.getField('readyListUrl'), {method: 'get', credentials: 'include'})
				.then( response => response.text() )
				.then( txt => {
					doc.setField('rog', txt);
					_readyList = (txt.slice(1, -1) + ',').split('\n');

				})
				.catch( err => doc.setField('rog', err.message) );
		if ( Object.keys(_rogDC).length === 0 )
			doc.util.jsonByUrl(doc.getField('readyDCUrl'))
				.then( jsn => _rogDC = jsn)
				.catch ( mess => console.error('rogDC.js: doc.util.jsonByUrl:' + mess) );
	},
	
    //*** *** ***
  
    recalc: {
        DLGPART: (doc, label, opt, i) => {
			_filt1P = opt;
			_filt2T = '';
			window.sovaActions.themes.cmd.setFilter(doc, _filt_);
			doc.setField( 'dlgTheme', '' );

			if (opt)
                doc.util.jsonByUrl('list?rgThemeList' + opt)
					.then( jsn => doc.changeDropList('dlgTheme', jsn || []))
					.catch ( mess => console.error('themes.js: doc.util.jsonByUrl:' + mess) );
            else
                doc.changeDropList( 'dlgTheme', [] );
        },
		
		DLGTHEME: (doc, label, opt, i) => {
			_filt2T = label ? '.00' + label.slice(0, 2) : '';
			window.sovaActions.themes.cmd.setFilter(doc, _filt_);
		}
    },
    
    // *** *** ***
    
    cmd: {
        clsDlg: doc => console.log('clsDlg'),
		
        setFilter: (doc, filt) => { // в питоне указано onEnter='setFilter', в классе Text: Util.runCmd(this.props.doc, this.props.onEnter, this.state.text, e.ctrlKey);
			let f = filt.toLowerCase().trim();
			_filt_ = f;
			let ls = _readyList;
			let f1, f2;
			
			if (f) {
				if ( parseInt(f, 10) ) {
					f = '=' + ('000' + f).slice(-4) + '=';
					ls = ls.filter( it => it.includes(f) );
				}
				else {
					if (f.includes('*')) {
						[f1, f2] = doc.util.partition(f, '*');
						ls = ls.filter( it => it.toLowerCase().includes(f1.trim()) || it.toLowerCase().includes(f2.trim()));
					}
					else if (f.includes(' ')) {
						[f1, f2] = doc.util.partition(f, ' ');
						ls = ls.filter( it => it.toLowerCase().includes(f1.trim()) && it.toLowerCase().includes(f2.trim()));
					}
					else
						ls = ls.filter( it => it.toLowerCase().includes(f) );
				}
			}
			if ( _filt1P )
				ls = ls.filter( it => it.toLowerCase().includes(_filt1P + _filt2T) )
			doc.setField('rog', '[' + ls.join(' ').slice(0, -1) + ']');
        },
        addAsk: (doc, unid) => {
			let o = _rogDC[unid];
			alert('Вопрос ' + o.RGCODE);
        },
		showAsk: (doc, unid) => {
			let o = _rogDC[unid];
			let text = `Раздел: ${o.RGPART}\n\nТематика: ${o.RGTHEME}\n\nТема: ${o.RGSUBJ}\n\nВопрос: ${o.RGASK}`;
			if ( o.RGASK2 )
				text += `\n\nПодвопрос: ${o.RGASK2}`;
			text += `\n\nТематический блок АКК: ${o.RGAKK}`;
			
			doc.msg.box(text, title='Вопрос ' + o.RGCODE, buttons=['Добавить+|Y', 'Отмена'], style=null)
				.then( _ => window.sovaActions.themes.cmd.addAsk(doc, unid) )
				.catch(_ => {});
		},
    }
};





















