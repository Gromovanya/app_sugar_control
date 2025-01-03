import json
from os import makedirs, path
from constants import DEFAULT_SETTINGS, SETTING_PATH_FILE, PATH_DIR_JSON, TIMER_PATH_FILE, DEFAULT_TIMER


def get_json_file(path_file: str, default: dict):
    makedirs(PATH_DIR_JSON, exist_ok=True)

    if not path.exists(path_file):
        with open(path_file, 'w', encoding='utf-8') as json_file:
            json.dump(default, json_file, indent=4)


def read_data_file(file_path: str) -> dict:
    get_json_file(SETTING_PATH_FILE, DEFAULT_SETTINGS)
    get_json_file(TIMER_PATH_FILE, DEFAULT_TIMER)

    with open(file_path, 'r', encoding='utf-8') as json_file:
        setting = json.load(json_file)
    return setting


def update_json_file(needs_modify_key: str, value: any, path_file: str):
    get_json_file(SETTING_PATH_FILE, DEFAULT_SETTINGS)
    get_json_file(TIMER_PATH_FILE, DEFAULT_TIMER)

    data = read_data_file(path_file)

    data[needs_modify_key] = value
    with open(path_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)
