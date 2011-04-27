#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append('../')
import SocketServer
from common.xec_tcpsvr import *
from common.logger import *

listen_host = ''
listen_port = 0

session_list = {}

class SessionServer(SocketServer.StreamRequestHandler):
    
    def __init__(self, request, client_address, server):
        self.timeout = 2
        self.disable_nagle_algorithm = True        
        SocketServer.StreamRequestHandler.__init__(self, request, client_address, server)
        
    def put_session(self):
        global session_list
        
        session_key = self.rfile.read(32).strip()
        username    = self.rfile.read(32).strip()
        password    = self.rfile.read(32).strip()
        
        logger(__file__, 'put session [%s:%s:%s]' % (session_key, username, password))
        
        session_item = {};
        session_item['key'] = session_key
        session_item['usr'] = username
        session_item['pwd'] = password
        
        session_list[session_key] = session_item
        
    def query_session(self):
        
        session_key = self.rfile.read(32).strip()
        logger(__file__, 'query session [%s]' % (session_key))
        session_item = session_list[session_key]
        if session_item == None:
            return False
        if session_key != session_item['key']:
            return False
        
        return True
        
    def handle(self):  
        
        cmd = self.rfile.read(5)            # 命令
        
        if cmd == None or len(cmd) == 0:
            return
        
        if cmd.startswith('PUTSS'):         # 添加session到list
            self.put_session()
            self.wfile.write('TRUE ')
            
        elif cmd.startswith('QUERY'):
            if self.query_session():
                self.wfile.write('TRUE ')
            else:
                self.wfile.write('FALSE')
        else:
            pass
                      
        logger(__file__, 'requect close')
            
    def finish(self):
        logger(__file__, 'client disconnect...')
        
def main():
    logger(__file__, 'Session Server Starting....')         # 日志
    
    # 读取配置文件
    listen_host = read_conf_file('SessionServer', 'host')
    listen_port = int(read_conf_file('SessionServer', 'port'))
    
    start_listen_thread(SessionServer, listen_host, listen_port)
    logger(__file__, 'Session Server Exit.')

if __name__ == '__main__':
    main()