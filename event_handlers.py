import time
import threading
from char_manager import update_chart_data, get_current_time
from db_manager import fetch_statistics, insert_db_data, create_table, connect_db
import flet as ft
from os import remove, path

MIN_SUGAR = 0
MAX_SUGAR = 25


def set_color_page(page: ft.Page, color: ft.Colors):
    page.bgcolor = color
    page.update()

def theme_dark_and_light(page: ft.Page, line_chart: ft.LineChart, theme: ft.Row):
    if page.theme_mode == 'dark':
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
    else:
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
    page.update()


def reset_text_bt(btn: ft.OutlinedButton, page: ft.Page):
    time.sleep(2)
    btn.text = 'Ввести'
    page.update()


def delete_chart(chart: ft.LineChart, name_table: str, page: ft.Page,
                avg_stat: ft.Text, max_stat: ft.Text, min_stat: ft.Text, count_stat: ft.Text):
    chart.data_series[0].data_points = []
    remove(name_table)
    
    avg_stat.value = 'Пока нет данных'
    max_stat.value = 'Пока нет данных'
    min_stat.value = 'Пока нет данных'
    count_stat.value = '0'
    
    page.update()
    
def renewal_statistics(stats: dict, avg_stat: ft.Text, max_stat: ft.Text, min_stat: ft.Text, count_stat: ft.Text):
    avg_stat.value = round(stats['avg'], 1) if not stats['avg'] is None else 'Пока нет данных'
    max_stat.value = stats['max'] if not stats['max'] is None else 'Пока нет данных'
    min_stat.value = stats['min'] if not stats['min'] is None else 'Пока нет данных'
    count_stat.value = stats['count'] if not stats['count'] is None else 'Пока нет данных'

def on_change_sugar(input_sugar: ft.TextField, btn_upd: ft.OutlinedButton):
    if input_sugar.value:
        btn_upd.disabled = False
    else:
        btn_upd.disabled = True
    btn_upd.update()


def timer(input_sugar: ft.TextField, timer_glav: ft.Text, page: ft.Page):
    temp_on_change = input_sugar.on_change
    input_sugar.on_change = None
    minute = 5
    secund = 0
    timer_glav.value = f"{minute:02}:{secund:02}"
    timer_glav.update()

    while minute >= 0:
        while secund >= 0:
            if not path.exists('db_registr.sugar'):
                minute = 0
                secund = 0
            timer_glav.value = f"{minute:02}:{secund:02}"
            page.update()
            time.sleep(1)
            secund -= 1
        minute -= 1
        secund = 59

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

        db = connect_db("db_registr.sugar")
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
