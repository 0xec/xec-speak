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
        sess = s.recv(1024)
        print sess
#        cmd         = sess[:5].strip()
#        session_key = sess[5:37].strip()
#        hall_host   = sess[37:70].strip()
#        hall_port   = int(sess[70:75].strip())
        
        s.close