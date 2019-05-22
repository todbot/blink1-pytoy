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
        blink1_color(100, 255,0,255)

    def on_purple(self, event):
        print ('BLOOOP')
        blink1_color(100, 255,255,255)

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()

class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self):
        super().__init__(parent=None, title='blink(1) toy')
        panel = wx.Panel(self)        
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        self.text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)        
        my_btn = wx.Button(panel, label='Press Me')
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)        
        panel.SetSizer(my_sizer)        
        self.Show()
        
    def on_press(self, event):
        value = self.text_ctrl.GetValue()
        if not value:
            print("You didn't enter anything!")
            return
        print(f'You typed: "{value}"')

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

    
