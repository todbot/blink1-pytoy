#!/usr/bin/env python
#
# pyinstaller blink1Toy.py --windowed
#
#
import wx
import wx.adv
import os
import sys
from blink1.blink1 import Blink1

TRAY_TOOLTIP = 'blink(1) toy'
TRAY_ICON = 'icon.png'

#def GetImgsDir():
#    installDir = os.path.split(os.path.abspath(sys.argv[0]))[0]
#    imgsDir = os.path.join(self.installDir, "imgs")
#    return imgsDir

def blink1_color(msec,r,g,b):
    try:
        blink1 = Blink1()
        blink1.fade_to_rgb(msec,r,g,b)
        blink1.close()
    except:
       print("no blink1 found")

#def create_menu_item(menu, label, func):
#    item = wx.MenuItem(menu, wx.NewId(), label)
#    menu.Bind(wx.EVT_MENU, func, item)
#    menu.Append(item)
#    return item

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
#        self.set_icon( TRAY_ICON )
        self.set_icon( os.path.join(wx.GetApp().GetImgsDir(), TRAY_ICON) )
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'White', self.on_white)
        create_menu_item(menu, 'Purple', self.on_purple)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(path)
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        print ('Tray icon was left-clicked.')

    def on_white(self, event):
        print ('Hello, world!')
        blink1_color(100, 255,255,255)

    def on_purple(self, event):
        print ('BLOOOP')
        blink1_color(100, 255,0,255)

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()

class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self):
        super().__init__(parent=None, title='blink(1) toy')
        panel = wx.Panel(self)
        self.Bind(wx.EVT_CLOSE, self.closewindow)

        topSizer = wx.BoxSizer(wx.VERTICAL)
        inputOneSizer = wx.BoxSizer(wx.HORIZONTAL)
        blBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

#        labelOne = wx.StaticText(panel, wx.ID_ANY, 'Input 1')
#        inputTxtOne = wx.TextCtrl(panel, wx.ID_ANY, '')

        okBtn = wx.Button(panel, wx.ID_ANY, 'OK')
        cancelBtn = wx.Button(panel, wx.ID_ANY, 'Cancel')

        redBtn = wx.Button(panel, wx.ID_ANY, 'red')
        grnBtn = wx.Button(panel, wx.ID_ANY, 'grn')
        bluBtn = wx.Button(panel, wx.ID_ANY, 'blu')
        self.Bind(wx.EVT_BUTTON, self.onBlinkButton, redBtn)
        self.Bind(wx.EVT_BUTTON, self.onBlinkButton, grnBtn)
        self.Bind(wx.EVT_BUTTON, self.onBlinkButton, bluBtn)

#        inputOneSizer.Add(labelOne, 0, wx.ALL, 5)
#        inputOneSizer.Add(inputTxtOne, 0, wx.ALL|wx.EXPAND, 5)

        blBtnSizer.Add(redBtn, 0, wx.ALL, 5)
        blBtnSizer.Add(grnBtn, 0, wx.ALL, 5)
        blBtnSizer.Add(bluBtn, 0, wx.ALL, 5)

        btnSizer.Add(okBtn, 0, wx.ALL, 5)
        btnSizer.Add(cancelBtn, 0, wx.ALL, 5)

        # topSizer.Add(inputOneSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(panel), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(blBtnSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(panel), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(btnSizer, 0, wx.ALL|wx.CENTER, 5)

        panel.SetSizer(topSizer)
        topSizer.Fit(self)

        # panel.SetSizer(bsizer)
        self.Show()

    def onBlinkButton(self,event):
#        print('event', event )
        obj = event.GetEventObject()
        print(obj.GetLabel())
        lbl = obj.GetLabel()
        if lbl == 'red' :
            print('reeed')
            blink1_color(100, 255,0,0 )
        elif lbl == 'grn':
            print('greeen')
            blink1_color(100, 0,255,0)

    def closewindow(self,event):
        self.Destroy()

    def on_press(self, event):
        print(f'You clicked')

class App(wx.App):
    def OnInit(self):
        frame = MyFrame()
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        #self.imgsDir = 'hello'
        print(f'imgs_dir:{self.GetImgsDir()}')
        return True

    def OnExit(self):
        blink1_color(100,0,0,0)
        return True

    def GetImgsDir(self):
        installDir = os.path.split(os.path.abspath(sys.argv[0]))[0]
        imgsDir = os.path.join(installDir, "imgs")
        return imgsDir

def main():
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    main()
