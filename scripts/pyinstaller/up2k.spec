# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['u2c.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'bz2',
        'ftplib',
        'getpass',
        'lzma',
        'pickle',
        'platform',
        'selectors',
        'ssl',
        'subprocess',
        'tarfile',
        'tempfile',
        'tracemalloc',
        'typing',
        'zipfile',
        'zlib',
        'email.contentmanager',
        'email.policy',
        'encodings.zlib_codec',
        'encodings.base64_codec',
        'encodings.bz2_codec',
        'encodings.charmap',
        'encodings.hex_codec',
        'encodings.palmos',
        'encodings.punycode',
        'encodings.rot_13',
        'urllib.response',
        'urllib.robotparser',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# this is the only change to the autogenerated specfile:
xdll = ["libcrypto-1_1.dll"]
a.binaries = [x for x in a.binaries if x[0] not in xdll]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='u2c',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='up2k.rc2',
    icon=['up2k.ico'],
)
