# Alternative spec for directory mode (faster startup)
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('templates', 'templates')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'pandas', 'scipy', 'IPython', 'jupyter'],
    noarchive=False,
    optimize=2,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    [],
    exclude_binaries=True,
    name='Report Generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=True,
    upx=False,
    name='Report Generator',
)

app = BUNDLE(
    coll,
    name='Report Generator.app',
    icon='icons/app_icon.icns',
    bundle_identifier='com.yourcompany.berichtsheftgenerator',
)
