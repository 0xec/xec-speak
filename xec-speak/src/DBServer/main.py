#!/usr/bin/env python
#coding=utf-8

import SocketServer
import sys
sys.path.append('../')
from common.xec_tcpsvr import *
from common.logger import *
import os
import sqlite3.dbapi2 as sqlite

listen_host = ''
listen_port = 0

db_file = os.path.abspath('./../db/dbfile.sqlite');

class DatabaseServer(SocketServer.StreamRequestHandler):
    
    def __init__(self, request, client_address, server):
        self.timeout = 2
        self.disable_nagle_algorithm = True
        
        # 初始化 sqlite
        logger(__name__, 'load database %s' % (db_file))
        self.db = sqlite.connect(db_file)
        self.db.cursor()
        
        SocketServer.StreamRequestHandler.__init__(self, request, client_address, server)
        
        
    def handle(self):
            
        try:
            self.cmd = self.rfile.read(5)
            if self.cmd == None or len(self.cmd) == 0:
                return
            
            if self.cmd.startswith('LOGON'):
                self.usr = self.rfile.read(32).strip()
                self.pwd = self.rfile.read(32).strip()
                self.sql = 'SELECT uid, usr, pwd, pm from users where usr = \'%s\' and pwd = \'%s\'' % (self.usr, self.pwd)
                self.rs = self.db.execute(self.sql)
                self.line = self.rs.fetchone()
                if self.line == None:
                    self.wfile.write('FAILD')
                else:
                    print self.line[0]
                    self.wfile.write('%-5d' % (self.line[0]))
            else:
                pass
                
           
            logger(__name__, 'requect process finish')

        except Exception, err:
            self.request.close()
            logger(__name__, str(err).decode('gbk'))
                
        logger(__name__, 'requect close')
            
    def finish(self):
        logger(__name__, 'client disconnect...')

def main():
    logger(__name__, 'DB Server Starting....')
    
    # 读取配置文件
    listen_host = read_conf_file('DBServer', 'host')
    listen_port = int(read_conf_file('DBServer', 'port'))
    
    start_listen_thread(DatabaseServer, listen_host, listen_port)
    logger(__name__, 'DB Server Exit.')

if __name__ == '__main__':
    main()