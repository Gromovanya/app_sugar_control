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


def create_line_chart():
    chart = ft.LineChart(
        data_series=[
            ft.LineChartData(
                data_points=[],
                stroke_width=2,
                color=ft.Colors.WHITE,
                curved=True,
                stroke_cap_round=True,
                dash_pattern=[2, 10],
            ),
            ft.LineChartData(
                data_points=[
                    ft.LineChartDataPoint(x=0, y=9.9),
                    ft.LineChartDataPoint(
                        x=HOURS_IN_A_DAY * MINUTES_IN_AN_HOUR, y=9.9)
                ],
                stroke_width=3,
                color=ft.Colors.ORANGE,
                dash_pattern=[9, 10],
            ),
            ft.LineChartData(
                data_points=[
                    ft.LineChartDataPoint(x=0, y=3.9),
                    ft.LineChartDataPoint(
                        x=HOURS_IN_A_DAY * MINUTES_IN_AN_HOUR, y=3.9)
                ],
                stroke_width=3,
                color=ft.Colors.RED,
                dash_pattern=[9, 10],

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
            labels_size=55, title=ft.Text('Sugar', size=25, weight=ft.FontWeight.BOLD), title_size=40
        ),
        bottom_axis=ft.ChartAxis(
            labels=[],
            labels_size=40
        ),
        tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY),
        tooltip_fit_inside_horizontally=True,
        bgcolor='#00001B',
        min_y=MIN_Y,
        max_y=MAX_Y,
        min_x=MIN_Y,
        max_x=HOURS_IN_A_DAY * MINUTES_IN_AN_HOUR,
        expand=True,
    )

# def create_bar_chart():
#     chart = ft.BarChart(
#         bar_groups=[
#             ft.BarChartGroup()
#         ]
#     )

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


def update_chart_data(chart: ft.LineChart, data_point: ft.LineChartDataPoint):
    if data_point:
        if data_point.y >= 10:
            data_point.point = ft.ChartCirclePoint(radius=2, stroke_width=3,
                                                color=ft.Colors.ORANGE, stroke_color=ft.Colors.ORANGE_400)
        elif data_point.y <= 3.9:
            data_point.point = ft.ChartCirclePoint(radius=2, stroke_width=3,
                                                color=ft.Colors.RED, stroke_color=ft.Colors.RED_400)
        else:
            data_point.point = ft.ChartCirclePoint(radius=2, stroke_width=3,
                                                color=ft.Colors.BLUE, stroke_color=ft.Colors.BLUE_400)
    chart.data_series[0].data_points.append(data_point)