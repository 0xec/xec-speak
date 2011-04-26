#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-4-21
@author: xec
'''
import SocketServer
from common.xec_tcpsvr import *
from common.logger import *

config_file = 'config.conf'

# code

listen_host = ''
listen_port = 0
server = []

class LogonServerHandler(SocketServer.StreamRequestHandler):
    
    def __init__(self, request, client_address, server):
        self.timeout = 2
        self.disable_nagle_algorithm = True
        SocketServer.StreamRequestHandler.__init__(self, request, client_address, server)
    
    # verify version
    def auth_version(self):
        version = self.rfile.read(2)
        print len(version)
        for i in range(0, len(version)):
            print version[i]
        ret = (version == '\x00\x01')
        if not ret:
            logger('unknow version %d.%d' % (ord(version[1]), ord(version[0])))  
        else:
            logger('check version %d.%d' % (ord(version[1]), ord(version[0]))) 
            
        return ret
    
    def auth_logonuser(self, username, password):
        
        return True
    
    
    def handle(self):
       
        while True:
            
            logger('request accept : %s:%d' % (self.client_address[0], self.client_address[1]))
            
            try:
                # verifier version
                if not self.auth_version():
                    #return 
                    pass
                    
                # 验证账户密码
                usr = self.rfile.read(32)
                pwd = self.rfile.read(32)
                
                if not self.auth_logonuser(usr, pwd):
                    return
                
                # make session key
                
                # put sesssion key to main server
                
                # send session, chat server to client
               
                logger('requect process finish')

            except Exception, err:
                logger(str(err).decode('gbk'))
            
    def finish(self):
        print 'finish'

# global functions
def main():
    logger('Logon Server Starting....')
    start_listen_thread(LogonServerHandler, '', 5000)
    logger('Logon Server Exit.')
        
if __name__ == '__main__':
    main()