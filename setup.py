# coding=utf-8

import sys
import json
import os
from cx_Freeze import setup, Executable


name = "s2speech"
version = "0.4"
description = 'Scratch to Speech (python-OpenJTalk Speeth Synthesis)'
author = 'Hiroaki Kawashima'
url ='https://github.com/memakura/s2speech'

# 変更しない
upgrade_code = '{91FA8218-8094-4AF4-875E-4CBF25CF01AD}'

# ----------------------------------------------------------------
# セットアップ
# ----------------------------------------------------------------
shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "s2speech",                    # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]s2speech.exe",# Target
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

build_exe_options = {"packages": ['asyncio'],
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
exe = Executable(script='s2speech.py',
                 targetName='s2speech.exe',
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
