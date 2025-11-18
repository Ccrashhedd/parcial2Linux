# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Sistema POS Restaurante
# Actualizado: Noviembre 2025

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('DB', 'DB')],
    hiddenimports=[
        'psycopg2', 
        'psycopg2.extensions', 
        'psycopg2.pool',
        'psycopg2.extras',
        'conexionDB',
        'interfaz_restaurante',
        'modelo_restaurante',
        'dialogo_impresion',
        'dialogo_login',
        'visor_productos',
        'verificar_menu_dia',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=1,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='parcial2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin consola para aplicación GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Aquí puedes agregar un ícono si tienes uno
)
