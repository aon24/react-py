# -*- coding: utf-8 -*- 
'''
Created on 01 mar 2019.

@author: aon
'''
try:
    from toolsLC import err, snd
except:
    from .... util.first import snd, err
    
from . svgTools import parsePage

import asyncio
import websockets
import json
import time

# *** *** ***

_forDisplay = {}
_tm = time.time()

# *** *** ***

async def hello(websocket, path):
    global _tm, _forDisplay
    path = path.partition('::')[0]
    async for message in websocket:
        if message == 'Hello Web Socket!':
            _forDisplay[path] = _forDisplay.get(path, [])
            _forDisplay[path].append(websocket)
        elif path in _forDisplay:
            try:
                page = parsePage( json.loads(message) )
                m = json.dumps([page], ensure_ascii=False)
            except Exception as ex:
                err(f'{message}\n{ex!r}', cat='websocket-json')
                m = None

            loop = True
            while m and loop:
                loop = False
                for disp in _forDisplay[path]:
                    try:
                        await disp.send(m)
                    except Exception as ex:
                        _forDisplay[path].remove(disp)
                        snd(f'{disp.remote_address[0]}, all={len(_forDisplay)}', cat='WebSocket closed')
                        loop = True
                        break
        # Cleaning
        if time.time() - _tm > 600:
            _tm = time.time()
            remove = []
            for k, v in _forDisplay.items():
                if not v:
                    remove.append(k)
                    continue
                
                loop = True
                while loop:
                    loop = False
                    for con in v:
                        try:
                            await con.send('')
                        except Exception as ex:
                            v.remove(con)
                            snd(f'Cleaning: {con.remote_address[0]}, all={len(_forDisplay)}', cat='WebSocket closed')
                            loop = True
                            break

            for k in remove:
                del _forDisplay[k]
                snd(f'Cleaning: {k}', cat='WebSocket closed')
                
# *** *** ***

def wsServer(port):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    start_server = websockets.serve(hello, port=port)
    loop.run_until_complete(start_server)
    loop.run_forever()

# *** *** ***










