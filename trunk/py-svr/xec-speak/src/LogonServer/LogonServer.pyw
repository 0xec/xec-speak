#!/usr/bin/env python
#coding=gbk
import sys
sys.path.append('../')
from common.xec_tcpsvr import *
from common.logger import *
from common.frame import *
import socket
import md5
import uuid
import json

json_enc = json.JSONEncoder()
json_dec = json.JSONDecoder()

# code

listen_host = ''
listen_port = 0

class LogonServerHandler(SocketServer.StreamRequestHandler):
    
    def __init__(self, request, client_address, server):
        self.timeout = 2
        self.disable_nagle_algorithm = True
        SocketServer.StreamRequestHandler.__init__(self, request, client_address, server)
    
    # verify version
    def auth_version(self, ver):
                   
        ret = (ver == 1.0)
        if not ret:
            logger(__file__, 'unknow version %.1f' % (ver))  
        else:
            logger(__file__, 'check version %.1f' % (ver))  
            
        return ret
    
    def auth_logonuser(self, username, password):
        '''验证用户名和密码是否合法'''
        db_host = read_conf_file('logonServer', 'dbsvr_host')
        db_port = int(read_conf_file('logonServer', 'dbsvr_port'))
        
        dbconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dbconn.settimeout(2)
        
        query_info = {}
        query_info['Request'] = 'Logon'
        query_info['usr'] = username
        query_info['pwd'] = password
        
        data = json_enc.encode(query_info)
        
        dbconn.connect((db_host, db_port))
        dbconn.send(data)
        DBRecv = dbconn.recv(1024)
        dbconn.close()
        
        DB_Response = json_dec.decode(DBRecv)
        
        return (DB_Response['Response'] == True and DB_Response['uid'] != None)  
    
    def make_session_key(self):
        '''生成 session key'''
        return uuid.uuid1().get_hex()
    
    def put_session_to_server(self, session, usr, pwd):
        '''发送 session 到服务器'''
        info = {}
        info['Request'] = 'put_session'
        info['session'] = session
        info['usr'] = usr
        info['pwd'] = pwd
        
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
    
    def send_session_to_client(self, session):
        '''发送Session 和 Hall 服务器IP地址到 Client '''
        hall_ip   = read_conf_file('logonServer', 'HallIP')
        hall_port = int(read_conf_file('logonServer', 'HallPort'))
        
        info = {}
        info['Response'] = True
        info['HallHost'] = hall_ip
        info['HallPort'] = hall_port
        info['Session']  = session
        
        data = json_enc.encode(info)
        self.request.send(data)
        
    
    def handle(self):
            
        try:
            data = self.request.recv(1024)
            request_info = json_dec.decode(data)
            # verifier version
            if not self.auth_version(request_info['ver']):
                return
            
            logger(__file__, 'request accept : %s:%d' % (self.client_address[0], self.client_address[1]))
                
            # 验证账户密码
            usr = request_info['usr']
            pwd = request_info['pwd']
            
            pwd = md5.new(pwd).hexdigest()
            if not self.auth_logonuser(usr, pwd):
                return
            
            # make session key
            session_key = self.make_session_key()               
            
            # put sesssion key to main server
            if not self.put_session_to_server(session_key, usr, pwd):
                return
            
            # send session, chat server to client
            self.send_session_to_client(session_key)
           
            logger(__file__, 'requect process finish')
            
            self.request.close()

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
    
    show_frame('Logon Server')
    
    logger(__file__, 'Logon Server Starting....')
    
    # 读取配置文件
    listen_host = read_conf_file('logonServer', 'host')
    listen_port = int(read_conf_file('logonServer', 'port'))
    
    start_listen_thread(LogonServerHandler, listen_host, listen_port)
    
    main_loop()
    
    logger(__file__, 'Logon Server Exit.')
        
if __name__ == '__main__':
    main()