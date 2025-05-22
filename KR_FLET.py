import flet as ft
import pandas as pd
import calendar
from datetime import datetime
import os
import sys

df_excel = pd.DataFrame(columns=["Время", "Название", "Количество", "Мера", "Период"])

def get_desktop_path():
    if sys.platform == "win32":
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
        )
        return winreg.QueryValueEx(key, "Desktop")[0]
    else:
        return os.path.join(os.path.expanduser("~"), "Desktop")

def main(page: ft.Page):
    page.title = "Умная таблетница"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    # Элементы ввода
    hour_tf = ft.TextField(
        label="Часы (00-23)",
        width=100,
        text_align=ft.TextAlign.CENTER,
        keyboard_type=ft.KeyboardType.NUMBER
    )

    minute_tf = ft.TextField(
        label="Минуты (00-59)",
        width=100,
        text_align=ft.TextAlign.CENTER,
        keyboard_type=ft.KeyboardType.NUMBER
    )

    name_pill = ft.TextField(
        label="Название",
        width=150,
        text_align=ft.TextAlign.CENTER
    )

    volume = ft.TextField(
        label="Количество",
        width=150,
        text_align=ft.TextAlign.CENTER
    )

    volumet = ft.TextField(
        label="Мера",
        width=150,
        text_align=ft.TextAlign.CENTER
    )

    status = ft.Text(size=20)
    current_period = "Месяц"
    selected_day = datetime.now().day
    selected_month = datetime.now().month
    selected_year = datetime.now().year

    # Кнопки выбора периода
    def on_click_month(e):
        nonlocal current_period
        current_period = "Месяц"
        status.value = f"Выбран период: {current_period}"
        status.color = ft.colors.BLUE
        page.update()

    month_btn = ft.ElevatedButton("Месяц", on_click=on_click_month)

    def on_click_day(e):
        nonlocal current_period
        current_period = "День"
        status.value = f"Выбран период: {current_period}"
        status.color = ft.colors.BLUE
        page.update()

    day_btn = ft.ElevatedButton("День", on_click=on_click_day)

    def on_click_week(e):
        nonlocal current_period
        current_period = "Неделя"
        status.value = f"Выбран период: {current_period}"
        status.color = ft.colors.BLUE
        page.update()

    week_btn = ft.ElevatedButton("Неделя", on_click=on_click_week)

    def save_to_excel(e):
        try:
            desktop = get_desktop_path()
            file_path = os.path.join(desktop, "Таблетница.xlsx")
            df_excel.to_excel(file_path, index=False)
            status.value = f"Файл сохранен!\nПуть: {file_path}"
            status.color = ft.colors.GREEN
            page.update()
        except Exception as e:
            status.value = f"Ошибка: {str(e)}"
            status.color = ft.colors.RED
            page.update()

    def clear_fields():
        hour_tf.value = ""
        minute_tf.value = ""
        name_pill.value = ""
        volume.value = ""
        volumet.value = ""
        page.update()

    def show_list(e):
        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Название", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Время", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Количество", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Мера", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Период", weight=ft.FontWeight.BOLD)),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(row["Название"]))),
                        ft.DataCell(ft.Text(str(row["Время"]))),
                        ft.DataCell(ft.Text(str(row["Количество"]))),
                        ft.DataCell(ft.Text(str(row["Мера"]))),
                        ft.DataCell(ft.Text(str(row["Период"]))),
                    ]
                ) for _, row in df_excel.iterrows()
            ],
            column_spacing=20,
            heading_row_color=ft.colors.BLUE_GREY_100,
        )

        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Text("Список записей", size=20, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=data_table,
                        padding=10,
                        border=ft.border.all(1, ft.colors.GREY_300),
                    ),
                    ft.Row([
                        ft.ElevatedButton("Назад", on_click=show_main_page),
                        ft.ElevatedButton("Сохранить", on_click=save_to_excel),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

    def show_calendar(e):
        page.clean()
        current_year = selected_year
        current_month = selected_month

        month_names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                       "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

        header = ft.Text(
            value=f"{month_names[current_month - 1]} {current_year}",
            size=24,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        def select_date(e):
            nonlocal current_period
            current_period = f"{selected_day:02d}.{current_month:02d}.{current_year}"
            status.value = f"Выбрана дата: {current_period}"
            status.color = ft.colors.BLUE
            show_main_page(None)

        def prev_month(e):
            nonlocal current_month, current_year
            current_month -= 1
            if current_month == 0:
                current_month = 12
                current_year -= 1
            header.value = f"{month_names[current_month - 1]} {current_year}"
            update_calendar()

        def next_month(e):
            nonlocal current_month, current_year
            current_month += 1
            if current_month == 13:
                current_month = 1
                current_year += 1
            header.value = f"{month_names[current_month - 1]} {current_year}"
            update_calendar()

        nav_buttons = ft.Row(
            controls=[
                ft.IconButton(ft.icons.ARROW_BACK, on_click=prev_month),
                ft.IconButton(ft.icons.ARROW_FORWARD, on_click=next_month),
                ft.ElevatedButton("Выбрать", on_click=select_date),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        selected_date_display = ft.Text(
            value=f"Выбрано: {selected_day:02d}.{current_month:02d}.{current_year}",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLUE,
        )

        calendar_grid = ft.Column(spacing=10)

        def update_calendar():
            calendar_grid.controls.clear()
            weekday_names = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
            week_header = ft.Row(
                controls=[ft.Text(day, width=40, text_align=ft.TextAlign.CENTER)
                          for day in weekday_names],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            )
            calendar_grid.controls.append(week_header)

            cal = calendar.monthcalendar(current_year, current_month)
            for week_days in cal:
                week_row = ft.Row()
                for day in week_days:
                    if day == 0:
                        week_row.controls.append(
                            ft.Container(width=40, height=40)
                        )
                        continue
                    day_btn = ft.ElevatedButton(
                        text=str(day),
                        width=40,
                        height=40,
                        bgcolor=ft.colors.BLUE_100 if day == selected_day else None,
                        on_click=lambda e, d=day: select_day(d)
                    )
                    week_row.controls.append(day_btn)
                calendar_grid.controls.append(week_row)
            page.update()

        def select_day(day):
            nonlocal selected_day
            selected_day = day
            selected_date_display.value = f"Выбрано: {selected_day:02d}.{current_month:02d}.{current_year}"
            update_calendar()

        back_button = ft.ElevatedButton(
            "Назад",
            on_click=show_main_page,
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE,
        )

        update_calendar()

        page.add(ft.Column(
            [
                header,
                nav_buttons,
                selected_date_display,
                calendar_grid,
                back_button
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ))

    def show_main_page(e=None):
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Text("Умная таблетница", size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=20),

                    ft.Text("Время приема:", size=16),
                    ft.Row([hour_tf, minute_tf], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Text("Детали:", size=16),
                    name_pill,
                    volume,
                    volumet,

                    ft.Text("Период:", size=16),
                    ft.Row([day_btn, week_btn, month_btn], alignment=ft.MainAxisAlignment.CENTER),
                    ft.ElevatedButton("Выбрать дату", on_click=show_calendar),

                    ft.Divider(height=20),
                    ft.Row([
                        ft.ElevatedButton("Добавить", on_click=add_pill),
                        ft.ElevatedButton("Список", on_click=show_list),
                        ft.ElevatedButton("Сохранить", on_click=save_to_excel),
                    ], spacing=20),
                    status
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    def add_pill(e):
        try:
            if not all([hour_tf.value, minute_tf.value, name_pill.value, volume.value]):
                raise ValueError("Заполните все обязательные поля!")

            h = int(hour_tf.value)
            m = int(minute_tf.value)
            if not (0 <= h < 24 and 0 <= m < 60):
                raise ValueError("Некорректное время!")

            new_data = {
                "Время": f"{h:02d}:{m:02d}",
                "Название": name_pill.value,
                "Количество": volume.value,
                "Мера": volumet.value,
                "Период": current_period if current_period in ["День", "Неделя", "Месяц"]
                else f"{selected_day:02d}.{selected_month:02d}.{selected_year}"
            }

            global df_excel
            df_excel = pd.concat([df_excel, pd.DataFrame([new_data])], ignore_index=True)
            status.value = "Запись добавлена!"
            status.color = ft.colors.GREEN
            clear_fields()
            page.update()

        except Exception as e:
            status.value = f"Ошибка: {str(e)}"
            status.color = ft.colors.RED
            page.update()

    show_main_page()

ft.app(target=main)
