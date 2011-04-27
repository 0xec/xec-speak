#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append('../')
import SocketServer
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
        self.timeout = 2
        self.disable_nagle_algorithm = True        
        SocketServer.StreamRequestHandler.__init__(self, request, client_address, server)
        
    def get_chat_rooms(self):
        
        rep = {}
        for i in range(1, 10):
            rep['client%d' % i] = {}
            rep['client%d' % i]['host'] = '127.0.0.1'
            rep['client%d' % i]['port'] = 8404
            
        return rep      
        
        
    def handle(self):  
        
        while True:
            try:
                data = self.request.recv(1024)
                if data == None or len(data) == 0:
                    return
                
                req_info = json_dec.decode(data)
                rep_info = {}
                
                if req_info['Request'] == 'ChatRoomList':
                    
                    rep_info = self.get_chat_rooms()
                    
                else:
                    pass
                    
                    
                data = json_enc.encode(rep_info)
                self.request.send(data)
               
                logger(__file__, 'db process finish')
    
            except Exception, err:
                self.request.close()
                logger(__file__, str(err).decode('gbk'))
        # end while
            
    def finish(self):
        logger(__file__, 'client disconnect...')
        
def main():
    logger(__file__, 'Hall Server Starting....')         # 日志
    
    # 读取配置文件
    listen_host = read_conf_file('HallServer', 'host')
    listen_port = int(read_conf_file('HallServer', 'port'))
    
    start_listen_thread(SessionServer, listen_host, listen_port)
    logger(__file__, 'Hall Server Exit.')

if __name__ == '__main__':
    main()