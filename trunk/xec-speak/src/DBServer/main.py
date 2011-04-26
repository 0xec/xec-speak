'''
Created on 2011-4-21

@author: xec
'''

import SocketServer
from common.xec_tcpsvr import *
from common.logger import *


listen_host = ''
listen_port = 0

class DatabaseServer(SocketServer.StreamRequestHandler):
    def __init__(self, request, client_address, server):
        self.timeout = 2
        self.disable_nagle_algorithm = True
        SocketServer.StreamRequestHandler.__init__(self, request, client_address, server)
        
    def handle(self):
            
        try:
            # verifier version
            if not self.auth_version():
                return
            
            logger(__name__, 'request accept : %s:%d' % (self.client_address[0], self.client_address[1]))
                
            # ��֤�˻�����
            usr = self.rfile.read(32)
            pwd = self.rfile.read(32)
            if not self.auth_logonuser(usr, pwd):
                return
            
            # make session key
            
            # put sesssion key to main server
            
            # send session, chat server to client
           
            logger(__name__, 'requect process finish')

        except Exception, err:
            self.request.close()
            logger(__name__, str(err).decode('gbk'))
                
        logger(__name__, 'requect close')
            
    def finish(self):
        logger(__name__, 'client disconnect...')

def main():
    logger(__name__, 'Logon Server Starting....')
    
    # ��ȡ�����ļ�
    listen_host = read_conf_file('config', 'host')
    listen_port = int(read_conf_file('config', 'port'))
    
    start_listen_thread(DatabaseServer, listen_host, listen_port)
    logger(__name__, 'Logon Server Exit.')

if __name__ == '__main__':
    main()