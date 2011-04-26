#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append('../')
from common.xec_tcpsvr import *
from common.logger import *
import sqlite3.dbapi2 as sqlite

listen_host = ''
listen_port = 0

db_file = os.path.abspath('./../db/dbfile.sqlite');

class DatabaseServer(SocketServer.StreamRequestHandler):
    
    def __init__(self, request, client_address, server):
        self.timeout = 2
        self.disable_nagle_algorithm = True   
        self.dbconn  = sqlite.connect(db_file)
        self.dbconn.cursor()   
        SocketServer.StreamRequestHandler.__init__(self, request, client_address, server)
        
        
    def handle(self):
            
        try:
            self.cmd = self.rfile.read(5)
            if self.cmd == None or len(self.cmd) == 0:
                return
            
            if self.cmd.startswith('LOGON'):
                self.usr = self.rfile.read(32).strip()
                self.pwd = self.rfile.read(32).strip()
                
                logger(__file__, 'query usr[%s:%s]' % (self.usr, self.pwd))
                
                self.sql = 'SELECT uid, usr, pwd, pm from users where usr = \'%s\' and pwd = \'%s\'' % (self.usr, self.pwd)
                self.rs = self.dbconn.execute(self.sql)
                self.line = self.rs.fetchone()
                if self.line == None:
                    self.wfile.write('FAILD')
                else:
                    self.wfile.write('%-5d' % (self.line[0]))
            else:
                pass
                
           
            logger(__file__, 'db process finish')

        except Exception, err:
            self.request.close()
            logger(__file__, str(err).decode('gbk'))
            
    def finish(self):
        logger(__file__, 'db client disconnect...')

def main():
    logger(__file__, 'DB Server Starting....')
    
    # 读取配置文件
    listen_host = read_conf_file('DBServer', 'host')
    listen_port = int(read_conf_file('DBServer', 'port'))
    
    start_listen_thread(DatabaseServer, listen_host, listen_port)
    logger(__file__, 'DB Server Exit.')

if __name__ == '__main__':
    main()