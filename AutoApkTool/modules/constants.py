import os
from pathlib import Path

# ==================== 全局配置常量 ====================

# 路径配置
PROJECT_PATH = Path(os.getcwd())
JSON_FILE = "input.json"
TEMP_DIR = "app_out"
APKTOOL_JAR = "apktool.jar"

# 环境配置
ENV_CONF = {
    "overseas": {
        "ip_address": "sgdns.shanlipoc.com:10200,usdns.shanlipoc.com:10200",
        "context": "pocstar",
        "upgrade_url": "upgrade.pocstar.com"
    },
    "domestic_v2": {
        "ip_address": "cndns.shanliptt.com:10200",
        "context": "show",
        "upgrade_url": "upgrade.shanliptt.com"
    },
}

# 2. 显示名称映射
ENV_DISPLAY_NAMES = {
    "overseas": {"zh": "海外环境", "en": "Overseas Env"},
    "domestic_v2": {"zh": "国内环境2.0", "en": "Domestic 2.0"}
}

LOGIN_TYPE_MAPPING = {
    "account": {"zh": "账号登录", "en": "Account Login"},
    "serial": {"zh": "IMEI登录", "en": "IMEI Login"},
    "iccid": {"zh": "ICCID登录", "en": "ICCID Login"}
}

MAP_CONFIG_TEMPLATES = {
    "baidu_domestic": {
        "display_name": {"zh": "百度 [国内]", "en": "Baidu [Domestic]"},
        "config": {
            "enabled": True,
            "report": True,
            "map_type": "baidu",
            "provider": "baidu",
            "coor": "bd09ll",
            "update_period_sec": 40,
            "report_period_sec": 40
        }
    },
    "baidu_oversea": {
        "display_name": {"zh": "百度 [海外]", "en": "Baidu [Oversea]"},
        "config": {
            "enabled": True,
            "report": True,
            "map_type": "baidu",
            "provider": "baidu",
            "coor": "wgs84",
            "update_period_sec": 40,
            "report_period_sec": 40
        }
    },
    "google": {
        "display_name": {"zh": "谷歌", "en": "Google"},
        "config": {
            "enabled": True,
            "report": True,
            "map_type": "google",
            "provider": "google",
            "coor": "wgs84",
            "update_period_sec": 40,
            "report_period_sec": 40
        }
    },
    "none": {
        "display_name": {"zh": "GPS", "en": "GPS"},
        "config": {
            "enabled": True,
            "report": True,
            "map_type": "none",
            "provider": "default",
            "coor": "wgs84",
            "update_period_sec": 40,
            "report_period_sec": 40
        }
    }
}

# 关键文件路径
PATH_YML = PROJECT_PATH / "app_out" / "apktool.yml"
PATH_ASS = PROJECT_PATH / "app_out" / "assets"
PATH_SLCLIENT = PROJECT_PATH / "app_out" / "assets" / "slclient"
PATH_SLCLIENT_JSON = PROJECT_PATH / "app_out" / "assets" / "slclient.json"
PATH_INPUT_JSON_SRC = "input.json"
PATH_INPUT_JSON_DST = PROJECT_PATH / "app_out" / "assets" / "slclient" / "input.json"

# 命名空间（确保与 manifest 中一致）
ANDROID_NAMESPACE = "http://schemas.android.com/apk/res/android"
PATH_MANIFEST_XML = PROJECT_PATH / "app_out" / "AndroidManifest.xml"

# 签名配置
KEYSTORE_BIG = PROJECT_PATH / "cert" / "shanli.jks"
KEYSTORE_SMALL = PROJECT_PATH / "cert" / "shanlitech.keystore"

KEYSTORE_CONFIG = {
    "large": {"path": KEYSTORE_BIG, "password": "123456"},
    "middle": {"path": KEYSTORE_BIG, "password": "123456"},
    "small": {"path": KEYSTORE_SMALL, "password": "Lgsj829517"},
    "none": {"path": KEYSTORE_SMALL, "password": "Lgsj829517"},
}

# 工具链路径
ZIPALIGN_EXE = PROJECT_PATH / "win" / "zipalign.exe"
APKSIGNER_BAT = PROJECT_PATH / "win" / "apksigner.bat"

# 业务常量
LAUNCHER_MODULE_PATH = ["ui", "launcherModule"]
RECORDER_ENABLE_PATH = ["recorder", "enable"]

LBS_COOR_PATH = ["lbs", "coor"]
LBS_MAP_PYPE = ["lbs", "map_type"]

DEFAULT_CUSTOM_LIST = [
    "join_next_group",
    "switch_group_name_tts",
    "switch_group_click",
    "join_prev_group",
    "new_call_in"
]

SKIP_FEEDBACK_INTERVAL = 5
DEBOUNCE_SECONDS = 1.5
