#!/usr/bin/env python
#coding=utf-8

from socket import *

if __name__ == '__main__':
    usr = '%-32s' % ('xx')
    pwd = '%-32s' % ('yy')
    data = '\x00\x01' + usr + pwd
    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.connect(('localhost', 8400) )
    sockobj.send(data)
    print sockobj.recv(1000)
    sockobj.close()