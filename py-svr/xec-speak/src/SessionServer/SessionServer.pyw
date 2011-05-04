#!/usr/bin/env python
#coding=gbk

import sys
sys.path.append('../')
from common.xec_tcpsvr import *
from common.logger import *
from common.frame import *
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
        
    def put_session(self, req_info):
        global session_list
        
        session_key = req_info['session']
        username    = req_info['usr']
        password    = req_info['pwd']
        
        logger(__file__, 'put session [%s:%s:%s]' % (session_key, username, password))
        
        session_item = {};
        session_item['key'] = session_key
        session_item['usr'] = username
        session_item['pwd'] = password
        
        session_list[session_key] = session_item
        
    def query_session(self, req_info, rep_info):
        
        session_key = req_info['session']
        logger(__file__, 'query session [%s]' % (session_key))
        
        if not session_list.has_key(session_key):
            return False
        if session_key != session_list[session_key]['key']:
            return False
        
        session_item = session_list[session_key]
        rep_info['Username'] = session_item['usr']
        
        return True
        
    def handle(self):  
        
        data = self.request.recv(1024)
        if data == None or len(data) == 0:
            return
            
        req_info = json_dec.decode(data)
        
        rep_info = {}
        
        if req_info['Request'] == 'put_session':         # 添加session到list
            self.put_session(req_info)
            
            rep_info['Response'] = True
            
        elif req_info['Request'] == 'query_session':
            
            if self.query_session(req_info, rep_info):
                rep_info['Response'] = True
            else:
                rep_info['Response'] = False
            
        else:
            pass
           
        data = json_enc.encode(rep_info)
        self.request.send(data)           
        logger(__file__, 'requect close')
            
    def finish(self):
        logger(__file__, 'client disconnect...')
        
def main():
    global listen_host
    global listen_port
    
    show_frame('Session Server')
    
    logger(__file__, 'Session Server Starting....')         # 日志
    
    # 读取配置文件
    listen_host = read_conf_file('SessionServer', 'host')
    listen_port = int(read_conf_file('SessionServer', 'port'))
    
    start_listen_thread(SessionServer, listen_host, listen_port)
    
    main_loop()
    
    logger(__file__, 'Session Server Exit.')

if __name__ == '__main__':
    main()