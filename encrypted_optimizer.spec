# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['encrypted_launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('key.txt', '.'),
        ('encrypted_code.txt', '.'),
    ],
    hiddenimports=['cryptography', 'wmi', 'win32com.client', 'win32api', 'win32con', 'psutil'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Windows Optimizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
    icon='C:\\Users\\Agustin\\Desktop\\windows optimizer\\icon.ico'
) 