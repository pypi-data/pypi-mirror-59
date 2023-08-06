# Copyright (c) 2019-2019 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

__all__ = ('__title__', '__summary__', '__uri__', '__version_info__',
           '__version__', '__author__', '__maintainer__', '__email__',
           '__copyright__', '__license__')

__title__        = "pyc_wheel"
__summary__      = "Compile all py files in a wheel to pyc files."
__uri__          = "https://pypi.org/project/pyc_wheel/"
__version_info__ = type("version_info", (), dict(serial=0,
                        major=1, minor=0, micro=3, releaselevel="final"))
__version__      = "{0.major}.{0.minor}.{0.micro}{1}{2}".format(__version_info__,
                   dict(final="", alpha="a", beta="b", rc="rc")[__version_info__.releaselevel],
                   "" if __version_info__.releaselevel == "final" else __version_info__.serial)
__author__       = "Grant Patten, Adam Karpierz"
__maintainer__   = "Adam Karpierz"
__email__        = "adam@karpierz.net"
__copyright__    = "Copyright (c) 2019-2019 {0}".format(__author__)
__license__      = "MIT License ; {0}".format(
                   "https://opensource.org/licenses/MIT")
