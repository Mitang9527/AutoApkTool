# AutoApkTool

AutoApkTool 是一款专为 Android 自动化测试和 APK 定制设计的工具。它集成了 APK 反编译、配置修改、自动重包、签名以及实时按键事件监听功能，旨在简化 Android 设备的适配和调试流程。

## 核心功能

- **APK 反编译与重包**：集成 `Apktool`，支持一键反编译 APK 并重新打包。
- **配置自动同步**：支持将本地 `input.json`、`slclient.json` 等配置文件自动同步到 APK 内部。
- **签名与对齐**：内置 `zipalign` 和 `apksigner`，确保生成的 APK 符合发布标准。
- **内置 APK 支持**：集成大屏、中屏、小屏及无屏四种预设 APK 模板，支持一键快速适配。
- **实时按键监听**：通过 ADB 实时捕获设备的 Intent 事件（如 PTT、SOS 按键），并自动生成对应的 `input.json` 配置项。
- **国际化支持**：支持中英文双语界面切换。
- **终端配置管理**：内置大量预设终端配置文件，支持快速导入和应用。

## 环境要求

在运行或打包本项目前，请确保您的系统已安装以下组件：

1. **Java JDK (1.8 或更高版本)**：用于运行 `Apktool`。
2. **ADB (Android Debug Bridge)**：用于设备通信和事件监听。
3. **Python 3.8+**：开发和运行环境。

> **注意**：项目 `Env` 目录下提供了部分环境组件的压缩包供参考。

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python AutoApkTool/main.py
```

## 打包说明

本项目支持使用 `PyInstaller` 打包成单文件 EXE，方便在没有 Python 环境的机器上运行。

### 打包命令

在项目根目录下运行：

```powershell
pyinstaller AutoApkTool/main.spec
```

打包完成后，单文件 EXE 将生成在 `dist` 目录下。该 EXE 已内置所有必要的资源（locales, win 工具链, cert, 默认 APK 等）。

## 项目结构

- `AutoApkTool/main.py`: 程序入口。
- `AutoApkTool/modules/`: 逻辑模块，包含 UI、后端、环境检查、APK 工具等。
- `AutoApkTool/locales/`: 国际化 JSON 语言包。
- `AutoApkTool/win/`: Windows 平台下的工具链（aapt, zipalign, apksigner 等）。
- `AutoApkTool/cert/`: APK 签名所需的证书文件。
- `AutoApkTool/terminal_configs/`: 预设的各型号终端配置文件。

## 开发规范

- **代码格式**：使用 `Black` 进行代码格式化。
- **日志输出**：程序内部日志（Log Tab）统一使用英文输出，确保兼容性。
- **路径处理**：使用 `RESOURCE_PATH` 访问只读资源，使用 `WORKSPACE_PATH` 访问用户生成的文件。

## 许可证

[待补充]
