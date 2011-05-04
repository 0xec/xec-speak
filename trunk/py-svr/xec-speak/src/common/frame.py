#!/usr/bin/env python
#coding=gbk

import sys
import os
from wxPython.wx import *

frame = object
App   = object

class mainFrame(wxFrame):
    def __init__(self, title):
        wxFrame.__init__(self, None, wxID_ANY, title, wxDefaultPosition, wxSize(600, 300))
     #   self.Panel = wxPanel(self, wxID_ANY)
        self.textCtrl = wxTextCtrl(self, pos=wxDefaultPosition, size=wxDefaultSize, style=wxTE_MULTILINE)
        self.Bind(EVT_CLOSE, self.OnClose, self)
        wxFrame.Centre(self)
        
    def OnClose(self, event):
        sys.exit(1)

class theApp(wxApp):
    
    def setTitle(self, FrameTitle):
        frame.SetTitle(FrameTitle)

    def OnInit(self):
        global frame
        frame = mainFrame('')
        frame.Show(true)
        return true
        
def show_frame(title):
    global App
    App = theApp(0)
    App.setTitle(title)
    
def main_loop():
    global App
    App.MainLoop()
    
if __name__ == '__main__':
    show_frame('test')
    main_loop()
    
        