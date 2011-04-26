#!/usr/bin/env python
#coding=utf-8

from socket import *

if __name__ == '__main__':
    #for i in range(1, 9999):
        usr = '%-32s' % ('xx')
        pwd = '%-32s' % ('yy')
        data = '\x00\x01' + usr + pwd
        sockobj = socket(AF_INET, SOCK_STREAM)
        sockobj.connect(('localhost', 8400) )
        sockobj.send(data)
        sockobj.close() 