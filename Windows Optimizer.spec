# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['encrypted_launcher.py'],
    pathex=[],
    binaries=[],
    datas=[('key.txt', '.'), ('encrypted_code.txt', '.')],
    hiddenimports=['tkinter', 'cryptography', 'wmi', 'win32com.client', 'win32api', 'win32con', 'psutil', 'tkinter.ttk', 'webbrowser', 'subprocess', 'shutil', 'time'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
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
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
)
