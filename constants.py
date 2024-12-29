import flet as ft

# Constants for constants.py, event_handlers.py
KEY_THEME = "theme"
KEY_COLOR_DOP_THEME = "color_dop_theme"
KEY_TIMER_MINUTE = "timer_minute"
KEY_TIMER_SEC = "timer_sec"

# Constants for event_handlers.py
MIN_SUGAR = 0
MAX_SUGAR = 25

# Constants for char_manager.py
HOURS_IN_A_DAY = 24
MINUTES_IN_AN_HOUR = 60
MAX_Y = 25
MIN_Y = 0

# Constants for db_manager.py
SUGAR_DB = "db-app-data.sugar"


# Constants for json_manager.py, event_handlers.py
SETTING_PATH_FILE = 'data_app_sugar/setting_app.json'
PATH_DIR_JSON = 'data_app_sugar'
DEFAULT_SETTINGS = {
    KEY_THEME: 'dark',
    KEY_COLOR_DOP_THEME: None,
    KEY_TIMER_MINUTE: 0,
    KEY_TIMER_SEC: 0,
}

# Constants for event_handlers.py
NOT_DATA = 'Not data'