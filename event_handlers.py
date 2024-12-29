import time
import threading
import flet as ft
from constants import (
    MIN_SUGAR,
    MAX_SUGAR,
    SETTING_PATH_FILE,
    KEY_THEME,
    KEY_COLOR_DOP_THEME,
    KEY_TIMER_MINUTE,
    KEY_TIMER_SEC,
    NOT_DATA
)
from char_manager import (
    update_chart_data,
    get_current_time
)
from db_manager import (
    verification_table,
    fetch_statistics,
    insert_db_data,
    create_table,
    connect_db,
    del_table
)
from json_manager import (
    reed_data_file,
    update_json_file,
    get_json_file
)


def set_color_page(page: ft.Page, color: str):
    color_code = getattr(ft.colors, color, "#000001") if color is not None else None
    update_json_file(KEY_COLOR_DOP_THEME, color)
    page.bgcolor = color_code
    page.update()


def dark_theme(page: ft.Page, line_chart: ft.LineChart, theme: ft.Row):
    theme.controls[0].controls[0].icon = ft.icons.LIGHT_MODE
    theme.controls[0].controls[1].value = "Light"
    page.theme_mode = 'dark'
    line_chart.data_series[0].color = ft.Colors.WHITE
    line_chart.bgcolor = '#00001B'
    line_chart.horizontal_grid_lines = ft.ChartGridLines(
        interval=1, color=ft.Colors.with_opacity(opacity=1, color=ft.Colors.ON_SURFACE), width=0.1
    )
    line_chart.vertical_grid_lines = ft.ChartGridLines(
        interval=60, color=ft.Colors.with_opacity(opacity=1, color=ft.Colors.ON_SURFACE), width=0.1
    )

def light_theme(page: ft.Page, line_chart: ft.LineChart, theme: ft.Row):
    theme.controls[0].controls[0].icon = ft.icons.DARK_MODE
    theme.controls[0].controls[1].value = "Dark"
    page.theme_mode = 'light'
    line_chart.data_series[0].color = ft.Colors.GREY_600
    line_chart.bgcolor = '#00005B'
    line_chart.horizontal_grid_lines = ft.ChartGridLines(
        interval=1, color=ft.Colors.with_opacity(opacity=1, color=ft.Colors.WHITE), width=0.1
    )
    line_chart.vertical_grid_lines = ft.ChartGridLines(
        interval=60, color=ft.Colors.with_opacity(opacity=1, color=ft.Colors.WHITE), width=0.1
    )
    
    
def theme_dark_and_light(page: ft.Page, line_chart: ft.LineChart, theme: ft.Row):
    if page.theme_mode == 'dark':
        light_theme(page, line_chart, theme)
        update_json_file(KEY_THEME, 'light')
    else:
        dark_theme(page, line_chart, theme)
        update_json_file(KEY_THEME, 'dark')
    page.update()


def reset_text_bt(btn: ft.OutlinedButton, page: ft.Page):
    time.sleep(2)
    btn.text = 'Ввести'
    page.update()


def delete_chart(chart: ft.LineChart, page: ft.Page,
                    avg_stat: ft.Text, max_stat: ft.Text, min_stat: ft.Text, count_stat: ft.Text):
    chart.data_series[0].data_points = []
    db = connect_db()
    del_table(db, "indic_sugar")
    db.close()

    avg_stat.value = NOT_DATA
    max_stat.value = NOT_DATA
    min_stat.value = NOT_DATA
    count_stat.value = '0'

    page.update()


def renewal_statistics(stats: dict, avg_stat: ft.Text, max_stat: ft.Text, min_stat: ft.Text, count_stat: ft.Text):
    avg_stat.value = round(
        stats['avg'], 1) if not stats['avg'] is None else NOT_DATA
    max_stat.value = stats['max'] if not stats['max'] is None else NOT_DATA
    min_stat.value = stats['min'] if not stats['min'] is None else NOT_DATA
    count_stat.value = stats['count'] if not stats['count'] is None else NOT_DATA


def on_change_sugar(input_sugar: ft.TextField, btn_upd: ft.OutlinedButton):
    if input_sugar.value:
        btn_upd.disabled = False
    else:
        btn_upd.disabled = True
    btn_upd.update()


def timer(input_sugar: ft.TextField, timer_glav: ft.Text, page: ft.Page, on_click: bool=False):
    get_json_file()
    setting = reed_data_file(SETTING_PATH_FILE)
    temp_on_change = input_sugar.on_change
    input_sugar.on_change = None
    minute = setting[KEY_TIMER_MINUTE] if on_click else 5
    second = setting[KEY_TIMER_SEC] if on_click else 0
    timer_glav.value = f"{minute:02}:{second:02}"
    page.update()

    while minute >= 0:
        while second >= 0:
            if verification_table("indic_sugar"):
                minute = 0
                second = 0
            timer_glav.value = f"{minute:02}:{second:02}"
            page.update()
            time.sleep(1)
            update_json_file(KEY_TIMER_SEC, second)
            second -= 1
        minute -= 1
        second = 59
        update_json_file(KEY_TIMER_MINUTE, minute)

    update_json_file(KEY_TIMER_MINUTE, 0)
    update_json_file(KEY_TIMER_SEC, 0)
    input_sugar.on_change = temp_on_change
    page.update()


def register_sugar(input_sugar: ft.TextField, btn_upd: ft.OutlinedButton, timer_glav: ft.Text,
                    chart: ft.LineChart, page: ft.Page,
                    avg_stat: ft.Text, max_stat: ft.Text, min_stat: ft.Text, count_stat: ft.Text):
    try:
        num_sugar = round(float(input_sugar.value), 1)

        if num_sugar >= MAX_SUGAR:
            num_sugar = MAX_SUGAR
        elif num_sugar <= MIN_SUGAR:
            num_sugar = MIN_SUGAR

        current_time = get_current_time()

        db = connect_db()
        create_table(db)
        insert_db_data(
            db, num_sugar, current_time[0], current_time[1], current_time[2], current_time[3])

        stats = fetch_statistics(db)
        rows = stats['rows'][-1]
        update_chart_data(chart, ft.LineChartDataPoint(rows[2], rows[1]))
        renewal_statistics(stats, avg_stat, max_stat, min_stat, count_stat)

        db.close()

        input_sugar.value = ''
        btn_upd.text = 'Введено'
        btn_upd.disabled = True

        threading.Thread(target=reset_text_bt, args=(
            btn_upd, page,), daemon=True).start()

        threading.Thread(target=timer, args=(
            input_sugar, timer_glav, page,), daemon=True).start()

        page.update()

    except ValueError:
        page.snack_bar = ft.SnackBar(
            ft.Text('Нужно вводить только числа!'))
        page.snack_bar.open = True
        page.update()


def modify_setting(page: ft.Page, line_chart: ft.LineChart, theme: ft.Row):
    get_json_file()
    setting = reed_data_file(SETTING_PATH_FILE)
    color_dop_theme = setting[KEY_COLOR_DOP_THEME]
    
    if setting[KEY_THEME] == 'dark':
        dark_theme(page, line_chart, theme)
    else:
        light_theme(page, line_chart, theme)
    page.bgcolor = getattr(ft.colors, color_dop_theme, None) if color_dop_theme is not None else None