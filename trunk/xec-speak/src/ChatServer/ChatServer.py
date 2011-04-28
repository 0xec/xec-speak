#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append('../')
import SocketServer
import socket
from common.xec_tcpsvr import *
from common.logger import *
import json

json_enc = json.JSONEncoder()
json_dec = json.JSONDecoder()

listen_host = ''
listen_port = 0

session_list = {}

class SessionServer(SocketServer.StreamRequestHandler):
    
    def __init__(self, request, client_address, server):
        self.disable_nagle_algorithm = False        
        SocketServer.StreamRequestHandler.__init__(self, request, client_address, server)
    
    def check_session(self, session_key):
        info = {}
        info['Request'] = 'query_session'
        info['session'] = session_key
        
        data = json_enc.encode(info)
                
        session_host = read_conf_file('logonServer', 'sessionsvr_host')
        session_port = int(read_conf_file('logonServer', 'sessionsvr_port'))
        
        session_svr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        session_svr.settimeout(2)

        session_svr.connect((session_host, session_port))
        session_svr.send(data)
        data_response = session_svr.recv(1024)
        session_svr.close()
                
        rep = json_dec.decode(data_response)
        
        return (rep['Response'] == True)
        
        
    def handle(self):  
        
        while True:
            try:
                data = self.request.recv(1024)
                if data == None or len(data) == 0:
                    return
                
                req_info = json_dec.decode(data)
                rep_info = {}

                if req_info.has_key('Session') == False:
                    rep_info['Response'] = False
                    rep_info['info'] = 'no session'
                    
                else:      
                    
                    if self.check_session(req_info['Session']):
                              
                        if req_info['Request'] == 'Broadcast':   # 请求命令
                            pass                            
                        else:
                            pass
                    
                    else:
                        rep_info['Response'] = False
                        rep_info['info'] = 'session error'
                    
                    
                data = json_enc.encode(rep_info)
                self.request.send(data)
    
            except Exception, err:
                self.request.close()
                logger(__file__, str(err).decode('gbk'))
                break
            
        # end while
            
    def finish(self):
        logger(__file__, 'client disconnect...')
        
def main():
    logger(__file__, 'Chat Server Starting....')         # 
    
    # 
    listen_host = read_conf_file('ChatServer', 'host')
    listen_port = int(read_conf_file('ChatServer', 'port'))
    
    start_listen_thread(SessionServer, listen_host, listen_port)
    logger(__file__, 'Chat Server Exit.')

if __name__ == '__main__':
    main()