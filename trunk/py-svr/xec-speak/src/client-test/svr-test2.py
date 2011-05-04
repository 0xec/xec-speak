#!/usr/bin/env python
#coding=gbk

from socket import *
import json
import time
import struct
import base64

json_enc = json.JSONEncoder()
json_dec = json.JSONDecoder()

if __name__ == '__main__':
  #  for i in range(1, 999):  
        Session_Key = None
        
        info = {}
        info['usr'] = 'admin2'
        info['pwd'] = 'admin888'
        info['ver'] = 1.0
        
        data = json_enc.encode(info)

        # 登陆服务器
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(('localhost', 8400) )
        s.send(data)
        data = s.recv(1024)
        s.close
        rep = json_dec.decode(data)
        print rep
        
        Session_Key = rep['Session']
        
        info = {}
        
        # 大厅服务器
        s = None
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((rep['HallHost'], rep['HallPort']))
        
        info['Request'] = 'ChatRoomList'
        info['Session'] = Session_Key
        data = json_enc.encode(info)
        s.send(data)
        data = s.recv(1024)
        s.close
        rep = json_dec.decode(data)
        
        # 连接到聊天室
        chat_host = rep['client1']['host']
        chat_port = rep['client1']['port']
        
        print 'connect to', chat_host, chat_port
        
        s = None
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((chat_host, chat_port))    
        
        loop = 0
        while loop < 50:
            
            data = {}
            data['Request'] = 'Broadcast'
            data['Session'] = Session_Key
            data['Data']    = base64.encodestring('\x30\xAA\xFC\AA')
            data = json_enc.encode(data)
            
            s.send(data)
            
            data = s.recv(1024)  
            print data  
            time.sleep(5)    
            loop = loop + 1
        
        s.close()
        