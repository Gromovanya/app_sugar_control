import flet as ft
from datetime import datetime

HOURS_IN_A_DAY = 24
MINUTES_IN_AN_HOUR = 60
MAX_Y = 25
MIN_Y = 0

def get_current_time():
    now = datetime.now()
    current_time = now.hour * 60 + now.minute
    current_day = now.day
    current_month = now.month
    current_year = now.year
    
    return current_time, current_day, current_month, current_year

def create_chart():
    chart = ft.LineChart(
        data_series=[
            ft.LineChartData(
                data_points=[],
                stroke_width=5,
                color=ft.Colors.ORANGE,
                curved=True,
                stroke_cap_round=True,
            )
        ],
        border=ft.border.all(width=3, color=ft.Colors.with_opacity(
            opacity=0.2, color=ft.Colors.ON_SURFACE)),
        horizontal_grid_lines=ft.ChartGridLines(
            interval=1, color=ft.Colors.with_opacity(opacity=1, color=ft.Colors.ON_SURFACE), width=0.1
        ),
        vertical_grid_lines=ft.ChartGridLines(
            interval=MINUTES_IN_AN_HOUR, color=ft.Colors.with_opacity(opacity=1, color=ft.Colors.ON_SURFACE), width=0.1
        ),
        left_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=MIN_Y,
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
                    value=MAX_Y,
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
        min_y=MIN_Y,
        max_y=MAX_Y,
        min_x=MIN_Y,
        max_x=HOURS_IN_A_DAY * MINUTES_IN_AN_HOUR,
        expand=True,
    )

    for hour in range(HOURS_IN_A_DAY + 1):
        minutes_in_hour = hour * MINUTES_IN_AN_HOUR
        new_label = ft.ChartAxisLabel(
            value=minutes_in_hour,
            label=ft.Container(
                ft.Text(
                    f"{hour:02}:00",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
                margin=ft.margin.only(top=10),
            )
        )
        chart.bottom_axis.labels.append(new_label)
    
    return chart
    

def update_chart_data(chart: ft.LineChart, data_point: list):
    chart.data_series[0].data_points.extend(data_point)