// *** *** ***

let pi_3 = [0, -1*Math.PI/3, -2*Math.PI/3, -Math.PI, -4*Math.PI/3, -5*Math.PI/3, 0];
let _grad = Math.PI/180;
let [_d, _y, r, _u, _doc, _oPol, _setI, _cx, _cy, _u2] = [280, 75, 150, 0.0, null, null, null, 400, 400, 0];

let _selectedApp;

// *** *** ***

window.sovaActions = window.sovaActions || {};
window.sovaActions.react_py = {
    init: doc => {
        doc.fieldValues['SCREEN_FD'] = doc.util.anyMobile ? 's' : 'p';
        _selectedApp = doc.util.anyMobile ? 'BTN_APP_1' : 'BTN_APP1';
    },
	init2: doc => {
//		console.log(doc.util.anyMobile);
		_doc = doc;
		_oPol = JSON.parse(doc.getField('_polygon'));
                _oPol[0].attributes = _doc.util.anyMobile ?
                    {width: "820", height: "800", viewBox: "0 0 1640 1600"}
                    :
		    {width: "820", height: "800", viewBox: "0 0 1640 1600"};
		_oPol[0].children[0].children[0].attributes = {};
        if ( doc.getField('CHMODE_FD') === 'p' ) {
            doc.setField('polygon_fd', _oPol);
            _setI = setInterval( __, 25);
        }
	},
	
    //*** *** ***

    recalc: {
		CHMODE_FD: (doc, label) => {
            if (label === 'n') { // normal
                clearInterval(_setI);
                doc.setField('polygon_fd', null);
            }
            else {
                _setI = setInterval( __, 50);
            }
            doc.forceUpdate();
		},
        SCREEN_FD: (doc, newValue) => {
            doc.util.anyMobile = newValue !== 'p'; // p - значит компьютер
            runChApp(doc, doc.util.anyMobile ? '_1' : '1');
            doc.forceUpdate();
        },
    },
    
    // *** *** ***
   
    hide: {
        plain1: doc => doc.getField('CHMODE_FD') !== 'n' || _selectedApp > 'BTN_APP3' || doc.util.anyMobile,
        plain2: doc => doc.getField('CHMODE_FD') !== 'n' || _selectedApp <= 'BTN_APP3' || doc.util.anyMobile,
        
        plain_1: doc => doc.getField('CHMODE_FD') !== 'n' || _selectedApp > 'BTN_APP_3' || !doc.util.anyMobile,
        plain_2: doc => doc.getField('CHMODE_FD') !== 'n' || _selectedApp <= 'BTN_APP_3' || !doc.util.anyMobile,
        
        descr1: doc => doc.getField('CHMODE_FD') !== 'n' || _selectedApp != 'BTN_APP1' || doc.util.anyMobile,
        descr2: doc => doc.getField('CHMODE_FD') !== 'n' || _selectedApp != 'BTN_APP2' || doc.util.anyMobile,
        descr3: doc => doc.getField('CHMODE_FD') !== 'n' || _selectedApp != 'BTN_APP3' || doc.util.anyMobile,
        descr4: doc => doc.getField('CHMODE_FD') !== 'n' || _selectedApp != 'BTN_APP4' || doc.util.anyMobile,
        descr5: doc => doc.getField('CHMODE_FD') !== 'n' || _selectedApp != 'BTN_APP5' || doc.util.anyMobile,
        descr6: doc => doc.getField('CHMODE_FD') !== 'n' || _selectedApp != 'BTN_APP6' || doc.util.anyMobile,

        descr_1: doc => doc.getField('CHMODE_FD') !== 'n' || _selectedApp != 'BTN_APP_1' || !doc.util.anyMobile,
        descr_2: doc => doc.getField('CHMODE_FD') !== 'n' || _selectedApp != 'BTN_APP_2' || !doc.util.anyMobile,
        descr_3: doc => doc.getField('CHMODE_FD') !== 'n' || _selectedApp != 'BTN_APP_3' || !doc.util.anyMobile,
        descr_4: doc => doc.getField('CHMODE_FD') !== 'n' || _selectedApp != 'BTN_APP_4' || !doc.util.anyMobile,
        descr_5: doc => doc.getField('CHMODE_FD') !== 'n' || _selectedApp != 'BTN_APP_5' || !doc.util.anyMobile,
        descr_6: doc => doc.getField('CHMODE_FD') !== 'n' || _selectedApp != 'BTN_APP_6' || !doc.util.anyMobile,
        
        priz: doc => doc.getField('CHMODE_FD') !== 'n',
    },
    cmd: {
        app1: doc => runChApp(doc, '1'), app11: doc => runChApp(doc, '1'),
        app2: doc => runChApp(doc, '2'), app12: doc => runChApp(doc, '2'),
        app3: doc => runChApp(doc, '3'), app13: doc => runChApp(doc, '3'),
        app4: doc => runChApp(doc, '4'), app14: doc => runChApp(doc, '4'),
        app5: doc => runChApp(doc, '5'), app15: doc => runChApp(doc, '5'),
        app6: doc => runChApp(doc, '6'), app16: doc => runChApp(doc, '6'),

        app_1: doc => runChApp(doc, '_1'), app_11: doc => runChApp(doc, '_1'),
        app_2: doc => runChApp(doc, '_2'), app_12: doc => runChApp(doc, '_2'),
        app_3: doc => runChApp(doc, '_3'), app_13: doc => runChApp(doc, '_3'),
        app_4: doc => runChApp(doc, '_4'), app_14: doc => runChApp(doc, '_4'),
        app_5: doc => runChApp(doc, '_5'), app_15: doc => runChApp(doc, '_5'),
        app_6: doc => runChApp(doc, '_6'), app_16: doc => runChApp(doc, '_6'),
    }
};

let runChApp = (doc, s) => {
    doc.setField(_selectedApp, {className: 'nosel'});
    doc.setField('BTN_APP' + s, {className: 'sel'});
    _selectedApp = 'BTN_APP' + s;
    doc.forceUpdate();
}
// *** *** ***

let _priz = ugr => {
	_oPol[0].attributes = _doc.util.anyMobile ?
		{width: "820", height: "800", viewBox: "0 0 1640 1600"}
		:
		{width: "820", height: "800", viewBox: "0 0 1640 1600"};
	
	if (_y > 0) _y -= _y > 1 ? 1 : 0.12;
	 {
		if (r > 45) {
			_d -= 2;
			r--;
		}
	}

    let ls = [];
    let [x1, y1, x11, y11] = [ [], [], [], [] ];
    let ug = ugr*_grad;

	pi_3.forEach( (u, i) => {
        let [x,y] = [Math.cos(u+ug), Math.sin(u+ug)];
        [x1[i], y1[i]] = [0.87*(x-y), 0.25*(-x-y)];
		if (_y > 0) {
			[x,y] = [Math.cos(-u-ug), Math.sin(-u-ug)];
			[x11[i], y11[i]] = [0.87*(-x+y), 0.25*(x+y)];
		}
	});

	if (_y <= 0)
		[x11, y11] = [x1, y1];

    for (let i = 0; i < 6; i++) {
        ls[i+6] = [_cx+r*x1[i], _cy+r*y1[i]-_y, _cx, _cy-_d-_y, _cx+r*x1[i+1], _cy+r*y1[i+1]-_y, `rgba(176,${255*6*0.0},${255*6*0.0}, ${0.7})`, '#faa'];
		rand = Math.random() / 10.;
		ls[i]   = [_cx+r*x11[i], _cy+r*y11[i]+_y, _cx, _cy+_d+_y, _cx+r*x11[i+1], _cy+r*y11[i+1]+_y, `rgba(176,${255*6*0.15},${255*6*0.15}, ${0.7})`, '#fff'];
//		ls[i]   = [_cx+r*x1[i], _cy+r*y1[i]+y, _cx, 680+y, _cx+r*x1[i+1], _cy+r*y1[i+1]+y, 'rgba(0,35,74, ${0.7})'];

	}
	return ls;
};

// *** *** ***

const __ = _ => {
    if ( !_oPol )
        return;
	let ls = _priz(_u);
	let ir = 4 + Math.floor((_u+25.)/60.);
	let ib = 4 + Math.floor((_u-(_y > 0 ? 90. : 0))/60.);
	if ( ir >= 6 )
		ir -= 6;

	if ( ib >= 6 )
		ib -= 6;

	if ( r <= 45 ) {
		_sec = 0;
		_u2 -= _doc.util.anyMobile ? 0.2 : 0.1;
		if (_u2 <= -360)
			u2 = 0;
		_oPol[0].children[0].children[0].attributes.transform = `rotate(${_u2} ${_cx} ${_cy})`
	}
	
	_oPol[0].children[2].children.forEach( (it,j) => {
		let i = j;
		if ( j < 6 ) {
			i += ib;
			if ( i >= 6 )
				i -= 6;
		}
		else {
			i += ir;
			if ( i >= 12 )
				i -= 6;
		}
		it.attributes.points = `${ls[i][0]},${ls[i][1]} ${ls[i][2]},${ls[i][3]} ${ls[i][4]},${ls[i][5]}`;
		it.attributes.fill = ls[i][6];
		it.attributes.stroke = ls[i][7];
	});
	_doc.setField('polygon_fd', _oPol, 0);
	_u += 0.5;
	if (_u >= 360)
		_u = 0.0;
	if ( r <= 45 ) {
		clearInterval(_setI);
		_setI = setInterval( __, 50);
	}
	else
		_u += 1;
}

















