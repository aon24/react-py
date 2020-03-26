#!/usr/bin/env bash
cd /home/aon24/aon_2020/Sova/sova-online
npm run build
cp -f /home/aon24/aon_2020/Sova/sova-online/build/static/js/main.*.js   /home/aon24/aon_2020/AON/DpServer/api/react.js/sova-main.js
cp -f /home/aon24/aon_2020/Sova/sova-online/build/static/css/main.*.css /home/aon24/aon_2020/AON/DpServer/api/react.js/sova-main.css

