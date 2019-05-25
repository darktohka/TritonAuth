# -*- mode: python -*-

block_cipher = None

a = Analysis(['../start.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=['PyQt5'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='TritonAuth',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          console=False, icon='icon.ico')
app = BUNDLE(exe,
             name='TritonAuth.app',
             icon='icon.icns',
             bundle_identifier=None)