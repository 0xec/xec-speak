'''
Created on 2011-4-26

@author: xec
'''
import threading

lock = threading.RLock()

def logger(module, msg):
    lock.acquire()
    log = '[%s][thread: %s] %s' % (module, threading.currentThread().getName(), msg)
    print log
    lock.release()

if __name__ == '__main__':
    pass
        