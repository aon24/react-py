window.sovaActions = window.sovaActions || {};
window.sovaActions.fm_svg = {
    init: doc => {
        let elemT = window.document.getElementsByTagName('title')[0];
        elemT.innerHTML = doc.getField('title');
    },
    
    // *** *** ***
    hide: {
    	cmInsert: doc => !doc.contextMenu,
		dlgProps: doc => doc.dlgOpen !== 'dlgProps',
    },
	// *** *** ***
    cmd: {
		contextMenu: (doc, p) => {
			doc.contextMenu = !doc.contextMenu;
			doc.contextBox = p.box;

			let ctm = p.dom.getScreenCTM();
			let pt = p.dom.createSVGPoint();
			pt.x = p.event.clientX;
			pt.y = p.event.clientY;
			pt = pt.matrixTransform(ctm.inverse());

			let st = doc.register.CMINSERT_FD.dom.current.style;

			let wh = window.innerHeight;
			let ww = window.innerWidth;

			let y = (wh - pt.y) > 200 ? pt.y : (pt.y - 170);
			let x = (ww - pt.x) > 240 ? pt.x : (pt.x - 200);

			st.top = y + 'px';
			st.left = x + 'px';

			doc.setField('cmInsert_FD', -1);
			doc.forceUpdate();
		},
	// ***

		sendShow: (doc) => {
			let data = JSON.stringify(getShow(doc.mainSvg));
			if ( wsIsOpen ) {
				webSocket.send(data);
            }
			else {
				webSocket = new WebSocket('ws://' + doc.getField('webSocketServer') + '/' + doc.unid + '/' + window.jsDoc.userName);
				webSocket.onopen  = _ => {
					wsIsOpen = true;
					webSocket.send(data);
				};
				webSocket.onclose = _ => wsIsOpen = false;
				webSocket.onmessage = mess => console.log('webSocket message:', mess);
			}
		},
    },
	// *** *** ***

	recalc: {
		CMINSERT_FD: (doc, item, alias, i) => {
			doc.contextMenu = false;
			doc.forceUpdate();
            let sett = doc.contextBox.setting;
            if ( !(['div', 'form', 'span', 'b', 'i', 'p', 'ol', 'ul', 'a', 'label'].includes(sett.type) || doc.contextBox.id === 'main') )
                return doc.msg.box('You cannot insert a new item in this box');
            alias && doc.util.jsonByUrl('api.get?loadDropList&' + alias)
                .then( jsn => doc.msg.list(jsn, item, {}, true) )
                .then( un => un && doc.contextBox.appendChild(alias + '&' + un) )
                .catch( ex => {} );
        },
    },
    
    dialog: {
        init: dlg => {
            dlg.changeDropList('bgValue');
            dlg.changeDropList('subCat');
        },
    	recalc: {
            CAT:    (dlg, item, alias) => dlg.changeDropList('subCat'),
    		BGTYPE: (dlg, item, alias) => {
    				dlg.changeDropList('bgValue');
                    dlg.setField('bgValue', '');
                    dlg.forceUpdate();
                    dlg.setFocus('bgType');
    			},
            LABFIELD: dlg => dlg.forceUpdate(),
            AIMG: dlg => dlg.forceUpdate(),
            BTNTYPE: dlg => dlg.forceUpdate(),
    	},
        hide: {
            cls: dlg => dlg.getField('bgType') === 'video',
            label: dlg => !dlg.getField('labField'),
            aImg: dlg => dlg.getField('aImg') !== '<a>',
            subm: dlg => !dlg.getField('btnType'),
            cmdImg: dlg => dlg.getField('aImg') !== 'cmd',
        },
    },
};

// *** *** ***
// *** *** ***

let webSocket;
let wsIsOpen;

// *** *** ***

window.setSvgBoxProprty = (doc, contextBox) => {
    doc.contextMenu = false;
    let sett = contextBox.setting;
    let fi = {};
    let tit, dlgFi, elemT, moreButtons;
    let attr = ['id', 'type', 'name', 'br', 'className', 'style', 'text', 'position', 'notes', 's2', 'classic', 'btnType', 'cmd', 'param',
        'bgType', 'bgValue', 'title', 'src', 'aImg', 'editMode', '_doc_', 'paramKV', 'htmlAttr', 'submit',
        'labfield', 'fn', 'ft', 'dropList', 'label', 'labelClassName', 'labelStyle', 'ttaClassName', 'ttaStyle', 'dayD', 'href', 'target'];
    let attrPage =  ['cat', 'subcat', 'formName', 'title', 'javaScriptUrl', 'cssUrl', 'notes']
    let h = 500; //dlg height
    attr.forEach( k => fi[k] = sett[k] );
    if (contextBox.id === 'main') {
        elemT = window.document.getElementsByTagName('title')[0];
        fi.TITLE = elemT.innerHTML;
        attrPage.forEach( k => fi[k] = doc.getField(k) );
        tit = 'page property';
        dlgFi = 'pageProps_fd';
        moreButtons = 'pageMB_fd';
    }
    else {
        switch(sett.type) {
            case 'div':
                tit = 'div property';
                dlgFi = 'divProps_fd';
                moreButtons = 'divMB_fd';
                break;
            case 'a+':
                tit = '<a+> property';
                dlgFi = 'aTextProps_fd';
                moreButtons = 'aTextMB_fd';
                break;
            case 'img':
                tit = '<img> property';
                dlgFi = 'imgProps_fd';
                moreButtons = 'imgMB_fd';
                h = 460;
                break;
            case 'field':
                tit = 'field property';
                dlgFi = 'fieldProps_fd';
                moreButtons = 'fieldMB_fd';
                h = 610;
                break;
            case 'button':
                tit = 'button property';
                dlgFi = 'btnProps_fd';
                moreButtons = 'btnMB_fd';
                h = 440;
                break;
            case 'pyComponent':
                tit = 'component property';
                dlgFi = 'compProps_fd';
                moreButtons = 'svgMB_fd';
                h = 440;
                break;
            case 'svg':
                tit = 'SVG property';
                dlgFi = 'svgProps_fd';
                moreButtons = 'svgMB_fd';
                h = 460;
                break;
            default:
                tit = sett.type + ' property';
                dlgFi = 'tegProps_fd';
                moreButtons = 'tegMB_fd';
                h = 460;
                break;
        }
    }

    doc.dlg.show(
        tit,
        fi,
        { style: {width:600, top: '5%', height:h, overflow: 'hidden' },  //  стиль всего диалога
           buttons: ['Apply+|Y', 'Cancel'],
           cmButton: _ => {
                attr.forEach( k => sett[k] = doc.dlg.getField(k) );
                if (contextBox.id === 'main') {
                    elemT.innerHTML = doc.dlg.getField('title');
                    attrPage.forEach( k => doc.setField(k, doc.dlg.getField(k)) );
                }
                doc.util.runCmd(doc, 'sendShow');
                contextBox.forceUpdate();
                doc.setFocus('BTN_CLOSE');
                doc.forceUpdate();
           },
           cmCancel: _ => {doc.setFocus('BTN_CLOSE'); doc.forceUpdate();},
        },
        {width: 462, height: h-35}, // стиль области данных
        doc.getField(dlgFi) ? JSON.parse(doc.getField(dlgFi)) : `Props-dialog not defined for ${sett.type}`,
        null, null,
        doc.getField(moreButtons) ? JSON.parse(doc.getField(moreButtons)) : null,
    );
};
// *** *** ***

const getShow = (svgBox, parent) => {
    //console.log(svgBox);
    if (svgBox.id.startsWith('HL_') || svgBox.id.startsWith('VL_')) {
        parent[svgBox.id] = {};
        ['x1', 'y1', 'x2', 'y2'].forEach( it => parent[svgBox.id][it] = svgBox[it] );
        return 0;
    }

	let el = {
		attributes: {id: svgBox.id},
		setting: {...svgBox.setting},
	};
	
	['x', 'y', 'w', 'h'].forEach( it => {if (svgBox[it]) el.attributes[it] = svgBox[it]});

	if (svgBox.tree) {
		let ch = [];
		svgBox.tree.forEach( it => {
			let e = it.state && it.state.deleted ? null : getShow(it, el);
			e && ch.push(e);
		});
		if (ch.length)
			el.children = ch;
	}
	return el;
}

// *** *** ***

