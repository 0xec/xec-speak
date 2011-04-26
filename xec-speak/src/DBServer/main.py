'''
Created on 2011-4-21

@author: xec
'''

import SocketServer
from common.xec_tcpsvr import *
from common.logger import *


config_file = 'config.conf'

# code

listen_host = ''
listen_port = 0
server = []

class DatabaseServer(SocketServer.StreamRequestHandler):
    pass

if __name__ == '__main__':
    logger('Logon Server Starting....')
    start_listen_thread(DatabaseServer, '', 8000)
    logger('Logon Server Exit.')