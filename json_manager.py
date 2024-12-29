import json
from os import makedirs, path
from constants import DEFAULT_SETTINGS, SETTING_PATH_FILE, PATH_DIR_JSON, KEY_THEME

def get_json_file():
    makedirs(PATH_DIR_JSON, exist_ok=True)
    
    if not path.exists(SETTING_PATH_FILE):
        with open(SETTING_PATH_FILE, 'w', encoding='utf-8') as json_file:
            json.dump(DEFAULT_SETTINGS, json_file, indent=4)


def reed_data_file(file_path):
    if path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as json_file:
            setting = json.load(json_file)
        return setting


def update_json_file(needs_modify_key, data):
    setting = reed_data_file(SETTING_PATH_FILE)

    setting[needs_modify_key] = data
    if path.exists(SETTING_PATH_FILE):
        with open('data_app_sugar/setting_app.json', 'w', encoding='utf-8') as json_file:
            json.dump(setting, json_file, indent=4)
        