#!/usr/bin/env python
#coding=utf-8

import SocketServer
import ConfigParser
from logger import *

config_file = '../conf/config.conf'
server = []

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def read_conf_file(section, label):
    '''读取配置文件'''
    global listen_host
    global listen_port
    
    cf = ConfigParser.ConfigParser()
    cf.read(config_file)
    listen_host = cf.get(section, label)

def start_listen_thread(ServerHandler, host, port):
    '''启动服务器线程'''
    global server
    
    logger('Logon Server Work ' + host + ':' + str(port))
    
    # start listen socket
    try:
        server = ThreadedTCPServer((host, port), ServerHandler)
        server_thread = threading.Thread(target = server.serve_forever)
        server_thread.setDaemon(True)
        server_thread.start()
        server.serve_forever()
        
    except Exception, data:
        error = str(data)
        logger(error.decode('gbk'))
        
if __name__ == '__main__':
    pass