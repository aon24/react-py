window.sovaActions = window.sovaActions || {};
window.sovaActions.countdown = {init2: doc => window.countdown()};
window.countdown = _ => {
    let cd = document.getElementById('countdown');
    if (!cd)
        return;

    let chil = cd.children;
    let dt = new Date();
    let border = new Date(dt.getFullYear(), dt.getMonth()+1, 1).getTime();
    let STEP = -30;

    let dls = [];
    let j, i, i2;
    let arr = [[9, 24 * 3600], [2, 3600], [5, 60], [5, 1]];
    let ls = [];
    for (i = 0; i < 4; i++) {
        let s = '<div>';
        for (j = 0; j <= arr[i][0]; j++)
            s += "<div> " + j + "</div>";
        chil[i * 2].innerHTML = s + '<div>0</div></div>';
        dls[i * 2] = chil[i * 2].children[0];
        s = '<div>';
        for (j = 0; j <= 9; j++)
            s += "<div> " + j + "</div>";
        chil[i * 2 + 1].innerHTML = s + '<div>0</div></div>';
        dls[i * 2 + 1] = chil[i * 2 + 1].children[0];
    }
    let tm = [
      _ => {dls[0].removeAttribute('notrans'); dls[0].style.marginTop = 9 * STEP + 'px';},
      _ => {dls[1].removeAttribute('notrans'); dls[1].style.marginTop = 9 * STEP + 'px';},
      _ => {dls[2].removeAttribute('notrans'); dls[2].style.marginTop = 2 * STEP + 'px';},
      _ => {dls[3].removeAttribute('notrans'); dls[3].style.marginTop = 9 * STEP + 'px';},
      _ => {dls[4].removeAttribute('notrans'); dls[4].style.marginTop = 5 * STEP + 'px';},
      _ => {dls[5].removeAttribute('notrans'); dls[5].style.marginTop = 9 * STEP + 'px';},
      _ => {dls[6].removeAttribute('notrans'); dls[6].style.marginTop = 5 * STEP + 'px';},
      _ => {dls[7].removeAttribute('notrans'); dls[7].style.marginTop = 9 * STEP + 'px';},
    ];
    setInterval( _ => {
        let o = (border - Date.now()) / 1000;
        for (i = 0, i2 = 0; i < 4; i++, i2 = i * 2) {
            let it = arr[i];
            let d = it[1];
            let v = parseInt(o / d);
            o %= d;
            let v1 = parseInt(v / 10);
            let v2 = v % 10;
            if (ls[i2] !== v1) {
                ls[i2] = v1;
                if (v1 === it[0]) {
                    dls[i2].setAttribute('notrans', 'true');
                    dls[i2].style.marginTop = (v1 + 1) * STEP + 'px';
                    setTimeout( tm[i2], 50);
                }
                else
                    dls[i * 2].style.marginTop = v1 * STEP + 'px';
            }
            i2++;
            if (ls[i2] !== v2) {
                ls[i2] = v2;
                if (v2 === 9) {
                    dls[i2].setAttribute('notrans', 'true');
                    dls[i2].style.marginTop = 10 * STEP + 'px';
                    setTimeout(tm[i2], 50);
                }
                else
                    dls[i2].style.marginTop = v2 * STEP + 'px';
            }
        }
    }, 1000);
};
