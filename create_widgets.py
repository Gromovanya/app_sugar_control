import flet as ft
from event_handlers import (
    delete_chart,
    theme_dark_and_light,
    set_color_page,
)
from json_manager import (
    update_json_file
)
from constants import (
    KEY_INPUT_SUGAR,
    KEY_STATISTICS
)


def create_panel_statistics(avg_stat: ft.Text, max_stat: ft.Text, min_stat: ft.Text, count_stat: ft.Text):
    return ft.Column(
        [
            ft.Row([ft.Text("Статистика за день", size=24)],
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
                        avg_stat: ft.Text, max_stat: ft.Text, min_stat: ft.Text,
                        count_stat: ft.Text, panel_menu_theme: ft.Container):
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
                        page.clean(), page.add(panel_menu, chart, panel_menu_theme),
                        update_json_file(KEY_INPUT_SUGAR, False), update_json_file(KEY_STATISTICS, False))
                ),
                ft.PopupMenuItem(
                    icon=ft.icons.ADD_CHART, text='Input sugar',
                    on_click=lambda _: (page.controls.remove(panel_statistics), update_json_file(KEY_INPUT_SUGAR, True),
                        update_json_file(KEY_STATISTICS, False), page.add(panel_input_sugar)) if panel_statistics in page.controls 
                        else (page.add(panel_input_sugar), update_json_file(KEY_INPUT_SUGAR, True))
                ),
                ft.PopupMenuItem(
                    icon=ft.icons.SSID_CHART, text='Statistics',
                    on_click=lambda _: (page.controls.remove(panel_input_sugar), update_json_file(KEY_STATISTICS, True),
                        update_json_file(KEY_INPUT_SUGAR, False), page.add(panel_statistics)) if panel_input_sugar in page.controls 
                        else (page.add(panel_statistics),  update_json_file(KEY_STATISTICS, True))
                ),
                ft.PopupMenuItem(
                    icon=ft.icons.DELETE, text='Full cleaning the data of charts',
                    on_click=lambda _: delete_chart(
                        chart, page, avg_stat, max_stat, min_stat, count_stat)
                ),
            ],
        ),
        alignment=ft.alignment.top_left
    )
    return panel_menu


def create_panel_menu_theme(page: ft.Page, line_chart: ft.LineChart):
    panel_menu_theme = ft.Column(
        controls=[
            ft.Row(
                [
                    ft.IconButton(icon=ft.icons.LIGHT_MODE, on_click=lambda _: theme_dark_and_light(
                        page, line_chart, panel_menu_theme)),
                    ft.Text('Light', size=17, weight='bold')
                ]
            ),
            ft.Row(
                [
                    ft.Container(
                        content=ft.PopupMenuButton(
                            icon=ft.icons.PALETTE_OUTLINED,
                            icon_color=ft.Colors.ON_PRIMARY_CONTAINER,
                            icon_size=25,
                            items=[
                                ft.PopupMenuItem(
                                    content=ft.Row([ft.Icon(ft.Icons.PALETTE_OUTLINED, ft.Colors.DEEP_PURPLE_ACCENT, size=25),
                                                    ft.Text('Deep-purple', size=17)]),
                                    on_click=lambda _: set_color_page(
                                        page, "DEEP_PURPLE_ACCENT_100")
                                ),
                                ft.PopupMenuItem(
                                    content=ft.Row([ft.Icon(ft.Icons.PALETTE_OUTLINED, ft.Colors.PINK_ACCENT, size=25),
                                                    ft.Text('Pink', size=17)]),
                                    on_click=lambda _: set_color_page(
                                        page, "PINK_ACCENT_100")
                                ),
                                ft.PopupMenuItem(
                                    content=ft.Row([ft.Icon(ft.Icons.PALETTE_OUTLINED, ft.Colors.BLUE_ACCENT, size=25),
                                                    ft.Text('Blue', size=17)]),
                                    on_click=lambda _: set_color_page(
                                        page, "BLUE_ACCENT_100")
                                ),
                                ft.PopupMenuItem(
                                    content=ft.Row([ft.Icon(ft.Icons.PALETTE_OUTLINED, ft.Colors.DEEP_ORANGE_ACCENT, size=25),
                                                    ft.Text('Deep-orange', size=17)]),
                                    on_click=lambda _: set_color_page(
                                        page, "DEEP_ORANGE_ACCENT_100")
                                ),
                                ft.PopupMenuItem(
                                    content=ft.Row([ft.Icon(ft.Icons.PALETTE_OUTLINED, ft.Colors.GREEN_ACCENT, size=25),
                                                    ft.Text('Green', size=17)]),
                                    on_click=lambda _: set_color_page(
                                        page, "GREEN_ACCENT_100")
                                ),
                                ft.PopupMenuItem(
                                    content=ft.Row([ft.Icon(ft.Icons.PALETTE_OUTLINED, ft.Colors.AMBER_ACCENT, size=25),
                                                    ft.Text('Yellow', size=17)]),
                                    on_click=lambda _: set_color_page(
                                        page, "AMBER_ACCENT_100")
                                ),
                                ft.PopupMenuItem(
                                    content=ft.Row([ft.Icon(ft.Icons.PALETTE_OUTLINED, ft.Colors.RED_ACCENT, size=25),
                                                    ft.Text('Red', size=17)]),
                                    on_click=lambda _: set_color_page(
                                        page, "RED_ACCENT_100")
                                ),
                                ft.PopupMenuItem(
                                    content=ft.Row([ft.Icon(ft.Icons.CANCEL, ft.Colors.RED_900, size=25),
                                                    ft.Text('Default theme', size=17)]),
                                    on_click=lambda _: set_color_page(
                                        page, None)
                                )
                            ],
                            shape=ft.RoundedRectangleBorder(radius=15)
                        )
                    ),
                    ft.Text("Extra themes", size=17, weight='bold')
                ]
            )
        ]
    )
    return panel_menu_theme
