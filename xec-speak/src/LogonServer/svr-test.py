#!/usr/bin/env python
#coding=utf-8

from socket import *

if __name__ == '__main__':
    #for i in range(1, 9999):
        usr = '%-32s' % ('admin')
        pwd = '%-32s' % ('admin888')
        data = '\x00\x01' + usr + pwd
        sockobj = socket(AF_INET, SOCK_STREAM)
        sockobj.connect(('localhost', 8400) )
        sockobj.send(data)
        sess = sockobj.recv(74)
        print sess
        cmd         = sess[:5].strip()
        session_key = sess[5:37].strip()
        hall_host   = sess[37:70].strip()
        hall_port   = int(sess[70:75].strip())
        sockobj.close() 