#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append('../')
from common.xec_tcpsvr import *
from common.logger import *
from common.frame import *
import sqlite3.dbapi2 as sqlite

import json

json_enc = json.JSONEncoder()
json_dec = json.JSONDecoder()

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
            data = self.request.recv(1024)
            if data == None or len(data) == 0:
                return
            
            req_info = json_dec.decode(data)
            
            if req_info['Request'] == 'Logon':
                rep_info = {}
                
                logger(__file__, 'query usr[%s:%s]' % (req_info['usr'], req_info['pwd']))
                
                self.sql = 'SELECT uid, usr, pwd, pm from users where usr = \'%s\' and pwd = \'%s\'' % (req_info['usr'], req_info['pwd'])
                self.rs = self.dbconn.execute(self.sql)
                self.line = self.rs.fetchone()
                if self.line != None:
                    rep_info['Response'] = True
                    rep_info['uid']      = self.line[0]
                else:
                    rep_info['Response'] = False
                    rep_info['uid']      = None
                
                data = json_enc.encode(rep_info)
                self.request.send(data)
                    
            else:
                pass
                
           
            logger(__file__, 'db process finish')

        except Exception, err:
            self.request.close()
            logger(__file__, str(err).decode('gbk'))
            
    def finish(self):
        logger(__file__, 'db client disconnect...')

def main():
    global listen_host
    global listen_port
    
    show_frame('DB Server')
    
    logger(__file__, 'DB Server Starting....')
    
    # 读取配置文件
    listen_host = read_conf_file('DBServer', 'host')
    listen_port = int(read_conf_file('DBServer', 'port'))
    
    start_listen_thread(DatabaseServer, listen_host, listen_port)
    
    main_loop()
    
    logger(__file__, 'DB Server Exit.')

if __name__ == '__main__':
    main()