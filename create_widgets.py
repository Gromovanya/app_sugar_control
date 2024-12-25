import flet as ft
from event_handlers import delete_chart

def create_panel_statistics(avg_stat: ft.Text, max_stat: ft.Text, min_stat: ft.Text, count_stat: ft.Text):
    return ft.Column(
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

def create_input_sugar(timer_glav: ft.Text, input_sugar: ft.TextField, btn_upd: ft.OutlinedButton):
    return ft.Column(
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

def create_panel_menu(page: ft.Page, chart: ft.LineChart, panel_statistics: ft.Column, panel_input_sugar: ft.Column,
                    avg_stat: ft.Text, max_stat: ft.Text, min_stat: ft.Text, count_stat: ft.Text):
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
                    icon=ft.icons.AREA_CHART, text='Graph',
                    on_click=lambda _: (
                        page.clean(), page.add(panel_menu, chart))
                ),
                ft.PopupMenuItem(
                    icon=ft.icons.ADD_CHART, text='Input sugar',
                    on_click=lambda _: (page.controls.remove(panel_statistics), page.add(
                        panel_input_sugar)) if panel_statistics in page.controls else page.add(panel_input_sugar)
                ),
                ft.PopupMenuItem(
                    icon=ft.icons.SSID_CHART, text='Statistics',
                    on_click=lambda _: (page.controls.remove(panel_input_sugar), page.add(
                        panel_statistics)) if panel_input_sugar in page.controls else page.add(panel_statistics)
                ),
                ft.PopupMenuItem(
                    icon=ft.icons.DELETE, text='Full cleaning the data of charts',
                    on_click=lambda e: delete_chart(chart, "db_registr.sugar", page, avg_stat, max_stat, min_stat, count_stat)
                ),
            ],
        ),
        alignment=ft.alignment.top_left
    )
    return panel_menu