#!/usr/bin/env python
from __future__ import with_statement

__author__  = 'Brian Blais <bblais@bryant.edu>'
__version__ = (0,1,6)

import sys
from compiler import parse, walk
from compiler.consts import *
import os
import subprocess
from optparse import OptionParser
import re

from first_pass import *
from second_pass import *
from definitions import *

#pynxc_root=os.getcwd()

pynxc_root = os.path.dirname(os.path.abspath(__file__)) \
                .replace("library.zip", "")
   
def python_to_nxc(pyfile,nxcfile=None,debug=False):

    filename = pyfile
    
    f = open(filename, 'U')
    codestring = f.read()
    f.close()

    if codestring and codestring[-1] != '\n':
        codestring = codestring + '\n'
        
    filestr = codestring
    
    
    defines=re.findall('\s*DEFINE (.*?)=(.*)',filestr)
    filestr=re.sub('\s*DEFINE (.*?)=(.*)',"",filestr)
    
    
    if debug:
        print "Filestr"
        print filestr
    
    ast = parse(filestr)
    v = FirstPassVisitor(debug=debug)
    v.v(ast)
    
    # print "variables assign:", v.variables_assign

    v.defines=defines
    
    if nxcfile:
        fid=open(nxcfile,'wt')
    else:
        fid=sys.stdout
        
    v2 = SecondPassVisitor(v,debug=debug,stream=fid, root=pynxc_root)
    v2.v(ast)
    v2.flush()


    if not fid==sys.stdout:
        fid.close()
    
def download(filename, run=False):
    nxc_file = filename.replace('.py', '.nxc')
    
    python_to_nxc(filename, nxc_file)

    nxc = pynxc_root + os.sep + os.path.join("nxc",sys.platform,'nbc')
    
    cmd = [nxc]
    cmd.append("-d")
    cmd.append("-S=usb")
    cmd.append("-v=128")
    if run:
        cmd.append("-r")
    cmd.append(nxc_file)
    
    proc = subprocess.Popen(cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE)

    out, err = proc.communicate()
    
    return (out, err)


    

def readconfig(fname):
    import yaml
    config={'firmware':'105'}
    
    if os.path.exists(fname):
        data=yaml.load(open(fname))        
        config.update(data)
    
    return config
    
def main():

    config=readconfig('pynxc.yaml')
    nxc=os.path.join("nxc",sys.platform,'nbc')
    if not os.path.exists(nxc):
        nxc = 'nbc' # expect 'nbc' in the binary PATH

    usage="usage: %prog [options] [filename]"
    parser = OptionParser(usage=usage)

    parser.add_option('-c', '--compile', dest="compile",
                      help='compile to nxc code only',default=False,
                      action="store_true")
    parser.add_option('--debug', dest="debug",
                      help='show debug messages',default=False,
                      action="store_true")
    parser.add_option('--show_nxc', dest="show_nxc",
                      help='show the nxc code',default=False,
                      action="store_true")
    parser.add_option('-d', '--download', dest="download",
                      help='download program',default=False,
                      action="store_true")
    parser.add_option('-B', '--bluetooth', dest="bluetooth",
                    help='enable bluetooth',default=False,
                    action="store_true")
    parser.add_option('--firmware', dest="firmware",
                      help='firmware version (105, 107, or 128)',default=config['firmware'])
    parser.add_option('--command',  dest="nxc",
                      help='what is the nxc/nqc command',default=nxc,
                      metavar="<command>")
                      
                  
    options, args = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        raise SystemExit
    
    options.firmware=config['firmware']

    # sanity check on the options
    
    if (options.download) and (options.compile):
        print "conflicting options"
        parser.print_help()
        raise SystemExit
        
    
    nxc_root,nxc=os.path.split(options.nxc)
    s=nxc.lower()

    filename = args[0]

    for filename in args:

        root,ext=os.path.splitext(filename)
        
        nxc_filename=root+".nxc"
        rxe_filename=root+".rxe"
        
        python_to_nxc(filename,nxc_filename,debug=options.debug)
        print "Wrote %s." % (nxc_filename)

        if options.show_nxc:
            fid=open(nxc_filename)
            print fid.read()
            fid.close()
            
        if not options.compile:
        
            cmd=options.nxc+" "
            if options.bluetooth:
                cmd+=' -BT '
                
            cmd=cmd+ "'%s'" % nxc_filename+ " -I='%s' -I=%s/ -v=%s -O='%s'" % (nxc_root,
                                                           pynxc_root,
                                                           options.firmware,
                                                           rxe_filename)
            print cmd
            a=os.system(cmd)
    
            if options.download:
                print "Downloading...",
                cmd=options.nxc+" "
                cmd=cmd+ nxc_filename+ " -I='%s/' -S=usb -I='%s/' v=%s -d" % (nxc_root,
                                                          pynxc_root,
                                                          options.firmware)
                a=os.system(cmd)
                nxtcom=os.path.join(nxc_root,'nxtcom')
                print nxtcom
                if os.path.exists(nxtcom):
                    cmd='%s %s' % (nxtcom,rxe_filename)
                    a=os.system(cmd)

                print "done."
        
            
    return


        
if __name__ == "__main__":
    if len(sys.argv) == 3:
        if sys.argv[1] == "ddd":
            download(sys.argv[2])
    elif len(sys.argv)<2:  # no args given, launch gui
        from gui import *
        app = Application(MainFrame, title="PyNXC")
        app.Run()
    else:
        sys.exit(main())
    
