import flet as ft
from char_manager import (
    create_line_chart,
    update_chart_data
)
from event_handlers import (
    delete_chart,
    renewal_text_stats,
    modify_setting
)
from create_widgets import (
    create_panel_statistics,
    create_panel_menu,
    create_input_sugar,
    create_panel_menu_theme
)
from db_manager import (
    fetch_statistics,
    create_table,
    connect_db
)
from get_data import (
    get_current_time
)


def main(page: ft.Page):
    page.title = "Glucose 24/7"
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.adaptive = True

    page.window_width = 1200
    page.window_height = 1000

    chart = create_line_chart()
    statistics = create_panel_statistics()

    panel_input_sugar = create_input_sugar(chart, page, statistics)
    panel_menu_theme = create_panel_menu_theme(page, chart)
    panel_menu = create_panel_menu(page, chart, statistics, panel_input_sugar, panel_menu_theme)

    page.add(panel_menu, chart, panel_menu_theme)

    db = connect_db()
    create_table(db)
    stats = fetch_statistics(db)
    rows = stats['rows']
    db.close()
    # print(rows)

    current_time = get_current_time()

    for row in rows:
        update_chart_data(chart, ft.LineChartDataPoint(row[2], row[1]))

        if row[3] != current_time[1] or row[4] != current_time[2] or row[5] != current_time[3]:
            delete_chart(chart, page, statistics)
            # print('Таблица очищена')
    # print("Данные добавлены в график.")

    renewal_text_stats(statistics)
    modify_setting(page, chart, panel_menu_theme, panel_input_sugar, statistics)


if __name__ == "__main__":
    ft.app(target=main)
