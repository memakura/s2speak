# coding=utf-8

import sys
import json
import os
from cx_Freeze import setup, Executable

# --- for resolving KeyError: 'TCL_LIBRARY' ---
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')
# ------

name = "s2speak"
version = "0.5"
description = 'Offline Speech Synthesis'
author = 'Hiroaki Kawashima'
url ='https://github.com/memakura/s2speak'

# 変更しない
upgrade_code = '{91FA8218-8094-4AF4-875E-4CBF25CF01AD}'

# ----------------------------------------------------------------
# セットアップ
# ----------------------------------------------------------------
shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "s2speak",                    # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]s2speak.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     "TARGETDIR",              # WkDir
    )
    ]

# Now create the table dictionary
msi_data = {"Shortcut": shortcut_table}

build_exe_options = {"packages": ['asyncio', 'idna'],
                    "excludes": [],
                    "includes": [],
                    "include_files": ['jtalk/','htsvoices/','images/','00scratch/', 'ThirdPartyLicenses.txt']
}
#                    "compressed": True


bdist_msi_options = {'upgrade_code': upgrade_code,
                    'add_to_path': False,
                    'data': msi_data
}

options = {
    'build_exe': build_exe_options,
    'bdist_msi': bdist_msi_options
}

# exeの情報
base = None #'Win32GUI' if sys.platform == 'win32' else None
icon = 'images/icon_256x256.ico'

# exe にしたい python ファイルを指定
exe = Executable(script='s2speak.py',
                 targetName='s2speak.exe',
                 base=base,
                 icon=icon
                 )
#                 copyDependentFiles = True

# セットアップ
setup(name=name,
      version=version,
      author=author,
      url=url,
      description=description,
      options=options,
      executables=[exe]
      )
