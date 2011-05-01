'''
Created on 2011-4-26

@author: xec
'''
import threading
import os
import frame

lock = threading.RLock()

def logger(module, msg):
    global frame
    lock.acquire()
    log = '[%s][thread: %s] %s\n' % (os.path.basename(module), threading.currentThread().getName(), msg)
    print log
    frame.frame.textCtrl.AppendText(log)
    lock.release()

if __name__ == '__main__':
    pass
        