# AutoApkTool

AutoApkTool 是一个基于 Python 和 CustomTkinter 开发的 Android 应用自动化定制与打包工具。它可以帮助开发者或实施人员快速反编译 APK、动态修改配置信息（如 DNS、环境节点、按键映射、语音编码、地图源等）、并重新签名打包出目标应用。

## 核心功能
- **一键反编译与回编译**：内置 `apktool` 与 `zipalign`、`apksigner`，提供顺畅的拆包与打包体验。
- **环境切换**：支持预设环境（海外环境、国内环境）的快速切换，以及自定义（独立部署）节点的快速配置。
- **动态按键捕获**：通过监听 ADB 的 Logcat，实时捕获硬件设备的实体按键（PTT、SOS），并动态生成按键映射文件（`input.json`）。
- **多终端支持**：支持大屏、中屏、小屏和无屏设备的不同底包选择。
- **多语言与国际化**：内置中英文切换功能。
- **可视化配置**：图形化界面提供音效配置（编解码、通道）、地图引擎设置、以及 Launcher 桌面化切换。
- **历史配置导入**：可从 `terminal_configs` 中快速导入不同硬件厂商的适配文件。

## 目录结构
```text
AutoApk/
├── script/
│   ├── main.py                  # 项目启动入口
│   ├── SmallApkTools.py         # 命令行模式的按键捕获独立工具
│   ├── apktool.jar              # Apktool 核心包
│   ├── input.json               # 动态生成的按键配置文件
│   ├── cert/                    # 签名证书目录（.jks, .keystore 等）
│   ├── locales/                 # 国际化语言包 (zh.json, en.json)
│   ├── terminal_configs/        # 厂商终端配置预设文件
│   └── modules/                 # 重构后的项目核心逻辑
│       ├── apk_tools.py         # APK 处理核心逻辑（解压、打包、签名）
│       ├── backend.py           # ADB 监听与按键映射生成逻辑
│       ├── constants.py         # 全局常量及环境节点定义
│       ├── env_checker.py       # Java 与 ADB 环境检测模块
│       ├── i18n.py              # 多语言国际化实现
│       ├── utils.py             # JSON、YAML 及 XML 文件操作辅助函数
│       └── ui/                  # UI 界面模块
│           ├── main_window.py   # 主窗口框架
│           └── tabs.py          # 独立拆分的标签页（Config, Build, LED, Terminal）
├── win/                         # Windows 工具链（zipalign, apksigner 等）
├── requirements.txt             # Python 依赖清单
└── README.md                    # 本帮助文档
```

## 环境要求
1. **操作系统**: Windows 10/11 推荐。
2. **Python**: Python 3.8 及以上版本。
3. **Java**: JDK 17 及以上版本（需要将 `java` 命令加入环境变量）。
4. **ADB**: Android Platform Tools（需要将 `adb` 命令加入环境变量）。

## 安装依赖
在项目根目录运行以下命令安装依赖：
```bash
pip install -r requirements.txt
```

## 运行程序
确保终端在 `script` 目录下，或者指定完整路径运行：
```bash
cd script
python main.py
```

## 常见问题排查
1. **提示 ADB/Java 环境缺失**:
   请检查 `java -version` 和 `adb version` 是否能在终端正常输出。如果不能，请下载相应的工具并配置到系统的 `PATH` 环境变量中。
2. **打包失败或签名失败**:
   请检查 `cert` 目录下的签名证书是否存在，并在 `modules/constants.py` 中的 `KEYSTORE_CONFIG` 里确认密码是否正确。
3. **ADB 监听按键无反应**:
   确保设备已开启“USB调试”，并且电脑已对设备授权。可以使用 `SmallApkTools.py` 单独测试按键日志。

## 注意事项
- 该工具修改 `AndroidManifest.xml` 与 `slclient.json` 可能会导致应用行为变更，建议先备份原有的 APK。
- 只有被 `Apktool` 支持的 APK 才可被正常反编译和回编译。
