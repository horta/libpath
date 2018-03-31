import platform
from os.path import join

from libpath import Unix, Windows

if platform.system() == 'Windows':
    s = Windows()
    f = s.get_programfiles()
    s.add_library_dir(join(f, 'zstd', 'lib'))
    s.add_include_dir(join(f, 'zstd', 'include'))
    libs = [s.find_libname('zstd')]
else:
    s = Unix()
    libs = ['zstd']

include_dirs = s.get_include_dirs()
library_dirs = s.get_library_dirs()

print(libs, include_dirs, library_dirs)
