#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append('../')
import SocketServer
from common.xec_tcpsvr import *
from common.logger import *

listen_host = ''
listen_port = 0

class SessionServer(SocketServer.StreamRequestHandler):
    
    def __init__(self, request, client_address, server):
        self.timeout = 2
        self.disable_nagle_algorithm = True        
        SocketServer.StreamRequestHandler.__init__(self, request, client_address, server)
        
        
    def handle(self):                
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