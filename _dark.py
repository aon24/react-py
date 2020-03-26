# -*- coding: utf-8 -*- 
'''
Created on 9 apr. 2017

@author: aon
'''
from sova.util.first import dbg, snd, err

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import socket
import urllib.parse
import sys
import platform
import threading

# *** *** ***

try:
    import importlib
    resource = importlib.import_module('resource')
    resource.setrlimit(resource.RLIMIT_NOFILE, (100000, 100000))
except:
    pass

# *** *** ***

wsgiApplication = None
versionString = 'HTTP Sova.online/3.2.1 Python/%s(%s) %s/%s' % (
            sys.version.split()[0], sys.platform,
            platform.system(), platform.release())

# *** *** ***

class SovaHttpServer(ThreadingMixIn, HTTPServer):
    def __init__(self, addr, handler):
        HTTPServer.__init__(self, addr, handler)
        
    def server_activate(self):
        self.socket.settimeout(30) # таймаут ответа клиента
        self.socket.listen(256) # по умолчанию 5, в торнадо 128
        
        socket._blocking_errnos.add(10053)  # блокировка ошибки разрыва соединения

# *** *** ***

class wsgiRH(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    
    def log_message(self, frmat, *args):
        dbg('addr %r, %s' % (self.client_address, frmat % args), cat='http-server')
    
    def log_error(self, frmat, *args):
        err( 'addr %r, %s' % (self.client_address, frmat % args), cat='error-http-server' )
        
    def version_string(self):
        return versionString

    def get_environ(self):
        env = dict(
            SERVER_SOFTWARE = 'WsgiSovaServer/1.0',
            SERVER_PROTOCOL = self.request_version,
            REQUEST_METHOD = self.command,
            REMOTE_ADDR = self.client_address[0],
            CONTENT_TYPE = self.headers.get('content-type', self.headers.get_content_type()),
            )
        env['wsgi.input'] = self.rfile
        env['wsgi.version'] = (1, 0)
        env['wsgi.errors'] = sys.stderr
        env['wsgi.multithread'] = True
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once'] = False

        path, _, query = self.path.partition('?')

        env['PATH_INFO'] = urllib.parse.unquote(path, 'iso-8859-1')
        env['QUERY_STRING'] = query
        
        host = self.address_string()
        if host != self.client_address[0]:
            env['REMOTE_HOST'] = host

        length = self.headers.get('content-length')
        if length:
            env['CONTENT_LENGTH'] = length

        for k, v in self.headers.items():
            k = k.replace('-', '_').upper()
            v = v.strip()
            if k not in env:
                if 'HTTP_' + k in env:
                    env['HTTP_' + k] += ',' + v
                else:
                    env['HTTP_' + k] = v
                
        return env

    # *** *** ***

    def handle_one_request(self):
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(HTTPStatus.REQUEST_URI_TOO_LONG)
                return
            if not self.raw_requestline:
                self.close_connection = True
                return
            if not self.parse_request():
                return

            result_iter = wsgiApplication(self.get_environ(), self.start_response) # run WSGI-application
            if result_iter:
                for data in result_iter:
                    self.wfile.write(data)
                    self.wfile.flush()

        except Exception as ex:
            self.log_error('svServer.py.handle_one_request: %r', ex)
            self.close_connection = True

    # *** *** ***

    def start_response(self, status, response_headers):
        try:
            st, _, mess = status.partition(' ')
            self.send_response(int(st), mess or None)
            
            for rh in response_headers:
                self.send_header(*rh)
            
            self.end_headers()
            
        except Exception as ex:
            self.log_error('svServer.py.start_response: %r', ex)
            self.close_connection = True

# *** *** ***
if __name__ == '__main__':
    import sovaApp
    wsgiApplication = sovaApp.application
    port = 8081

    server = SovaHttpServer(('', port), wsgiRH)
    threading.Thread(target = server.serve_forever).start()
    snd(f'''HTTP WSGI server started
=== === === {versionString}
=== === === server_address: {server.server_address}
=== === === Application: "sovaApp.application"''', cat='Start')
   
# *** *** ***

