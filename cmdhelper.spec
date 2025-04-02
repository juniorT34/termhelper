block_cipher = None

a = Analysis(
    ['cmdhelper\\__main__.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('cmdhelper/data/*.yaml', 'cmdhelper/data'),
        ('cmdhelper/web/templates/*', 'cmdhelper/web/templates'),
        ('cmdhelper/web/static/*', 'cmdhelper/web/static')
    ],
    hiddenimports=[
        'rich.console',
        'rich.theme',
        'rich.table',
        'rich.prompt',
        'flask',
        'openai',
        'rapidfuzz',
        'argcomplete'
    ],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='cmdhelper',
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
)
