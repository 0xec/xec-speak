#!/usr/bin/env python
#coding=gbk

import sys
sys.path.append('../')
import socket
from common.xec_tcpsvr import *
from common.logger import *
from common.frame import *
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
        '''验证 session 是否已经登录，返回登录状态和登录名'''
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
        
        return rep
    
    def Add_Client(self, req_socket, session, username):
        '''添加一个连接到客户端链表'''
        global client_list
       
        if not client_list.has_key(session):
            client_list[session] = {}
            client_list[session]['Request']  = req_socket
            client_list[session]['Session']  = session
            client_list[session]['Username'] = username
        
    def Remove_Client(self, req_socket):
        '''删除一个客户端连接'''
        global client_list
        
        for session in client_list.keys():
            if client_list[session]['Request'] == req_socket:
                print 'Remove Session', session
                del client_list[session]        
    
    def Broadcast_Data(self, data, session_key):
        
        for session in client_list:
            if client_list[session]['Session'] != session_key:
                
                rep_info = {}
                rep_info['Response'] = True
                rep_info['Info']     = 'Broadcast'
                rep_info['Username'] = client_list[session_key]['Username']
                rep_info['Data']     = data
                
                data = json_enc.encode(rep_info)
                client_list[session]['Request'].send(data)
                
    def Query_Users(self, rep):
        
        loop = 0
        rep['clients'] = {}
        for session in client_list:
            rep['clients'][loop] = client_list[session]['Username']
            loop = loop + 1
        
    def handle(self): 
        global client_list 
        
        while True:
            try:
                data = self.request.recv(1024)
                if data == None or len(data) == 0:
                    return
                
                req_info = json_dec.decode(data)
                rep_info = {}

                # 验证请求里是否有 session
                if req_info.has_key('Session') == False:
                    rep_info['Response'] = False
                    rep_info['Info'] = 'no session'
                    
                else:    
                    
                    # 客户 session
                    session_key = req_info['Session']
                         
                    # 验证 session 是否合法
                    chk_session = self.check_session(session_key)   
                    
                    if chk_session['Response'] == True:
                        
                        # 保存连接
                        self.Add_Client(self.request, session_key, chk_session['Username'])   
                              
                        # 判断请求类型
                        if req_info['Request'] == 'Broadcast':   # 请求命令
                            
                            # 广播消息
                            self.Broadcast_Data(req_info['Data'], session_key)
                            
                            rep_info['Response'] = True
                            rep_info['Info']     = 'Broadcast'   
                            
                        elif req_info['Request'] == 'QueryUsers':
                            
                            # 请求客户端链表
                            self.Query_Users(rep_info)
                            rep_info['Response'] = True
                            rep_info['Info']     = 'Users'   
                                              
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
        self.Remove_Client(self.request)
                
        logger(__file__, 'client disconnect...')
        
def main():
    global listen_host
    global listen_port
    
    show_frame('Chat Server')
    
    logger(__file__, 'Chat Server Starting....')         # 
    
    # 
    listen_host = read_conf_file('ChatServer', 'host')
    listen_port = int(read_conf_file('ChatServer', 'port'))
    
    start_listen_thread(SessionServer, listen_host, listen_port)
    
    main_loop()
    
    logger(__file__, 'Chat Server Exit.')

if __name__ == '__main__':
    main()