#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.aui
import wx.stc as stc
import os

from pystc import PythonSTC

import pycheck
import subprocess
from threading import Thread
import sys
import yaml
import tempfile

import ctypes

#--------------------------------   

class PYSTCChild(wx.aui.AuiMDIChildFrame):
    path = ''
    filename = ''
    SEARCHED = False
    res = None
    dlg = None

    def __init__(self, parent, title):
        """PYSTCChild initalization."""

        wx.aui.AuiMDIChildFrame.__init__(self, parent, -1, title=title)

        self.filename = title + '.py'           

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
        self.Bind(wx.EVT_MENU, self.onFindOpen, id=parent.ID_FIND)

        self.Bind(wx.EVT_MENU, self.onCompile, id=parent.ID_COMPILE)
        self.Bind(wx.EVT_MENU, self.onEmuRun, id=parent.ID_EMU_RUN)
        self.Bind(wx.EVT_MENU, self.onDownload, id=parent.ID_BRICK_DOWNLOAD)
        self.Bind(wx.EVT_MENU, self.onDownloadRun,
                  id=parent.ID_BRICK_DOWNLOAD_RUN)

        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.parent = parent

        self.emuproc = None

        self.findData = wx.FindReplaceData(wx.FR_DOWN)

        self.Bind(wx.EVT_FIND, self.onFind)
        self.Bind(wx.EVT_FIND_NEXT, self.onFind)
        self.Bind(wx.EVT_FIND_REPLACE, self.onReplace)
        self.Bind(wx.EVT_FIND_REPLACE_ALL, self.onReplaceAll)
        self.Bind(wx.EVT_FIND_CLOSE, self.onFindClose)


    def onFindOpen(self, event):
        self.dlg = wx.FindReplaceDialog(self, self.findData, "Find and Replace",
                            wx.FR_REPLACEDIALOG | wx.FR_NOUPDOWN | wx.FR_NOMATCHCASE | wx.FR_NOWHOLEWORD)
        self.dlg.ShowModal()

    def onFind(self, event):
        self.word = self.findData.GetFindString()
        
        if self.word == '':
            return

        self.updateRes()
        if self.res == -1:
            self.editor.GotoPos(0)
            self.updateRes()
            if self.res == -1:
                wx.MessageBox('Nothing found', 'Result', wx.OK | wx.ICON_INFORMATION)
                self.SEARCHED = False
                return False
            else:
                self.SEARCHED = False
        
        self.SearchFromHead(self.word)
        return True
        
    def onReplace(self, event):
        rstring = self.findData.GetReplaceString()

        if self.onFind(None):
            self.editor.ReplaceSelection(rstring)
            currPos = self.editor.GetCurrentPos()            
            self.editor.SetSelection(currPos - len(rstring) , currPos)
           
    def onReplaceAll(self, event):
        self.editor.GotoPos(0)
        fstring = self.findData.GetFindString()
        rstring = self.findData.GetReplaceString()

        self.updateRes()
        if self.res == -1:
            wx.MessageBox('Nothing found', 'Result', wx.OK | wx.ICON_INFORMATION)  
            return        

        text = self.editor.GetText()
        text = text.replace(fstring, rstring)

        self.editor.SetText(text)

    def onFindClose(self, event):
        self.dlg.Destroy()
        self.SEARCHED = False


    def SearchFromHead(self, word):
        currPos = self.editor.GetCurrentPos()

        if self.SEARCHED == False:
            self.SEARCHED = True
            self.editor.GotoPos(0)
        else:
            self.editor.GotoPos(currPos + len(word))
        
        self.editor.SearchAnchor()
        res = self.editor.SearchNext( stc.STC_FIND_REGEXP, word)

        if res == -1:
            self.SEARCHED = False
            self.SearchFromHead(word)

        self.editor.EnsureCaretVisible()

    def updateRes(self):
        self.word = self.findData.GetFindString()
        self.editor.SearchAnchor()
        self.res = self.editor.SearchNext( stc.STC_FIND_REGEXP, self.word)
        
    def get_doc_dir(self):
        """Returns the path to 'Documents' directory."""

        try:
            dll = ctypes.windll.shell32
            buf = ctypes.create_unicode_buffer(300)  # TODO: max_path
            if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
                    return buf.value
            else:
                    return os.getcwd()
        except:
            return os.getcwd()


    def onOpen(self, event):
        """Handle for file opening."""

        dir = self.get_doc_dir()
        wc = 'Py files (*.py)|*.py|All files(*)|*'
        dialog = wx.FileDialog(self, message='Open file ...',
                               defaultDir=dir, defaultFile='',
                               wildcard=wc,
                               style=wx.OPEN)

        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()

            # if there is something in active editor create a new one
            if self.path is not '':
                child = self.parent.OnNewChild(None)

                child.editor.LoadFile(path)
                child.path = path
                child.filename = os.path.basename(path)
                child.SetTitle(child.filename)

            else:
                self.editor.LoadFile(path)
                self.path = path
                self.filename = os.path.basename(path)
                self.SetTitle(self.filename)

        self.parent.titleUpdate()
        dialog.Destroy()


    def onSave(self, event):
        """Handle for file saving."""

        if self.path != '':
            self.editor.SaveFile(self.path)
        else:
            return self.onSaveAs(event)


    def onSaveAs(self, event):
        """Handle for saving file as."""

        dir = self.get_doc_dir()

        wc = 'Py files (*.py)|*.py|All files(*)|*'
        dialog = wx.FileDialog(self, message='Save file as...',
                               defaultDir=dir, defaultFile=self.GetTitle(),
                               wildcard=wc,
                               style=wx.SAVE | wx.OVERWRITE_PROMPT)

        status = dialog.ShowModal()
        if status == wx.ID_OK:
            path = dialog.GetPath()

            path = path.replace('.py', '')
            path = path.replace('.', '_')    # make it pythonic
            path += '.py'

            self.editor.SaveFile(path)
            self.path = path
            self.filename = os.path.basename(path)
            self.SetTitle(self.filename)

        self.parent.titleUpdate()
        dialog.Destroy()

        if status == wx.ID_CANCEL:
            return False
        else:
            return True


    def onClose(self, event):
        """Handle for closing PYSTCChild via either clicking on X or pressing
        Ctrl+W"""

        if self.editor.GetModify():
            dlgStyle = wx.YES_NO | wx.CANCEL | wx.ICON_INFORMATION
            msg = ("Save changes to document %s before closing?") % self.filename

            dlg = wx.MessageBox(msg, "Save changes?", style=dlgStyle)

            if dlg == wx.YES:
                self.onSave(None)
                self.Destroy()
            elif dlg == wx.NO: 
                self.Destroy()       

            # in case of Cancel
            else:
                return -1

            return
            
            # we don't need this, dlg is integer
            #dlg.Destroy()           

        self.parent.count -= 1
        if self.parent.count < 1:
            self.parent.Destroy()


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
            msg = "SyntaxError: %s \n\t on line %d" % \
                                (se.args[0], se.args[1][1])
            
            pos = self.editor.GetLineEndPosition(se.args[1][1] - 2)
            pos += se.args[1][2]

            self.editor.GotoPos(pos)
            self.parent.showMsg(msg)

            return False

        except ValueError as ve:
            msg = "ValueError: %s on line %d" % ve.args[:2]
            self.editor.GotoLine(ve.args[1] - 1)
            #pos = self.editor.GetLineEndPosition(ve.args[3])
            
            self.editor.SetSelection(ve.args[2][0], ve.args[2][1])
            self.parent.showMsg(msg)

            return False

        self.parent.statusbar.SetStatusText("Compiled...OK")

        wx.FutureCall(2000, self.clearStatusbar)

        f = open("%s/__progs__/e%s" % \
                 (self.parent.cfg["nxtemu"], self.filename), "w")

        f.write("from api import *\n")
        f.write(pycheck.loopFix(self.editor.GetText(), "ticker()"))
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
        extension = 'exe' if hasattr(sys, 'frozen') else 'py'
        nxtemu = "%s/nxtemu.%s" % (self.parent.cfg["nxtemu"], extension)
        
        self.emuproc = subprocess.Popen([nxtemu, 
                                         self.filename.replace('.py', '')],
                                         stdin = subprocess.PIPE,
                                         stdout = subprocess.PIPE,
                                         stderr = subprocess.PIPE)
        
        Thread(target=self.emuproc.communicate).start()


    def onDownloadRun(self, event):
        self.onCompile(event=None)
        from pynxc import download

        path = self.parent.dir + os.sep + self.filename

        f = open(path, "w")
        f.write(self.editor.GetText())
        f.close()
        
        out = download(path, run=True)

        if out != ('', ''):
            self.parent.showMsg(''.join(out))

    def onDownload(self, event):
        self.onCompile(event=None)
        from pynxc import download

        path = self.parent.dir + os.sep + self.filename

        f = open(path, "w")
        f.write(self.editor.GetText())
        f.close()

        out = download(path, run=False)

        if out != ('', ''):
            self.parent.showMsg(''.join(out))
            
        
    def clearStatusbar(self):
        self.parent.statusbar.SetStatusText("", 0)

class PreferencesDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 290))
        
        sizer = wx.GridBagSizer(8,3)
        itemsizer = wx.GridBagSizer(1, 3)
        sb = wx.StaticBox(self, label="nxtemu directory")
        boxsizer = wx.StaticBoxSizer(sb, wx.HORIZONTAL)
        
        self.i1 = wx.TextCtrl(self, -1, parent.cfg["nxtemu"], style=wx.EXPAND)
        b1 = wx.Button(self, -1, '...', style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.onDir, b1)
        ok = wx.Button(self, -1, 'Save and Apply', style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.onOk, ok)
        cancel = wx.Button(self, -1, 'Cancel', style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.onCancel, cancel)


        itemsizer.Add(self.i1, pos=(0,0), span=(1,3), flag=wx.EXPAND, border=3)
        itemsizer.Add(b1, pos=(0,3), border=3)
        itemsizer.AddGrowableCol(0)

        boxsizer.Add(itemsizer)
        sizer.Add(boxsizer, pos=(0,0), span=(1,3), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)
        sizer.Add(ok, pos=(8, 1), flag=wx.TOP|wx.RIGHT|wx.EXPAND, border=1)
        sizer.Add(cancel, pos=(8, 3), flag=wx.TOP|wx.RIGHT|wx.EXPAND, border=1)
        
        sizer.AddGrowableCol(0)  
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


    def onCancel(self,event):
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
    ID_FIND = 1010

    emuproc = None
    def __init__(self, parent):
        wx.aui.AuiMDIParentFrame.__init__(self, parent, -1,
                                          title = "nxted",
                                          size = (640,480),
                                          style = wx.DEFAULT_FRAME_STYLE)

        
        self.SetIcon(wx.Icon('icons/nxted_128.ico', wx.BITMAP_TYPE_ICO))

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

        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGING, self.tabChanged)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        self.OnNewChild(None)
        
        #self._mgr.Update()
        self.Show(True)
        
        # import config from yaml file
        self.cfg = yaml.load(open("config.yml").read())
        
        self.dir = tempfile.mkdtemp()
    
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

        item = self.menu.Append(self.ID_FIND, "Find\tCtrl+F")
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
        self.Bind(wx.EVT_MENU, self.OnQuit, item)
        

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
        return child
        

    def OnQuit(self, evt):
        #os.removedirs(self.dir)

        while self.GetActiveChild() != None:
            if self.GetActiveChild().onClose(None) == -1:
                return
        
        self.Destroy()

    def onPreferences(self, evt):
        pref = PreferencesDialog(self, -1, 'Preferences')
        pref.ShowModal()
        pref.Destroy()

    def titleUpdate(self):
        self.SetTitle("%s - %s" % (self.GetActiveChild().GetTitle(), 
                                   'nxted')
                     )

    def tabChanged(self, evt):
        wx.FutureCall(200, self.titleUpdate)

 
            
if __name__ == "__main__":
    if hasattr(sys, 'frozen'):
        app = wx.App(redirect=1, filename='nxted.exe.log')
    else:
        app = wx.App()
    Editor(None)
    app.MainLoop()
