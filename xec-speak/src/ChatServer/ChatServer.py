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

client_list = {}

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
    
    def Add_Client(self, info):
        '''添加一个连接到客户端链表'''
        global client_list
                
        session_key = info['Session']
        
        client_list[session_key] = {}
        client_list[session_key]['Request'] = self.request
        
    def Remove_Client(self):
        '''删除一个客户端连接'''
        global client_list
        
        for label in client_list.keys():
            if client_list[label]['Request'] == self.request:
                print 'Remove Session', label
                del client_list[label]        
    
    def Broadcast_Data(self, info):
        for item in client_list:
            if client_list[item]['Request'] != self.request:
                
                rep_info = {}
                rep_info['Response'] = True
                rep_info['Info']     = 'Broadcast'
                rep_info['Data']     = info['Data']
                
                data = json_enc.encode(rep_info)
                client_list[item]['Request'].send(data)
        
        
    def handle(self): 
        global client_list 
        
        while True:
            try:
                data = self.request.recv(1024)
                if data == None or len(data) == 0:
                    return
                
                req_info = json_dec.decode(data)
                rep_info = {}

                if req_info.has_key('Session') == False:
                    rep_info['Response'] = False
                    rep_info['Info'] = 'no session'
                    
                else:     
                  
                    # 保存连接
                    self.Add_Client(req_info)
                    
                    if self.check_session(req_info['Session']):
                              
                        if req_info['Request'] == 'Broadcast':   # 请求命令
                            
                            self.Broadcast_Data(req_info)
                            
                            rep_info['Response'] = True
                            rep_info['Info']     = 'Successfully'                           
                        else:
                            pass
                    
                    else:
                        rep_info['Response'] = False
                        rep_info['Info'] = 'session error'
                    
                    
                data = json_enc.encode(rep_info)
                self.request.send(data)
    
            except Exception, err:
                             
                self.request.close()                
                logger(__file__, str(err).decode('gbk'))
                break
            
        # end while
            
    def finish(self):
        self.Remove_Client()
                
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