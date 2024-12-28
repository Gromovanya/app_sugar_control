import flet as ft
from char_manager import create_line_chart, get_current_time, update_chart_data
from event_handlers import on_change_sugar, register_sugar, delete_chart, renewal_statistics
from create_widgets import create_panel_statistics, create_panel_menu, create_input_sugar, create_panel_menu_theme
from db_manager import fetch_statistics, create_table, connect_db


def main(page: ft.Page):
    page.title = "Sugar data Analyst"
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.adaptive = True
    
    page.window_width = 1200
    page.window_height = 1000

    chart = create_line_chart()
    input_sugar = ft.TextField(
        label='Введите сахар (ммоль/л)', width=230, on_change=lambda e: on_change_sugar(input_sugar, btn_upd_sugar))
    timer_glav = ft.Text("00:00", size=27)
    avg_stat = ft.Text('Пока нет данных', size=20)
    max_stat = ft.Text('Пока нет данных', size=20)
    min_stat = ft.Text('Пока нет данных', size=20)
    count_stat = ft.Text('Пока нет данных', size=20)
    btn_upd_sugar = ft.OutlinedButton(
        text='Ввести', width=230, on_click=lambda e:
            register_sugar(input_sugar, btn_upd_sugar, timer_glav, chart, page, avg_stat,
                            max_stat, min_stat, count_stat), disabled=True)

    panel_input_sugar = create_input_sugar(timer_glav, input_sugar, btn_upd_sugar)

    panel_statistics = create_panel_statistics(avg_stat, max_stat, min_stat, count_stat)
    
    panel_menu_theme = create_panel_menu_theme(page, chart)
    
    panel_menu = create_panel_menu(page, chart, panel_statistics, panel_input_sugar,
                                avg_stat, max_stat, min_stat, count_stat, panel_menu_theme)
    
    delete_db = False

    db = connect_db("db_registr.sugar")
    create_table(db)
    stats = fetch_statistics(db)
    rows = stats['rows']
    db.close()
    
    current_time = get_current_time()
    for row in rows:
        if row[3] != current_time[1] or row[4] != current_time[2] or row[5] != current_time[3]:
            delete_db = True
            break

    if delete_db:
        delete_chart(chart, "db_registr.sugar", page, avg_stat, max_stat, min_stat, count_stat)
        print('Таблица очищена')
    else:
        for row in rows:
            update_chart_data(chart, ft.LineChartDataPoint(row[2], row[1]))
            
        renewal_statistics(stats, avg_stat, max_stat, min_stat, count_stat)
        print("Данные добавлены в график.")
    page.add(panel_menu, chart, panel_menu_theme)


if __name__ == "__main__":
    ft.app(target=main)
