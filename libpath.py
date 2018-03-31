import os
import platform
from os.path import join, exists
from sysconfig import get_config_var
import struct

__version__ = "0.0.1"


def bits_arch():
    return struct.calcsize("P") * 8


class System(object):
    def __init__(self):
        self._library_dirs = []
        self._include_dirs = []

    def add_library_dir(self, d):
        self._library_dirs.append(d)

    def add_include_dir(self, d):
        self._include_dirs.append(d)


class Windows(System):

    def get_programfiles(self):
        if bits_arch() == 32:
            return self.get_32bits_programfiles()
        return self.get_64bits_programfiles()

    def get_64bits_programfiles(self):
        n = 'PROGRAMW6432'
        if n not in os.environ:
            raise RuntimeError("{} variable is not defined.".format(n))

        f = os.environ[n]
        if not exists(f):
            raise RuntimeError("Could not find {}.".format(f))

        return f

    def get_32bits_programfiles(self):
        n = 'PROGRAMFILES'
        if n not in os.environ:
            raise RuntimeError("{} variable is not defined.".format(n))

        f = os.environ[n]
        if not exists(f):
            raise RuntimeError("Could not find {}.".format(f))

        return f

    def get_include_dirs(self):
        dirs = [join(get_config_var('prefix'), 'include')]

        names = ['INCLUDE', 'LIBRARY_INC']
        vals = [os.environ[n] for n in names if n in os.environ]
        dirs += [d for v in vals for d in v.split(';')]

        dirs = [d for d in dirs if len(d) > 0 and exists(d)]
        return self._include_dirs + dirs

    def get_library_dirs(self):
        dirs = [join(get_config_var('prefix'), 'lib')]

        names = ['LIBRARY_LIB']
        vals = [os.environ[n] for n in names if n in os.environ]
        dirs += [d for v in vals for d in v.split(';')]

        dirs = [d for d in dirs if len(d) > 0 and exists(d)]
        return self._library_dirs + dirs

    def find_libname(self, name):
        names = ["{}.lib", "lib{}.lib", "{}lib.lib"]
        names = [n.format(name) for n in names]
        dirs = self.get_library_dirs()
        for d in dirs:
            for n in names:
                if exists(join(d, n)):
                    return n[:-4]
        msg = "Could not find the library name for {}.".format(name)
        raise ValueError(msg)

    def __str__(self):
        msg = "Arch: {}bits\n".format(bits_arch())
        if bits_arch() == 32:
            msg += "ProgramFiles: {}\n".format(self.get_32bits_programfiles())
        if bits_arch() == 64:
            msg += "ProgramFiles32: {}\n".format(
                self.get_32bits_programfiles())
            msg += "ProgramFiles64: {}\n".format(
                self.get_64bits_programfiles())
        msg += "Include dirs: {}\n".format(self.get_include_dirs())
        msg += "Library dirs: {}\n".format(self.get_library_dirs())
        return msg


class Unix(System):

    def get_include_dirs(self):
        dirs = [join(get_config_var('prefix'), 'include')]
        dirs += ['/usr/include', '/usr/local/include']
        dirs = [d for d in dirs if len(d) > 0 and exists(d)]
        return self._include_dirs + dirs

    def get_library_dirs(self):
        dirs = [join(get_config_var('prefix'), 'lib')]
        dirs += ['/usr/lib', '/usr/local/lib']
        dirs = [d for d in dirs if len(d) > 0 and exists(d)]
        return self._library_dirs + dirs

    def __str__(self):
        msg = "Arch: {}bits\n".format(bits_arch())
        msg += "Include dirs: {}\n".format(self.get_include_dirs())
        msg += "Library dirs: {}\n".format(self.get_library_dirs())
        return msg


if __name__ == "__main__":
    if platform.system() == 'Windows':
        w = Windows()
        pf = w.get_programfiles()
        w.add_library_dir(join(pf, 'zstd', 'lib'))
        w.add_include_dir(join(pf, 'zstd', 'include'))
        print(w)
        print(w.find_libname('zstd'))
    else:
        print(Unix())
