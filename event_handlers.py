import time
import threading
import flet as ft
from constants import (
    MIN_SUGAR, MAX_SUGAR, SETTING_PATH_FILE, KEY_THEME, KEY_COLOR_DOP_THEME,
    KEY_TIMER_MINUTE, KEY_TIMER_SEC, NOT_DATA, KEY_STATISTICS, KEY_INPUT_SUGAR,
    DEFAULT_QUANT_OBJECT_ON_PAGE, MINUTES, SECONDS, TIMER_PATH_FILE
)
from char_manager import update_chart_data
from db_manager import verification_table, fetch_statistics, insert_db_data, create_table, connect_db, del_table
from json_manager import read_data_file, update_json_file
from get_data import get_current_time

def modify_page_and_settings(page: ft.Page, panel_true: ft.Column | ft.Container, key_true: bool, keys_false: tuple):
    if panel_true not in page.controls:
        if len(page.controls) > DEFAULT_QUANT_OBJECT_ON_PAGE:
            del page.controls[DEFAULT_QUANT_OBJECT_ON_PAGE:]
            update_json_file(key_true, True, SETTING_PATH_FILE)
            
            for key_false in keys_false:
                update_json_file(key_false, False, SETTING_PATH_FILE)
            page.add(panel_true)
        else:
            page.add(panel_true)
            update_json_file(key_true, True, SETTING_PATH_FILE)

def set_color_page(page: ft.Page, color: str):
    color_code = getattr(ft.colors, color, "#000001") if color is not None else None
    update_json_file(KEY_COLOR_DOP_THEME, color, SETTING_PATH_FILE)
    page.bgcolor = color_code
    page.update()

def update_theme(page: ft.Page, line_chart: ft.LineChart, theme: ft.Row, mode: str, icon: str, text: str):
    theme.controls[0].controls[0].icon = icon
    theme.controls[0].controls[1].value = text
    page.theme_mode = mode
    line_chart.data_series[0].color = ft.Colors.WHITE if mode == 'dark' else ft.Colors.GREY_600
    line_chart.bgcolor = '#00001B' if mode == 'dark' else '#00005B'
    color = ft.Colors.ON_SURFACE if mode == 'dark' else ft.Colors.WHITE
    line_chart.horizontal_grid_lines = ft.ChartGridLines(interval=1, color=ft.Colors.with_opacity(1, color), width=0.1)
    line_chart.vertical_grid_lines = ft.ChartGridLines(interval=60, color=ft.Colors.with_opacity(1, color), width=0.1)
    page.update()

def theme_dark_and_light(page: ft.Page, line_chart: ft.LineChart, theme: ft.Row):
    if page.theme_mode == 'dark':
        update_theme(page, line_chart, theme, 'light', ft.icons.DARK_MODE, "Dark")
        update_json_file(KEY_THEME, 'light', SETTING_PATH_FILE)
    else:
        update_theme(page, line_chart, theme, 'dark', ft.icons.LIGHT_MODE, "Light")
        update_json_file(KEY_THEME, 'dark', SETTING_PATH_FILE)
    page.update()

def delete_chart(chart: ft.LineChart, page: ft.Page, statistics: ft.Column):
    chart.data_series[0].data_points = []
    db = connect_db()
    del_table(db, "indic_sugar")
    db.close()
    
    renewal_text_stats(statistics)
    page.update()

def renewal_text_stats(statistics: ft.Column):
    db = connect_db()
    stats = fetch_statistics(db)
    db.close()
    
    statistics.controls[1].controls[1].value = round(stats['avg'], 1) if stats['avg'] is not None else NOT_DATA
    statistics.controls[2].controls[1].value = stats['max'] if stats['max'] is not None else NOT_DATA
    statistics.controls[3].controls[1].value = stats['min'] if stats['min'] is not None else NOT_DATA
    statistics.controls[4].controls[1].value = stats['count'] if stats['count'] != 0 else "0"

def on_change_sugar(input_sugar: ft.TextField, btn_upd: ft.OutlinedButton):
    btn_upd.disabled = not bool(input_sugar.value)
    btn_upd.update()

def timer(input_sugar: ft.TextField, timer_glav: ft.Text, page: ft.Page, btn: ft.OutlinedButton):
    now_time = read_data_file(TIMER_PATH_FILE)
    temp_on_change = input_sugar.on_change
    input_sugar.on_change = None
    
    minute = now_time[KEY_TIMER_MINUTE]
    second = now_time[KEY_TIMER_SEC]
    timer_glav.value = f"{minute:02}:{second:02}"
    btn.text = 'Введено'
    page.update()

    while minute >= 0:
        while second >= 0:
            if verification_table():
                minute = second = 0
            timer_glav.value = f"{minute:02}:{second:02}"
            page.update()
            time.sleep(1)
            second -= 1
            update_json_file(KEY_TIMER_SEC, second, TIMER_PATH_FILE)
        minute -= 1
        second = 59
        update_json_file(KEY_TIMER_MINUTE, minute, TIMER_PATH_FILE)
        update_json_file(KEY_TIMER_SEC, second, TIMER_PATH_FILE)
        
    input_sugar.on_change = temp_on_change
    update_json_file(KEY_TIMER_MINUTE, MINUTES, TIMER_PATH_FILE)
    update_json_file(KEY_TIMER_SEC, SECONDS, TIMER_PATH_FILE)
    btn.text = 'Ввести'
    page.update()

def register_sugar(input_sugar: ft.TextField, btn_upd: ft.OutlinedButton, timer_glav: ft.Text,
                    chart: ft.LineChart, page: ft.Page, statistics: ft.Column):
    try:
        num_sugar = round(float(input_sugar.value), 1)
        num_sugar = max(min(num_sugar, MAX_SUGAR), MIN_SUGAR)
        current_time = get_current_time()

        db = connect_db()
        create_table(db)
        insert_db_data(db, num_sugar, current_time[0], current_time[1], current_time[2], current_time[3])

        rows = fetch_statistics(db)['rows'][-1]
        update_chart_data(chart, ft.LineChartDataPoint(rows[2], rows[1]))
        renewal_text_stats(statistics)
        db.close()

        input_sugar.value = ''
        btn_upd.text = 'Введено'
        btn_upd.disabled = True

        threading.Thread(target=timer, args=(input_sugar, timer_glav, page, btn_upd), daemon=True).start()
        page.update()

    except ValueError:
        page.snack_bar = ft.SnackBar(ft.Text('Нужно вводить только числа!'))
        page.snack_bar.open = True
        page.update()

def modify_setting(page: ft.Page, line_chart: ft.LineChart, theme: ft.Row,
                    panel_input_sugar: ft.Column, panel_statistics: ft.Column):
    setting = read_data_file(SETTING_PATH_FILE)
    now_timer = read_data_file(TIMER_PATH_FILE)
    color_dop_theme = setting[KEY_COLOR_DOP_THEME]
    
    page.bgcolor = getattr(ft.colors, color_dop_theme, None) if color_dop_theme else None
    if setting[KEY_THEME] == 'dark':
        update_theme(page, line_chart, theme, 'dark', ft.icons.LIGHT_MODE, "Light")
    else:
        update_theme(page, line_chart, theme, 'light', ft.icons.DARK_MODE, "Dark")

    if setting[KEY_STATISTICS]:
        page.add(panel_statistics)
    elif setting[KEY_INPUT_SUGAR]:
        page.add(panel_input_sugar)

    if now_timer[KEY_TIMER_MINUTE] != 5 or now_timer[KEY_TIMER_SEC] != 0:
        timer(
            panel_input_sugar.controls[2].controls[0].controls[1], 
            panel_input_sugar.controls[1].controls[0], 
            page, 
            panel_input_sugar.controls[2].controls[0].controls[2]
        )
