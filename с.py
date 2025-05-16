import flet as ft
import pandas as pd
from pathlib import Path

file_path = 'Новая таблица (5).xlsx'

# Проверка и инициализация файла
if not Path(file_path).exists():
    pd.DataFrame([[0]], columns=['Counter']).to_excel(file_path, index=False)


def main(page: ft.Page):
    # Загрузка данных
    current_df = pd.read_excel(file_path)
    initial_count = current_df.iat[0, 0]

    # Элементы интерфейса
    num1 = ft.TextField(label="Задача", width=150)
    result_text = ft.Text()
    txt = ft.Text(value=str(initial_count), size=30)
    count = initial_count

    def kliker(e):
        nonlocal count
        if num1.value:
            count += 1  # Увеличиваем счетчик
            task_text = num1.value.strip()
            result_text.value = f"Задача: {task_text}\nВсего задач: {count}"
            txt.value = str(count)
            num1.value = ""
            page.update()

    def save(e):
        nonlocal count
        pd.DataFrame([[count]], columns=['Counter']).to_excel(file_path, index=False)
        page.add(ft.Text("Сохранено!", color=ft.colors.GREEN))
        page.update()

    # Компоновка интерфейса
    page.title = "Ежедневник"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    page.add(
        ft.Column(
            [
                txt,
                num1,
                result_text,
                ft.Row(
                    [
                        ft.ElevatedButton("Добавить задачу", on_click=kliker),
                        ft.ElevatedButton("Сохранить", on_click=save)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )


ft.app(target=main)