#!/usr/bin/env python
#coding=utf-8
import sys
sys.path.append('../')
from common.xec_tcpsvr import *
from common.logger import *
import socket
import md5
import uuid

# code

listen_host = ''
listen_port = 0

class LogonServerHandler(SocketServer.StreamRequestHandler):
    
    def __init__(self, request, client_address, server):
        self.timeout = 2
        self.disable_nagle_algorithm = True
        SocketServer.StreamRequestHandler.__init__(self, request, client_address, server)
    
    # verify version
    def auth_version(self):
        version = self.rfile.read(2)
                    
        ret = (version == '\x00\x01')
        if not ret:
            logger(__file__, 'unknow version %d.%d' % (ord(version[1]), ord(version[0])))  
        else:
            logger(__file__, 'check version %d.%d' % (ord(version[1]), ord(version[0]))) 
            
        return ret
    
    def auth_logonuser(self, username, password):
        '''验证用户名和密码是否合法'''
        self.db_host = read_conf_file('logonServer', 'dbsvr_host')
        self.db_port = int(read_conf_file('logonServer', 'dbsvr_port'))
        
        self.dbconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dbconn.settimeout(2)

        self.dbconn.connect((self.db_host, self.db_port))
        self.dbconn.send('LOGON%-32s%-32s' % (username, password))
        self.uid = self.dbconn.recv(5)
        self.dbconn.close()
        
        return (self.uid != 'FAILD' and self.uid != None)  
    
    def make_session_key(self):
        '''生成 session key'''
        return uuid.uuid1().get_hex()
    
    def put_session_to_server(self, session, usr, pwd):
        '''发送 session 到服务器'''
        data = 'PUTSS%-32s%-32s%-32s' % (session, usr, pwd)  
        
        self.db_host = read_conf_file('logonServer', 'sessionsvr_host')
        self.db_port = int(read_conf_file('logonServer', 'sessionsvr_port'))
        
        self.dbconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dbconn.settimeout(2)

        self.dbconn.connect((self.db_host, self.db_port))
        self.dbconn.send(data)
        ret = self.dbconn.recv(5)
        self.dbconn.close()
        
        return (ret == 'TRUE ')
        
    
    def handle(self):
            
        try:
            # verifier version
            if not self.auth_version():
                return
            
            logger(__file__, 'request accept : %s:%d' % (self.client_address[0], self.client_address[1]))
                
            # 验证账户密码
            usr = self.rfile.read(32).strip()
            pwd = self.rfile.read(32).strip()
            if not self.auth_logonuser(usr, md5.new(pwd).hexdigest()):
                return
            
            # make session key
            session_key = self.make_session_key()               
            
            # put sesssion key to main server
            self.put_session_to_server(session_key, usr, pwd)
            
            # send session, chat server to client
           
            logger(__file__, 'requect process finish')

        except Exception, err:
            self.request.close()
            logger(__file__, str(err).decode('gbk'))
                
        logger(__file__, 'requect close')
            
    def finish(self):
        logger(__file__, 'client disconnect...')

# global functions
def main():
    global listen_host
    global listen_port
    
    logger(__file__, 'Logon Server Starting....')
    
    # 读取配置文件
    listen_host = read_conf_file('logonServer', 'host')
    listen_port = int(read_conf_file('logonServer', 'port'))
    
    start_listen_thread(LogonServerHandler, listen_host, listen_port)
    logger(__file__, 'Logon Server Exit.')
        
if __name__ == '__main__':
    main()