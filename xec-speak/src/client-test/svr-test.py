#!/usr/bin/env python
#coding=utf-8

from socket import *
import json

json_enc = json.JSONEncoder()
json_dec = json.JSONDecoder()

if __name__ == '__main__':
  #  for i in range(1, 999):  
        info = {}
        info['usr'] = 'admin'
        info['pwd'] = 'admin888'
        info['ver'] = 1.0
        
        data = json_enc.encode(info)

        s = socket(AF_INET, SOCK_STREAM)
        s.connect(('localhost', 8400) )
        s.send(data)
        data = s.recv(1024)
        s.close
        rep = json_dec.decode(data)
        print rep
        
        info = {}
        
        s = None
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((rep['HallHost'], rep['HallPort']))
        
        info['Request'] = 'ChatRoomList'
        data = json_enc.encode(info)
        s.send(data)
        data = s.recv(1024)
        s.close
        rep = json_dec.decode(data)
        for label in rep:
            print label
            print rep[label]
        print rep
        