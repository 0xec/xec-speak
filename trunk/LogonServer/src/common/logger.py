'''
Created on 2011-4-26

@author: xec
'''
import threading

def logger(msg):
    log = '[thread: %s] %s' % (threading.currentThread().getName(), msg)
    print log

if __name__ == '__main__':
    pass
        