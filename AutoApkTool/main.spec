import os
import sys

# 获取当前 spec 文件所在的绝对路径
spec_dir = os.path.dirname(os.path.abspath(SPEC))

a = Analysis(
    [os.path.join(spec_dir, "main.py")],
    pathex=[spec_dir],
    binaries=[],
    datas=[
        (os.path.join(spec_dir, "locales"), "locales"),
        (os.path.join(spec_dir, "cert"), "cert"),
        (os.path.join(spec_dir, "win"), "win"),
        (os.path.join(spec_dir, "terminal_configs"), "terminal_configs"),
        (os.path.join(spec_dir, "Env"), "Env"),
        (os.path.join(spec_dir, "apktool.jar"), "."),
        (os.path.join(spec_dir, "DEF_APK", "LargeApp.apk"), "DEF_APK"),
        (os.path.join(spec_dir, "DEF_APK", "SmallApp.apk"), "DEF_APK"),
        (os.path.join(spec_dir, "DEF_APK", "Screenless.apk"), "DEF_APK"),
        (os.path.join(spec_dir, "input.json"), "."),
    ],
    hiddenimports=[
        "modules",
        "modules.ui",
        "modules.ui.main_window",
        "modules.ui.tabs",
        "modules.apk_tools",
        "modules.backend",
        "modules.constants",
        "modules.env_checker",
        "modules.i18n",
        "modules.utils",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# 关键：移除 COLLECT，创建单文件
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="main",
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
    icon=os.path.join(spec_dir, "png", "icons", "8m465-bddl0-001.ico"),
)
