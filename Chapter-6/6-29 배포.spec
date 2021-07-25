# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['6-29 배포.py'],
             pathex=['C:\\tech\\TradingBot-BearU\\Chapter-6'],
             binaries=[('C:\\tech\\TradingBot-BearU\\Chapter-6\\5-25.ui', '.')],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='6-29 배포',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='C:\\tech\\TradingBot-BearU\\Chapter-6\\icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='program')
