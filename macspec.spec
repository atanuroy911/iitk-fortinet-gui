# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('img', 'img/.'), ('utils', 'utils/.')],
    hiddenimports=['PyQt5', 'plyer', 'pyobjus', 'plyer.platforms.macosx.notification', 'requests', 'sip', 'signal', 'getpass', 'argparse', 'logging'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=True,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='IITK Fortinet Authenticator',
)
app = BUNDLE(
    coll,
    name='IITK Fortinet Authenticator.app',
    icon='img/icon.icns',
    bundle_identifier='com.iitk.fortinet',
)
