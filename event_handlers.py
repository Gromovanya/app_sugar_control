import time
import threading
from char_manager import update_chart_data, get_current_time
from db_manager import fetch_statistics, insert_db_data, create_table, connect_db
from flet import LineChartDataPoint, SnackBar, Text, TextField, OutlinedButton, LineChart, Page
from functools import partial
from os import remove, path

MIN_SUGAR = 0
MAX_SUGAR = 25


def reset_text_bt(btn: OutlinedButton, page: Page):
    time.sleep(2)
    btn.text = 'Ввести'
    page.update()


def delete_chart(chart: LineChart, name_table: str, page: Page,
                avg_stat: Text, max_stat: Text, min_stat: Text, count_stat: Text):
    chart.data_series[0].data_points = []
    remove(name_table)
    
    avg_stat.value = 'Пока нет данных'
    max_stat.value = 'Пока нет данных'
    min_stat.value = 'Пока нет данных'
    count_stat.value = 'Пока нет данных'
    
    page.update()
    
def renewal_statistics(stats: dict, avg_stat: Text, max_stat: Text, min_stat: Text, count_stat: Text):
    avg_stat.value = round(stats['avg'], 1) if not stats['avg'] is None else 'Пока нет данных'
    max_stat.value = stats['max'] if not stats['max'] is None else 'Пока нет данных'
    min_stat.value = stats['min'] if not stats['min'] is None else 'Пока нет данных'
    count_stat.value = stats['count'] if not stats['count'] is None else 'Пока нет данных'

def on_change_sugar(input_sugar: TextField, btn_upd: OutlinedButton):
    if input_sugar.value:
        btn_upd.disabled = False
    else:
        btn_upd.disabled = True
    btn_upd.update()


def timer(input_sugar: TextField, timer_glav: Text, page: Page):
    temp_on_change = input_sugar.on_change
    input_sugar.on_change = None
    minute = 0
    secund = 4
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


def register_sugar(input_sugar: TextField, btn_upd: OutlinedButton, timer_glav: Text,
                    chart: LineChart, page: Page,
                    avg_stat: Text, max_stat: Text, min_stat: Text, count_stat: Text):
    try:
        num_sugar = round(float(input_sugar.value), 1)

        if MIN_SUGAR < num_sugar <= MAX_SUGAR:
            current_time = get_current_time()

            db = connect_db("db_registr.sugar")
            create_table(db)
            insert_db_data(
                db, num_sugar, current_time[0], current_time[1], current_time[2], current_time[3])

            stats = fetch_statistics(db)
            rows = stats['rows'][-1]
            data_point = [LineChartDataPoint(rows[2], rows[1])]
            update_chart_data(chart, data_point)
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
        page.snack_bar = SnackBar(
            Text('Нужно вводить только числа!'))
        page.snack_bar.open = True
        page.update()
