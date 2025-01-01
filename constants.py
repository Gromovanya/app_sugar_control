# Constants for general use
KEY_THEME: str = "theme"
KEY_COLOR_DOP_THEME: str = "color_dop_theme"
KEY_TIMER_MINUTE: str = "timer_minute"
KEY_TIMER_SEC: str = "timer_sec"
KEY_STATISTICS: str = "statistics"
KEY_INPUT_SUGAR: str = "input_sugar"

# Constants for event_handlers.py
MIN_SUGAR: int = 0
MAX_SUGAR: int = 25
DEFAULT_QUANT_OBJECT_ON_PAGE: int = 3
MINUTES: int = 5
SECONDS: int = 0

# Constants for char_manager.py
HOURS_IN_A_DAY: int = 24
MINUTES_IN_AN_HOUR: int = 60
MAX_Y: int = 25
MIN_Y: int = 0

# Constants for db_manager.py
SUGAR_DB: str = "data_app_sugar/db-app-data.sugar"

# Constants for json_manager.py and event_handlers.py
SETTING_PATH_FILE: str = 'data_app_sugar/setting_app.json'
TIMER_PATH_FILE: str = 'data_app_sugar/time.json'
PATH_DIR_JSON: str = 'data_app_sugar'

DEFAULT_SETTINGS: dict = {
    KEY_THEME: 'dark',
    KEY_COLOR_DOP_THEME: None,
    KEY_INPUT_SUGAR: False,
    KEY_STATISTICS: False
}

DEFAULT_TIMER: dict = {
    KEY_TIMER_MINUTE: MINUTES,
    KEY_TIMER_SEC: SECONDS
}

# Constants for event_handlers.py
NOT_DATA: str = 'Not data'