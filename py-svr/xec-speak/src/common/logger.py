#!/usr/bin/env python
#coding=gbk

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
        