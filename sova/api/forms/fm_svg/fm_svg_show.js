window.sovaActions = window.sovaActions || {};
window.sovaActions.fm_svg = {
    init: doc => {
            const webSocket = new WebSocket(`ws://${doc.getField('webSocketServer')}/${doc.unid}/${window.jsDoc.userName}`);
            webSocket.onopen = _ => webSocket.send("Hello Web Socket!");
            webSocket.onmessage = e => {
                if (e.data) {
                    if ( e.data.includes(', "editMode": "1"') )
                        doc.rsMode = 'edit';
                    doc.setField( 'show', e.data, Math.random() );
                    setTimeout(_ => window.countdown(), 500);
                }
            };
            webSocket.onclose = e => console.log(e.data);
    },

    init2: doc => window.countdown(),

};

// *** *** ***
