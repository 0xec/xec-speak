#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-4-21
@author: xec
'''
import SocketServer
import ConfigParser
from logger import *

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
        version = self.request.recv(2)
        ret = (version == '\x00\x01')
        if not ret:
            logger('unknow version %d.%d' % (ord(version[1]), ord(version[0])))   
            
        return ret
    
    def auth_logonuser(self, username, password):
        
        return True
    
    
    def handle(self):
        try:
            logger('request accept : %s:%d' % (self.client_address[0], self.client_address[1]))
        
            # verifier version
            if not self.auth_version():
                return 
                
            # 验证账户密码
            usr = self.request.recv(32);
            pwd = self.request.recv(32);
            
            if not self.auth_logonuser(usr, pwd):
                return
            
            
            

        except Exception, err:
            logger(str(err).decode('gbk'))
        
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

# global functions


def read_conf_file():
    global listen_host
    global listen_port
    
    cf = ConfigParser.ConfigParser()
    cf.read(config_file)
    listen_host = cf.get('config', 'host')
    listen_port = cf.getint('config', 'port')

def start_listen_thread():
    global server
    
    # read config file
    read_conf_file()
    
    logger('Logon Server Work ' + listen_host + ':' + str(listen_port))
    
    # start listen socket
    try:
        server = ThreadedTCPServer((listen_host, listen_port), LogonServerHandler)
        server_thread = threading.Thread(target = server.serve_forever)
        server_thread.setDaemon(True)
        server_thread.start()
        server.serve_forever()
    except Exception, data:
        error = str(data)
        logger(error.decode('gbk'))
        
if __name__ == '__main__':
    logger('Logon Server Starting....')
    start_listen_thread()
    logger('Logon Server Exit.')