import os
import json
import re
import shutil
import time
import traceback
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from typing import List, Any, Optional, Dict
from tkinter import messagebox
from ruamel.yaml import YAML
from .constants import (
    PATH_SLCLIENT_JSON,
    LOGIN_TYPE_MAPPING,
    MAP_CONFIG_TEMPLATES,
    LBS_COOR_PATH,
    LBS_MAP_PYPE,
    ANDROID_NAMESPACE,
    PATH_MANIFEST_XML,
)
from .i18n import i18n, _

# ==================== slclient.json处理 ====================


def update_slclient_login_type(login_type_ui: str) -> bool:
    """
    更新slclient.json中的profile.login_mode字段
    """
    if not PATH_SLCLIENT_JSON.exists():
        messagebox.showerror("ERROR", f"Please unzip apk first")
        return False

    login_mode_val = "account"  # 默认值
    for storage_key, names_dict in LOGIN_TYPE_MAPPING.items():
        if (
            names_dict.get("zh") == login_type_ui
            or names_dict.get("en") == login_type_ui
        ):
            login_mode_val = storage_key
            break

    try:
        with open(PATH_SLCLIENT_JSON, "r", encoding="utf-8") as f:
            slclient_data = json.load(f)

        slclient_data.setdefault("profile", {})["login_mode"] = login_mode_val

        with open(PATH_SLCLIENT_JSON, "w", encoding="utf-8") as f:
            json.dump(slclient_data, f, indent=2, ensure_ascii=False)

        return True

    except Exception as e:
        messagebox.showerror("修改失败", f"更新slclient.json出错：\n{str(e)}")
        traceback.print_exc()
        return False


def update_slclient_map_type(map_source_key: str) -> bool:
    """
    更新slclient.json中的地图源配置
    """
    if not PATH_SLCLIENT_JSON.exists():
        print(f"[Error] File not found: {PATH_SLCLIENT_JSON}")
        return False

    try:
        with open(PATH_SLCLIENT_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)

        template_config = MAP_CONFIG_TEMPLATES.get(map_source_key)
        if not template_config:
            print(f"[Error] No template found for key: {map_source_key}")
            return False

        if "lbs" not in data:
            data["lbs"] = {}
        data["lbs"].update(template_config["config"])

        with open(PATH_SLCLIENT_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return True

    except Exception as e:
        print(f"[Error] Failed to update slclient.json: {e}")
        return False


def get_json_field(file_path: Path, field_path: List[str]) -> Any:
    try:
        if not file_path.exists():
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        temp_data = data
        for key in field_path:
            if isinstance(temp_data, dict):
                temp_data = temp_data.get(key)
            else:
                return None
        return temp_data
    except Exception:
        return None


def set_json_field(file_path: Path, field_path: List[str], new_value: Any) -> bool:
    try:
        if not file_path.exists():
            return False

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        temp_data = data
        for key in field_path[:-1]:
            if isinstance(temp_data, dict) and key in temp_data:
                temp_data = temp_data[key]
            else:
                return False

        target_key = field_path[-1]
        if isinstance(temp_data, dict):
            temp_data[target_key] = new_value
        else:
            return False

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return True

    except Exception as e:
        return False


def load_slclient_json() -> dict:
    json_path = PATH_SLCLIENT_JSON
    data = {}

    if not json_path.exists():
        return data

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                data = json.loads(content)
    except Exception:
        pass

    return data


# ==================== Manifest 辅助函数 ====================


def android_attr(name):
    return f"{{{ANDROID_NAMESPACE}}}{name}"


def write_pretty_xml(tree, file_path):
    rough_string = ET.tostring(tree.getroot(), encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="    ")

    pretty_xml = "\n".join([line for line in pretty_xml.split("\n") if line.strip()])

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)


def modify_manifest(is_enabled: bool, log_callback=None):
    manifest_path = PATH_MANIFEST_XML

    if not os.path.exists(manifest_path):
        if log_callback:
            log_callback(" Error: Unable to find AndroidManifest.xml")
        return

    try:
        ET.register_namespace("android", ANDROID_NAMESPACE)
        tree = ET.parse(manifest_path)
        root = tree.getroot()

        application = root.find("application")
        if application is None:
            if log_callback:
                log_callback(" Error: Unable to find the <application>tag")
            return

        candidate_activity_names = [
            "com.shanli.pocstar.SplashActivity",
            "com.shanlitech.ptt.SplashActivity",
            "com.shanlitech.noscreen.SplashActivity",
        ]

        target_activity = None
        found_activity_name = ""

        for activity in application.findall("activity"):
            name = activity.attrib.get(android_attr("name"), "")
            if name in candidate_activity_names:
                target_activity = activity
                found_activity_name = name
                break

        if target_activity is None:
            if log_callback:
                log_callback(
                    f" Error: Target Activity not found (candidate:{candidate_activity_names})"
                )
            return

        intent_filter = target_activity.find("intent-filter")
        if intent_filter is None:
            if log_callback:
                log_callback(
                    f" Error：{found_activity_name} No<intent-filter>, cannot operate"
                )
            return

        home_category_elem = None
        for category in intent_filter.findall("category"):
            if (
                category.attrib.get(android_attr("name"))
                == "android.intent.category.HOME"
            ):
                home_category_elem = category
                break

        has_home = home_category_elem is not None

        if is_enabled:
            if not has_home:
                ET.SubElement(
                    intent_filter,
                    "category",
                    {android_attr("name"): "android.intent.category.HOME"},
                )
                write_pretty_xml(tree, manifest_path)
                if log_callback:
                    log_callback(f"[ok]  set to desktop as Launcher\n")
        else:
            if has_home:
                intent_filter.remove(home_category_elem)
                write_pretty_xml(tree, manifest_path)
                if log_callback:
                    log_callback(f"[ok] Launcher has  cancelled\n")

    except Exception as e:
        if log_callback:
            log_callback(f" operation failed：{e}")


# ==================== YAML 辅助函数 ====================


def load_yml(yml_path: Path) -> Optional[Dict]:
    yaml = YAML()
    if not os.path.exists(yml_path):
        return None
    try:
        with open(yml_path, "r", encoding="utf-8") as f:
            return yaml.load(f)
    except Exception:
        return None


def update_version_info(yml_path: Path, log_callback=None) -> None:
    yaml = YAML()

    def represent_none(self, data):
        return self.represent_scalar("tag:yaml.org,2002:null", "null")

    yaml.representer.add_representer(type(None), represent_none)

    data = load_yml(yml_path)
    if not data:
        return

    version_info = data.get("versionInfo", {})
    old_code = version_info.get("versionCode")
    old_name = version_info.get("versionName")

    if not old_code or not old_name:
        if log_callback:
            log_callback(
                "[Warn]Unable to obtain version information, skipping update\n"
            )
        return

    new_code = int(old_code) + 1

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    pattern = r"(POCSTARS_)\d+$"
    new_name = re.sub(pattern, rf"\1{timestamp}", old_name)
    if new_name == old_name:
        new_name = f"{old_name}_{timestamp}"

    version_info["versionCode"] = new_code
    version_info["versionName"] = new_name

    with open(yml_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f)

    if log_callback:
        log_callback(
            f"[Version]update successful：{old_name}->{new_name}, Code: {old_code}->{new_code}\n"
        )
