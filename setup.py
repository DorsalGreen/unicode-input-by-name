"""Distutils setup script."""

import meta

import sys
import os
import re
from glob import glob



from distutils.core import setup

#If we want to build a py2exe dist, patch distutils with py2exe
try:
    if 'py2exe' in sys.argv:
        import py2exe
except ImportError:
    pass

#If we want to build a egg dist, patch distutils with setuptools
try:
    if 'bdist_egg' in sys.argv:
        from setuptools import setup
except ImportError:
    pass


exclude_packages = ["Tkconstants", "Tkinter", "tcl", 'pydoc', '_ssl']
data_files = ['LICENSE.txt', 'README.txt', 'msvcp90.dll',
              'Microsoft.VC90.CRT.manifest']

if 'install' in sys.argv:
    raise RuntimeError('Install not yet supported, please just run uibn.pyw')

setup(name=meta.APPNAME_SHORT,
      version=meta.VERSION,
      description=meta.DESCRIPTION,
      author=meta.AUTHOR,
      author_email=meta.AUTHOR_EMAIL,
      license = "MIT",
      url = meta.URL,
      options = {'py2exe': {'dist_dir': 'bin',
                            'excludes': exclude_packages,
                            'bundle_files': 3
                            }
                },
      windows= [{'script': 'uibn.pyw',
                 'icon_resources': [(1, 'resources/upsilon.ico')],
                 'other_resources': [(24,1,meta.MANIFEST)]
                 }],
      scripts = ['uibn.pyw'],
      data_files = [('', data_files)],
      )
