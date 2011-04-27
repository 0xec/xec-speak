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
        
    def handle(self):  
        
        cmd = self.rfile.read(5)            # 命令
        
        if cmd == None or len(cmd) == 0:
            return
        
        if cmd.startswith('PUTSS'):         # 添加session到list
            pass
            
        elif cmd.startswith('QUERY'):
            pass
        else:
            pass
                      
        logger(__file__, 'requect close')
            
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