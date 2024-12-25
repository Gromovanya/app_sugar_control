import flet as ft
import sqlite3
import time
from datetime import datetime
import threading
from os import remove, path


def main(page: ft.Page):
    page.title = "Sugar data Analyst"
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.adaptive = True
    now = datetime.now()

    # Устанавливаем размеры окна
    page.window_width = 1200
    page.window_height = 1000

    def reset_text_bt():
        time.sleep(2)
        btn_upd.text = 'Ввести'
        page.update()

    def register_statistics():
        db = sqlite3.connect('db_registr.sugar')
        cur = db.cursor()

        cur.execute('SELECT AVG(indicators_sugar) FROM indic_sugar')
        res = cur.fetchone()
        avg_stat.value = round(
            res[0], 1) if res[0] is not None else 'Пока нет данных'

        cur.execute('SELECT MAX(indicators_sugar) FROM indic_sugar')
        res = cur.fetchone()
        max_stat.value = res[0] if res[0] is not None else 'Пока нет данных'

        cur.execute('SELECT MIN(indicators_sugar) FROM indic_sugar')
        res = cur.fetchone()
        min_stat.value = res[0] if res[0] is not None else 'Пока нет данных'
        
        cur.execute('SELECT COUNT(*) FROM indic_sugar')
        res = cur.fetchone()
        count_stat.value = res[0] if res[0] is not None else 'Пока нет данных'

        db.close()

    def timer():
        input_sugar.on_change = None
        minute = 4
        secund = 0
        timer_glav.value = f"{minute:02}:{secund:02}"
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

        input_sugar.on_change = on_change_sugar
        page.update()

    def register_sugar(e):
        try:

            num_sugar = round(float(input_sugar.value), 1)

            if 0 < num_sugar < 25:
                db = sqlite3.connect('db_registr.sugar')
                cur = db.cursor()

                cur.execute("""CREATE TABLE IF NOT EXISTS indic_sugar (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    indicators_sugar DECIMAL(5, 1),
                    time_in_day TIME,
                    current_day INTEGER,
                    current_month INTEGER,
                    current_year INTEGER
                )""")

                current_time = now.hour * 60 + now.minute
                current_day = now.day
                current_month = now.month
                current_year = now.year

                cur.execute(f"""INSERT INTO indic_sugar
                            (indicators_sugar, time_in_day,
                            current_day, current_month, current_year)
                            VALUES (?, ?, ?, ?, ?)""",
                            (num_sugar, current_time, current_day, current_month, current_year))

                chart_date[0].data_points.append(
                    ft.LineChartDataPoint(current_time, num_sugar))

                db.commit()
                db.close()

                input_sugar.value = ''
                btn_upd.text = 'Введено'
                btn_upd.disabled = True

                threading.Thread(target=reset_text_bt, daemon=True).start()
                threading.Thread(target=timer, daemon=True).start()

                register_statistics()
                page.update()

            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text('Значение должно быть в диапозоне от 0 до 25'))
                page.snack_bar.open = True
                page.update()

        except ValueError:
            page.snack_bar = ft.SnackBar(
                ft.Text('Нужно вводить только числа!'))
            page.snack_bar.open = True
            page.update()

    def on_change_sugar(e):
        if input_sugar.value:
            btn_upd.disabled = False
        else:
            btn_upd.disabled = True
        page.update()

    def delete_chart(e):
        chart_date[0].data_points = []
        remove("db_registr.sugar")

    def navigate(e):
        in_index = page.navigation_bar.selected_index
        page.clean()

        if in_index == 0:
            page.add(panel_menu, chart)
        elif in_index == 1:
            page.add(panel_input_sugar)
        elif in_index == 2:
            page.add(panel_statistics)

    input_sugar = ft.TextField(
        label='Введите сахар (ммоль/л)', width=230, on_change=on_change_sugar)
    btn_upd = ft.OutlinedButton(
        text='Ввести', width=230, on_click=register_sugar, disabled=True)
    timer_glav = ft.Text("00:00", size=27)
    avg_stat = ft.Text('Пока нет данных', size=20)
    max_stat = ft.Text('Пока нет данных', size=20)
    min_stat = ft.Text('Пока нет данных', size=20)
    count_stat = ft.Text('Пока нет данных', size=20)

    panel_input_sugar = ft.Column(
        [
            ft.Row([ft.Icon(ft.icons.TIMER, size=25)],
                alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([timer_glav], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text('Ввод показаний сахара', size=15,
                                    weight=ft.FontWeight.BOLD),
                            input_sugar,
                            btn_upd
                        ]
                    )
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        alignment=ft.alignment.center_left
    )

    chart_date = [
        ft.LineChartData(
            data_points=[],
            stroke_width=5,
            color=ft.Colors.ORANGE,
            curved=True,
            stroke_cap_round=True,
        )
    ]

    chart = ft.LineChart(
        data_series=chart_date,
        border=ft.border.all(width=3, color=ft.Colors.with_opacity(
            opacity=0.2, color=ft.Colors.ON_SURFACE)),
        horizontal_grid_lines=ft.ChartGridLines(
            interval=1, color=ft.Colors.with_opacity(opacity=1, color=ft.Colors.ON_SURFACE), width=0.1
        ),
        vertical_grid_lines=ft.ChartGridLines(
            interval=60, color=ft.Colors.with_opacity(opacity=1, color=ft.Colors.ON_SURFACE), width=0.1
        ),
        left_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=0,
                    label=ft.Text('LOW', size=14, weight=ft.FontWeight.BOLD)
                ),
                ft.ChartAxisLabel(
                    value=2,
                    label=ft.Text('2', size=14, weight=ft.FontWeight.BOLD)
                ),
                ft.ChartAxisLabel(
                    value=6,
                    label=ft.Text('6', size=14, weight=ft.FontWeight.BOLD)
                ),
                ft.ChartAxisLabel(
                    value=10,
                    label=ft.Text('10', size=14, weight=ft.FontWeight.BOLD)
                ),
                ft.ChartAxisLabel(
                    value=14,
                    label=ft.Text('14', size=14, weight=ft.FontWeight.BOLD)
                ),
                ft.ChartAxisLabel(
                    value=18,
                    label=ft.Text('18', size=14, weight=ft.FontWeight.BOLD)
                ),
                ft.ChartAxisLabel(
                    value=22,
                    label=ft.Text('22', size=14, weight=ft.FontWeight.BOLD)
                ),
                ft.ChartAxisLabel(
                    value=24,
                    label=ft.Text('HIGHT', size=14, weight=ft.FontWeight.BOLD)
                )
            ],
            labels_size=55,
        ),
        bottom_axis=ft.ChartAxis(
            labels=[],
            labels_size=40,
        ),
        tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY),
        min_y=0,
        max_y=25,
        min_x=0,
        max_x=24 * 60,
        expand=True,
    )

    for hour in range(25):
        minutes_in_hour = hour * 60
        new_label = ft.ChartAxisLabel(
            value=minutes_in_hour,
            label=ft.Container(
                ft.Text(
                    f"{hour}",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
                margin=ft.margin.only(top=10),
            )
        )
        chart.bottom_axis.labels.append(new_label)

    # page.navigation_bar = ft.NavigationBar(
    #     adaptive=True,
    #     destinations=[
    #         ft.NavigationBarDestination(
    #             icon=ft.icons.PIE_CHART, label='Graph'),
    #         ft.NavigationBarDestination(
    #             icon=ft.icons.ADD_CHART, label='Input sugar'),
    #         ft.NavigationBarDestination(
    #             icon=ft.icons.BAR_CHART, label='Statistics'),
    #     ],
    #     on_change=navigate
    # )
    db = sqlite3.connect('db_registr.sugar')
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS indic_sugar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                indicators_sugar DECIMAL(5, 1),
                time_in_day TIME,
                current_day INTEGER,
                current_month INTEGER,
                current_year INTEGER
                )""")

    cur.execute("SELECT * FROM indic_sugar")
    rows = cur.fetchall()
    db.close()

    panel_statistics = ft.Column(
        [
            ft.Row([ft.Text("Статистика за день", size=24, weight=ft.FontWeight.BOLD)],
                alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.Text("Среднее значение сахара: ", size=20), avg_stat],
                alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.Text("Максимальное значение сахара: ", size=20), max_stat],
                alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.Text("Минимальное значение сахара: ", size=20), min_stat],
                alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.Text("Количество замерок сахара: ", size=20), count_stat],
                alignment=ft.MainAxisAlignment.CENTER),
        ]
    )

    panel_menu = ft.Container(
        content=ft.PopupMenuButton(
            icon=ft.icons.MENU,
            items=[
                ft.PopupMenuItem(
                    icon=ft.icons.MENU,
                    text='Menu'
                ),
                ft.PopupMenuItem(),
                ft.PopupMenuItem(
                    icon=ft.icons.PIE_CHART, text='Graph',
                    on_click=lambda _: (
                        page.clean(), page.add(panel_menu, chart))
                ),
                ft.PopupMenuItem(
                    icon=ft.icons.ADD_CHART, text='Input sugar',
                    on_click=lambda _: (page.controls.remove(panel_statistics), page.add(
                        panel_input_sugar)) if panel_statistics in page.controls else page.add(panel_input_sugar)
                ),
                ft.PopupMenuItem(
                    icon=ft.icons.BAR_CHART, text='Statistics',
                    on_click=lambda _: (page.controls.remove(panel_input_sugar), page.add(
                        panel_statistics)) if panel_input_sugar in page.controls else page.add(panel_statistics)
                ),
                ft.PopupMenuItem(
                    icon=ft.icons.DELETE, text='Full cleaning the data of charts',
                    on_click=delete_chart
                ),
            ],
        ),
        alignment=ft.alignment.top_left
    )

    delete_db = False

    for row in rows:
        if row[3] != now.day or row[4] != now.month or row[5] != now.year:
            delete_db = True
            break

    if delete_db:
        delete_chart(None)
        print('Таблица очищена')
    else:
        for row in rows:
            chart_date[0].data_points.append(
                ft.LineChartDataPoint(row[2], row[1]))
        register_statistics()
        print("Данные добавлены в график.")
    page.add(panel_menu, chart)


ft.app(target=main)
