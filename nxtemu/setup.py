from distutils.core import setup
import os, glob, fnmatch
import py2exe
 
data_files = ['api.py']
#data_files.append('theme/default/*.*')
#data_files.append(('floor/line1.jpg', 'floor/line1.jpg'))

includes = []
excludes = [] #['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
           # 'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
           # 'Tkconstants', 'Tkinter']
packages = ['pygame', 'pygame.font']
dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll','tk84.dll']
extra_data = ['./theme/', './icons/', './floor/']


def find_data_files(self, srcdir, *wildcards, **kw):
    # get a list of all files under the srcdir matching wildcards,
    # returned in a format to be used for install_data
    def walk_helper(arg, dirname, files):
        names = []
        lst, wildcards = arg
        for wc in wildcards:
            wc_name = self.opj(dirname, wc)
            for f in files:
                filename = self.opj(dirname, f)

                if fnmatch.fnmatch(filename, wc_name) and not os.path.isdir(filename):
                    names.append(filename)
        if names:
            lst.append( (dirname, names ) )

    file_list = []
    recursive = kw.get('recursive', True)
    if recursive:
        os.path.walk(srcdir, walk_helper, (file_list, wildcards))
    else:
        walk_helper((file_list, wildcards),
                    srcdir,
                    [os.path.basename(f) for f in glob.glob(self.opj(srcdir, '*'))])
    return file_list

for data in extra_data:
    if os.path.isdir(data):
        data_files.extend(find_data_files(data, '*', recursive=True))
    else:
        data_files.append(('.', [data]))


#print find_data_files('theme', 'default/*', recursive=True)
#raw_input()



origIsSystemDLL = py2exe.build_exe.isSystemDLL # save the orginal before we edit it
def isSystemDLL(pathname):
    # checks if the freetype and ogg dll files are being included
    if os.path.basename(pathname).lower() in ("libfreetype-6.dll", "libogg-0.dll", "sdl_ttf.dll"):
            return 0
    return origIsSystemDLL(pathname) # return the orginal function
py2exe.build_exe.isSystemDLL = isSystemDLL


setup(
    options = {"py2exe": {"compressed": 2,
                          "optimize": 2,
                          "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          "bundle_files": 3,
                          "dist_dir": "../build/nxtemu/",
                          "xref": False,
                          "skip_archive": False,
                          "ascii": False,
                          "custom_boot_script": '',
                         },
             },
    data_files = data_files,
    windows=['nxtemu.py']
)
