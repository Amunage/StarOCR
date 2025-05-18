# __init__.spec
block_cipher = None
base_path = os.getcwd()

a = Analysis(
    ['__init__.py'],
    pathex=['.'],
    binaries=[],
    datas=[(f"{base_path}/Tesseract-OCR", "tesseract")],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='StarOCR',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    uac_admin=True,
    icon=f'{base_path}/data/scricon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='StarOCR'
)
