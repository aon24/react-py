// *** *** ***

window.showRooms = [];
window.loadAndShowRooms = (doc, noLoad, t1, t2) => {
    Object.keys(doc.register).forEach( xName => {
        let room = doc.register[xName];
        if ( room.props.showCol === doc.getField('show_FD') ) {
            if ( room.rType === (t1 || room.rType) || room.rType === (t2 || room.rType) ) {
                room.noLoad = noLoad;
                window.showRooms[parseInt(doc.util.partition(xName, '_')[1])] = true;
            }
            else
                window.showRooms[parseInt(doc.util.partition(xName, '_')[1])] = false;
        }
    });
    doc.setState({class_fd: null});
};

window.sovaActions = window.sovaActions || {};
window.sovaActions.schedule = {
    init: doc => doc.fieldValues['SCREEN_FD'] = doc.util.anyMobile ? 's' : 'p',
    
    // *** *** ***
    recalc: {
        SCREEN_FD: (doc, newValue) => {
            doc.util.anyMobile = newValue !== 'p'; // p - значит компьютер
            doc.forceUpdate();
        }
    },
  
    cmd: {
        delHour: (doc, id) => {
            if (!confirm('Удалить заказ ?'))
                return;

            // через 1.0с включить "Загрузка", если waitLoad=true
            setTimeout( _ => doc.waitLoad ? doc.setState({spinner: true}) : 0, 500 );
            let url = 'api.get?delHour&' + id;
            fetch(url, { method: 'get', credentials: 'include' } )
                .then( _ => {
                    doc.waitLoad = false;
                    doc.setState( {spinner: false} );
                    window.sovaActions.schedule.cmd.myHours(doc);
                })
                .catch( e => {
                    doc.setState( {spinner: false} );
                    doc.waitLoad = false;
                    console.log(`ERROR in shedule.js\nUrl:${url}\n` + e);
                });                
        },
        myHours: doc => {
            doc.setField('myHours', '');
            if ( !doc.getField('date1_fd') )
                return;
            // через 1.0с включить "Загрузка", если waitLoad=true
            setTimeout( _ => doc.waitLoad ? doc.setState({spinner: true}) : 0, 500 );

            let url = `api.get?myHours&${doc.getField('date1_fd')}&${doc.getField('date2_fd')}`;
            fetch(url, { method: 'get', credentials: 'include' } )
                .then( resp => resp.text() )
                .then( tx => {
                    doc.setField('myHours', tx);
                    doc.waitLoad = false;
                    doc.setState( {spinner: false} );
                })
                .catch( e => {
                    doc.setState( {spinner: false} );
                    doc.waitLoad = false;
                    console.log(`ERROR in shedule.js\nUrl:${url}\n` + e);
                });
        },
        
        
        loadRoom: (doc, cell) => {
            cell.noLoad = false;
            doc.forceUpdate();
        },
        
        
        chDate: doc => {
            let date_fd = doc.getField('date_fd');
            if ( !date_fd )
                return;
            let [yy, mm, dd] = date_fd.split('-');
            let dKey = `${parseInt(mm)}_${yy}`;
            Object.keys(doc.register).forEach( xName => {
                let room = doc.register[xName];
                if (room.dKey) {
                    if ( dKey === doc.util.partition(room.dKey, '_')[1] ) {
                        doc.setField('show_FD', room.props.showCol);
                        room.noLoad = false;
                        window.showRooms[parseInt(doc.util.partition(xName, '_')[1])] = true;
                    }
                    else {
                        window.showRooms[parseInt(doc.util.partition(xName, '_')[1])] = false;
                        //room.noLoad = true;
                    }
                }
            });
            doc.setState({class_fd: 'shCol'});
        },
        
        m:  doc => window.loadAndShowRooms(doc, true, 'M', 1),
        ml: doc => window.loadAndShowRooms(doc, false, 'M',1),
        s:  doc => window.loadAndShowRooms(doc, true, 'S', 1),
        sl: doc => window.loadAndShowRooms(doc, false, 'S',1),
        ms: doc => window.loadAndShowRooms(doc, true, 'M', 'S'),
        msl:doc => window.loadAndShowRooms(doc, false, 'M', 'S'),
        al: doc => window.loadAndShowRooms(doc, false, 0, 0),
        b:  doc => window.loadAndShowRooms(doc, true, 'B',1),
        bl: doc => window.loadAndShowRooms(doc, false, 'B',1),
    },
    // *** *** ***

    hide: {
        btnbook: doc => !doc.state.class_fd,
    },
};

for ( let i = 1; i <= 150; i++)
    window.sovaActions.schedule.hide[`sch_${i}`] = _ => !window.showRooms[i];





