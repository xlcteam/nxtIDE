#!/usr/bin/env python

import wx
import wx.aui
import os

from pystc import PythonSTC

import pycheck
import subprocess
from threading import Thread
import yaml


class PYSTCChild(wx.aui.AuiMDIChildFrame):
    path = ''
    filename = ''
    def __init__(self, parent, title):
        wx.aui.AuiMDIChildFrame.__init__(self, parent, -1, title=title)

        self.editor = PythonSTC(self, -1)
        self.mgr = wx.aui.AuiManager()
        self.mgr.SetManagedWindow(self)
        self.mgr.AddPane(self.editor, 
                                 wx.aui.AuiPaneInfo().Name("editor").
                                 CenterPane().PaneBorder(False))
        self.mgr.Update()
        
        self.Bind(wx.EVT_MENU, self.onOpen, id=parent.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.onSave, id=parent.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.onSaveAs, id=parent.ID_SAVE_AS)
        self.Bind(wx.EVT_MENU, self.onClose, id=parent.ID_CLOSE)

        self.Bind(wx.EVT_MENU, self.onCompile, id=parent.ID_COMPILE)
        self.Bind(wx.EVT_MENU, self.onEmuRun, id=parent.ID_EMU_RUN)
        self.Bind(wx.EVT_MENU, self.onDownload, id=parent.ID_BRICK_DOWNLOAD)
        self.Bind(wx.EVT_MENU, self.onDownloadRun, 
                  id=parent.ID_BRICK_DOWNLOAD_RUN)
        
        self.Bind(wx.EVT_CLOSE, self.close)

        self.parent = parent

        self.emuproc = None
        

    def onOpen(self, event):
        dir = os.getcwd()
        wc = 'Py files (*.py)|*.py|All files(*)|*'
        dialog = wx.FileDialog(self, message = 'Open file ...',
                               defaultDir = dir, defaultFile = '', 
                               wildcard = wc,
                               style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            self.editor.LoadFile(path)
            self.path = path
            self.filename = os.path.basename(path)
            self.SetTitle(self.filename)

        
        dialog.Destroy()

    def onSave(self, event):
        if self.path != '':
            self.editor.SaveFile(self.path)
        else:
            return self.onSaveAs(event)

    def onSaveAs(self, event):
        dir = os.getcwd()
        wc = 'Py files (*.py)|*.py|All files(*)|*'
        dialog = wx.FileDialog(self, message = 'Save file as...',
                               defaultDir = dir, defaultFile = self.GetTitle(), 
                               wildcard = wc,
                               style=wx.SAVE | wx.OVERWRITE_PROMPT)

        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            if not path.endswith('.py'):
                path += '.py'

            self.editor.SaveFile(path)
            self.path = path
            self.filename = os.path.basename(path)
            self.SetTitle(self.filename)

        
        dialog.Destroy()
    
    def closeTest(self):
        self.parent.count -= 1
        if self.parent.count < 1:
            self.parent.Destroy()



    def close(self, event):
        self.closeTest()

        event.Skip()

    def onClose(self, event):
        self.closeTest()

        self.Destroy()

    def onCompile(self, event):
        self.onSave(event = None)
        self.parent.hideMsg()

        check = pycheck.PyCheck()
        check.check(self.parent.cfg['nxtemu'] + "/api.py")
        try:
            check.check(self.path)
        except NameError as nr:
            msg = "NameError: %s on line %d" % nr.args
            self.editor.GotoLine(nr.args[1] - 1)
            self.parent.showMsg(msg)
            
            return False

        except SyntaxError as se:
            msg = "SyntaxError: on line %d" % se.args[1][1]
            
            pos = self.editor.GetLineEndPosition(se.args[1][1] - 2)
            pos += se.args[1][2]

            self.editor.GotoPos(pos)
            self.parent.showMsg(msg)

            return False

        self.parent.statusbar.SetStatusText("Compiled...OK")

        wx.FutureCall(2000, self.clearStatusbar)

        f = open("%s/__progs__/e%s" % \
                 (self.parent.cfg["nxtemu"], self.filename), "w")

        f.write("from api import *\n")
        f.write(pycheck.loopFix(self.editor.GetText(), "_ticker()"))
        f.close()

        return True

    def onEmuRun(self, event):
        
        # do not run in emulator if there is a syntax or name error
        if not self.onCompile(event = None):
            return
        
        if self.emuproc != None:
            try:
                self.emuproc.terminate()
            except OSError as e:
                pass

            self.emuproc = None
        
        # run an exe application if on Windows, otherwise py script
        extension = 'exe' if wx.Platform == '__WXMSW__' else 'py'
        nxtemu = "%s/nxtemu.%s" % (self.parent.cfg["nxtemu"], extension)
        
        self.emuproc = subprocess.Popen([nxtemu, 
                                         self.filename.replace('.py', '')],
                                         stdin = subprocess.PIPE,
                                         stdout = subprocess.PIPE,
                                         stderr = subprocess.PIPE)
        
        Thread(target=self.emuproc.communicate).start()


    def onDownloadRun(self, event):
        print "dr"

    def onDownload(self, event):
        print "d"

    def clearStatusbar(self):
        self.parent.statusbar.SetStatusText("", 0)

class PreferencesDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(600, 210))
        
        sizer = wx.GridBagSizer(3, 3)

        l1 = wx.StaticText(self, -1, 'nxtemu directory:')
        self.i1 = wx.TextCtrl(self, -1, parent.cfg["nxtemu"])
        b1 = wx.Button(self, -1, '...')
        self.Bind(wx.EVT_BUTTON, self.onDir, b1)
        ok = wx.Button(self, -1, 'Save')
        self.Bind(wx.EVT_BUTTON, self.onOk, ok)

        sizer.Add(l1, pos=(0, 0), flag=wx.TOP|wx.LEFT, border=5)
        sizer.Add(self.i1, pos=(0, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND)
        sizer.Add(b1, pos=(0, 4), flag=wx.TOP|wx.RIGHT, border=5)

        sizer.Add(ok, pos=(3, 4), flag=wx.TOP|wx.RIGHT|wx.EXPAND)
        
        sizer.AddGrowableCol(2)
        self.SetSizer(sizer)

        self.parent = parent
    
    def onDir(self, event):
        dialog = wx.DirDialog(None, "Choose a directory:", 
                                style=wx.DD_DEFAULT_STYLE, 
                                defaultPath=self.parent.cfg["nxtemu"])
        if dialog.ShowModal() == wx.ID_OK:
            self.parent.cfg["nxtemu"] = dialog.GetPath()

            self.i1.SetValue(self.parent.cfg["nxtemu"])
            dialog.Destroy()


    def onOk(self, event):
        f = open("config.yml", 'w')
        f.write(yaml.dump(self.parent.cfg))
        f.close()
        self.Destroy()


class Editor(wx.aui.AuiMDIParentFrame):
    ID_SAVE = 1001
    ID_SAVE_AS = 1002
    ID_CLOSE = 1003
    ID_OPEN = 1004
    ID_COMPILE = 1006
    ID_EMU_RUN = 1007
    ID_BRICK_DOWNLOAD = 1008
    ID_BRICK_DOWNLOAD_RUN = 1009

    emuproc = None
    def __init__(self, parent):
        wx.aui.AuiMDIParentFrame.__init__(self, parent, -1,
                                          title = "NXC Editor",
                                          size = (640,480),
                                          style = wx.DEFAULT_FRAME_STYLE)

        
        
        self._mgr = wx.aui.AuiManager()                                         
        self._mgr.SetManagedWindow(self) 
        self.msgs = wx.TextCtrl(self,-1, "", wx.Point(0, 0), wx.Size(150, 40),
                          wx.NO_BORDER | wx.TE_MULTILINE)    
        self._mgr.AddPane(self.msgs, wx.aui.AuiPaneInfo().    
                         Name("messages").Caption("Messages").Bottom().          
                         CloseButton(True).MaximizeButton(True).Hide())   

        self.count = 0
        self.mb = self.MakeMenuBar()
        self.SetMenuBar(self.mb)
        self.statusbar = self.CreateStatusBar()

        self.OnNewChild(None)
        
        #self._mgr.Update()
        self.Show(True)
        
        # import config from yaml file
        self.cfg = yaml.load(open("config.yml").read())


    
    def showMsg(self, msg = None):
        if msg != None:
            self.msgs.SetValue(msg)

        self._mgr.GetPane("messages").Show()
        self._mgr.Update()

    def hideMsg(self):
        self._mgr.GetPane("messages").Hide()
        self._mgr.Update()

    def MakeMenuBar(self):
        mb = wx.MenuBar()
        self.menu = wx.Menu()
        item = self.menu.Append(-1, "New\tCtrl-N")
        self.Bind(wx.EVT_MENU, self.OnNewChild, item)

        self.menu.AppendSeparator()
        
        item = self.menu.Append(self.ID_OPEN, "Open\tCtrl+O")
        item = self.menu.Append(self.ID_SAVE, "Save\tCtrl+S")
        item = self.menu.Append(self.ID_SAVE_AS, "Save as\tCtrl+Shift+S")
        self.menu.AppendSeparator()

      
                
        item = self.menu.Append(-1, "Next\tCtrl-PgDn")
        self.Bind(wx.EVT_MENU, self.Next, item)
        item = self.menu.Append(-1, "Previous\tCtrl-PgUp")
        self.Bind(wx.EVT_MENU, self.Prev, item)


        self.menu.AppendSeparator()
        item = self.menu.Append(-1, "Preferences")
        self.Bind(wx.EVT_MENU, self.onPreferences, item)
        self.menu.AppendSeparator()
        
        item = self.menu.Append(self.ID_CLOSE, "Close\tCtrl-W")
        item = self.menu.Append(-1, "Quit\tCtrl-Q")
        self.Bind(wx.EVT_MENU, self.OnDoClose, item)
        

        self.run_menu= wx.Menu()
        self.run_menu.Append(self.ID_COMPILE, "Compile\tF5")
        self.run_menu.Append(self.ID_EMU_RUN, "Run in nxtemu\tF6")
        self.run_menu.AppendSeparator()
        self.run_menu.Append(self.ID_BRICK_DOWNLOAD, 
                             "Download to NXT Brick\tCtrl-F5")
        self.run_menu.Append(self.ID_BRICK_DOWNLOAD_RUN, 
                             "Download to Brick && run\tCtrl-F6")
        
    
        mb.Append(self.menu, "&File")
        mb.Append(self.run_menu, "&Run")
        return mb

    def Next(self, event):
        return self.ActivateNext()

    def Prev(self, event):
        return self.ActivatePrevious()

    def OnNewChild(self, evt):
        self.count += 1
        child = PYSTCChild(self, "file%d" % self.count)
        child.Show()

        child.Refresh()
        self._mgr.Update()
        

    def OnDoClose(self, evt):
        self.Close()

    def onPreferences(self, evt):
        pref = PreferencesDialog(self, -1, 'Preferences')
        pref.ShowModal()
        pref.Destroy()
 
            
if __name__ == "__main__":
    app = wx.App()
    Editor(None)
    app.MainLoop()
