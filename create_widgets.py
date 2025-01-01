import flet as ft
from event_handlers import (
    delete_chart,
    theme_dark_and_light,
    set_color_page,
    modify_page_and_settings,
    register_sugar,
    on_change_sugar
)
from json_manager import update_json_file
from constants import (
    KEY_INPUT_SUGAR,
    KEY_STATISTICS,
    SETTING_PATH_FILE,
    NOT_DATA
)

def create_row_with_label_and_text(label: str, text: ft.Text) -> ft.Row:
    return ft.Row([ft.Text(label, size=20), text], alignment=ft.MainAxisAlignment.CENTER)

def create_panel_statistics() -> ft.Column:
    stats_labels = [
        ("Среднее значение сахара: ", NOT_DATA),
        ("Максимальное значение сахара: ", NOT_DATA),
        ("Минимальное значение сахара: ", NOT_DATA),
        ("Количество замерок сахара: ", "0"),
    ]

    statistics = ft.Column(
        [
            ft.Row([ft.Text("Статистика за день", size=24)], alignment=ft.MainAxisAlignment.CENTER),
            *[create_row_with_label_and_text(label, ft.Text(stat, size=20)) for label, stat in stats_labels]
        ]
    )
    return statistics

def create_input_sugar(chart: ft.LineChart, page: ft.Page, statistics: ft.Column) -> ft.Column:
    input_sugar = ft.TextField(
        label='Введите сахар (ммоль/л)', width=230, on_change=lambda _: on_change_sugar(input_sugar, btn_upd_sugar))
    
    timer_glav = ft.Text("00:00", size=27)
    
    btn_upd_sugar = ft.OutlinedButton(
        text='Ввести', width=230, on_click=lambda _:
            register_sugar(input_sugar, btn_upd_sugar, timer_glav, chart, page, statistics), disabled=True)

    panel_input_sugar = ft.Column(
        [
            ft.Row([ft.Icon(ft.icons.TIMER, size=25)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([timer_glav], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text('Ввод показаний сахара', size=15, weight=ft.FontWeight.BOLD),
                            input_sugar,
                            btn_upd_sugar
                        ]
                    )
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        alignment=ft.alignment.center_left
    )
    
    return panel_input_sugar

def create_panel_menu(page: ft.Page, chart: ft.LineChart, statistics: ft.Column, panel_input_sugar: ft.Column,
                        panel_menu_theme: ft.Container) -> ft.Container:
    panel_menu = ft.Container(
        content=ft.PopupMenuButton(
            icon=ft.icons.MENU,
            items=[
                ft.PopupMenuItem(icon=ft.icons.MENU, text='Menu'),
                ft.PopupMenuItem(),
                ft.PopupMenuItem(
                    icon=ft.icons.AREA_CHART, text='Graph',
                    on_click=lambda _: (
                        page.clean(),
                        page.add(panel_menu, chart, panel_menu_theme),
                        update_json_file(KEY_INPUT_SUGAR, False, SETTING_PATH_FILE),
                        update_json_file(KEY_STATISTICS, False, SETTING_PATH_FILE)
                    )
                ),
                ft.PopupMenuItem(
                    icon=ft.icons.ADD_CHART, text='Input sugar',
                    on_click=lambda _: modify_page_and_settings(page, panel_input_sugar, KEY_INPUT_SUGAR, (KEY_STATISTICS,))
                ),
                ft.PopupMenuItem(
                    icon=ft.icons.SSID_CHART, text='Statistics',
                    on_click=lambda _: modify_page_and_settings(page, statistics, KEY_STATISTICS, (KEY_INPUT_SUGAR,))
                ),
                ft.PopupMenuItem(
                    icon=ft.icons.DELETE, text='Full cleaning the data of charts',
                    on_click=lambda _: delete_chart(chart, page, statistics)
                ),
            ],
        ),
        alignment=ft.alignment.top_left
    )
    return panel_menu

def create_panel_menu_theme(page: ft.Page, line_chart: ft.LineChart) -> ft.Column:
    colors = [
        ("DEEP_PURPLE_ACCENT", "Deep-purple"),
        ("PINK_ACCENT", "Pink"),
        ("BLUE_ACCENT", "Blue"),
        ("DEEP_ORANGE_ACCENT_100", "Deep-orange"),
        ("GREEN_ACCENT", "Green"),
        ("AMBER_ACCENT", "Yellow"),
        ("RED_ACCENT", "Red")
    ]

    color_items = [
        ft.PopupMenuItem(
            content=ft.Row([ft.Icon(ft.Icons.PALETTE_OUTLINED, getattr(ft.Colors, color_code), size=25),
                            ft.Text(color_name, size=17)]),
            on_click=lambda e, color_code=color_code: set_color_page(page, color_code)
        ) for color_code, color_name in colors
    ]

    color_items.append(
        ft.PopupMenuItem(
            content=ft.Row([ft.Icon(ft.Icons.CANCEL, ft.Colors.RED_900, size=25),
                            ft.Text('Default theme', size=17)]),
            on_click=lambda _: set_color_page(page, None)
        )
    )

    panel_menu_theme = ft.Column(
        controls=[
            ft.Row(
                [
                    ft.IconButton(icon=ft.icons.LIGHT_MODE, on_click=lambda _: theme_dark_and_light(page, line_chart, panel_menu_theme)),
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
                            items=color_items,
                            shape=ft.RoundedRectangleBorder(radius=15)
                        )
                    ),
                    ft.Text("Extra themes", size=17, weight='bold')
                ]
            )
        ]
    )
    return panel_menu_theme
