
from waxy import *
import os, yaml, subprocess

__author__  = 'Brian Blais <bblais@bryant.edu>'
__version__ = (0,1,6)


def readconfig(fname):
    import yaml
    config={'firmware':'105'}
    
    if os.path.exists(fname):
        data=yaml.load(open(fname))        
        config.update(data)
    
    return config
 

class MainFrame(Frame):

    def Body(self):
        self.ReadConfig()
    
        self.nxc=os.path.join("nxc",sys.platform,'nbc')
        if not os.path.exists(self.nxc):
            nxc = 'nbc' # expect 'nbc' in the binary PATH

        self.prog=None

        self.CreateMenu()
        
        self.textbox = TextBox(self, multiline=1, readonly=1,
                       Font=Font("Courier New", 10), Size=(650,500),
                       Value='PyNXC Version '+str(__version__)+"\n" + 
                       "Firmware Version "+self.firmware_version+"\n")
        self.AddComponent(self.textbox, expand='both')

        self.Pack()
        self.CenterOnScreen()
        
        cmdlist=[self.nxc]
        self.DoCmd(cmdlist)
        
        self.ResetTitle()
        
    def ReadConfig(self):
    
        config=readconfig('pynxc.yaml')
        self.firmware_version=str(config['firmware'])
            
    def UpdateConfig(self):
    
        config={'firmware':self.firmware_version}
        with open("pynxc.yaml",'w') as fid:
            yaml.dump(config,fid,default_flow_style=False)
    
    def CreateMenu(self):
    
        
        menubar = MenuBar()
        
        menu1 = Menu(self)
        menu1.Append("L&oad Program File", self.Load, "Load a .py file",hotkey="Ctrl+O")
        menu1.Append("&Quit", self.Quit, "Quit",hotkey="Ctrl+Q")
        menubar.Append(menu1, "&File")
        
        menu1 = Menu(self)
        menu1.Append("Con&vert", self.OnlyConvert)
        menu1.Append("&Compile", self.Compile,hotkey="Ctrl+C")
        menu1.Append("Compile and &Download", self.Download,hotkey="Ctrl+D")
        menubar.Append(menu1, "&Program")
        self.menubar=menubar

        self.nxt_menu = Menu(self)
        self.nxt_menu.Append("&Info", self.NXT_Info)
        self.bluetooth_menu=self.nxt_menu.Append("Enable &Bluetooth", type='check')
        
        submenu=Menu(self)
        self.firmware_menus=[
            submenu.Append("Version 105",type='radio',event=self.FirmwareVersion),
            submenu.Append("Version 107",type='radio',event=self.FirmwareVersion),
            submenu.Append("Version 128",type='radio',event=self.FirmwareVersion),
        ]
        if self.firmware_version=='107':
            self.firmware_menus[1].Check(True)
        elif self.firmware_version=='128':
            self.firmware_menus[2].Check(True)
        else:
            self.firmware_menus[0].Check(True)
            self.firmware_version='105'
            self.UpdateConfig()
            
        self.nxt_menu.AppendMenu("Firmware",submenu)
        
        self.menubar.Append(self.nxt_menu, "&NXT")
            
            
        self.SetMenuBar(menubar)

        
    def FirmwareVersion(self,event):
        versions={'Version 105':'105',
        'Version 107':'107',
        'Version 128':'128',
        }
    
        for menu in self.firmware_menus:
            if menu.IsChecked():
                self.firmware_version=versions[menu.Label]
                self.UpdateConfig()
                
        
        
    def Load(self,event=None):
        dlg = FileDialog(self, 'Select a Program File',default_dir=os.getcwd(),wildcard='*.py',open=1)
        try:
            result = dlg.ShowModal()
            if result == 'ok':
                self.prog = dlg.GetPaths()[0]
                self.ResetTitle()
        finally:
            dlg.Destroy()
    
    def ResetTitle(self,event=None):
        if self.prog:
            junk,fname=os.path.split(self.prog)
            s='PyNXC: %s' % fname
        else:
            s='PyNXC'
            
        self.SetTitle(s)
        
            
    def NXT_Info(self,event=None):
        pass
    
    def Quit(self,event=None):
        self.Close()

    def DoCmd(self,cmdlist):
        
        S=self.textbox.GetValue()
        S=S+"#-> "+" ".join(cmdlist)+"\n"
        self.textbox.SetValue(S)
        
        print cmdlist

        try:

            if sys.platform=='win32':
                output=subprocess.Popen(
                    cmdlist,stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            else:
                output=subprocess.Popen(
                    cmdlist,stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)

            try: # there might be non-ASCII chars in the output
                S += output.stdout.read() + output.stderr.read()
            except UnicodeDecodeError:
                S += (output.stdout.read() + output.stderr.read()
                     ).decode('utf-8', 'replace')
            
            self.textbox.SetValue(S)
                
        except OSError:
            
            s=sys.exc_info()
            S=S+"Error with NXC Executable: "+str(s[1])
            self.textbox.SetValue(S)
            return
                
                
            
    def Convert(self):
        filename=self.prog

#        path,fname=os.path.split(filename)
        root,ext=os.path.splitext(filename)
        
        nxc_filename=root+".nxc"
        
        S=self.textbox.GetValue()
        
        S=S+"Writing %s..." % (nxc_filename)
        self.textbox.SetValue(S)
        
        python_to_nxc(filename,nxc_filename)
        
        
        S=S+".done\n"
        self.textbox.SetValue(S)
        
        return nxc_filename

    
    def OnlyConvert(self,event=None):
        self.textbox.SetValue("")
        
        if not self.prog:
            self.Load()
            
        if not self.prog:
            dlg = MessageDialog(self, "Error","No Program File Selected")
            dlg.ShowModal()
            dlg.Destroy()
            return
            
        try:
            nxc_filename=self.Convert()
        except:
            s=sys.exc_info()
            str1="Error in "+self.prog +": "+str(s[1])
            self.textbox.SetValue(str1)
            return

    def Compile(self,event=None):
        self.textbox.SetValue("")
        
        if not self.prog:
            self.Load()
            
        if not self.prog:
            dlg = MessageDialog(self, "Error","No Program File Selected")
            dlg.ShowModal()
            dlg.Destroy()
            return
            
        try:
            nxc_filename=self.Convert()
        except:
            s=sys.exc_info()
            str1="Error in "+self.prog +": "+str(s[1])
            self.textbox.SetValue(str1)
            return


        root,ext=os.path.splitext(nxc_filename)
        rxe_filename=root+".rxe"
        
        
        
        cmdlist=[self.nxc,nxc_filename," -v=%s" % self.firmware_version," -O=%s" % rxe_filename]
        
        self.DoCmd(cmdlist)
            

   
    def Download(self,event=None):
        
        self.textbox.SetValue("")
        
        if not self.prog:
            self.Load()
            
        if not self.prog:
            dlg = MessageDialog(self, "Error","No Program File Selected")
            dlg.ShowModal()
            dlg.Destroy()
            return
            
        try:
            nxc_filename=self.Convert()
        except:
            s=sys.exc_info()
            str1="Error in "+self.prog +": "+str(s[1])
            self.textbox.SetValue(str1)
            return

        flags=['-d','-S=usb','-v=%s' % self.firmware_version]
        if self.bluetooth_menu.IsChecked():
            flags.append('-BT')
            
        root,ext=os.path.splitext(nxc_filename)
        rxe_filename=root+".rxe"
        cmdlist=[self.nxc]
        cmdlist.extend(flags)
        cmdlist.append(nxc_filename)
        
        self.DoCmd(cmdlist)

        root,ext=os.path.split(self.nxc)
        nxtcom=os.path.join(root,'nxtcom_scripts/nxtcom')
        print nxtcom
        if os.path.exists(nxtcom):
            print "Downloading...",
            cmd='%s %s' % (nxtcom,rxe_filename)
            a=os.system(cmd)
            print "done."
       
