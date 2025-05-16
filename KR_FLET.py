import flet as ft
import pandas as pd


file_path = 'Новая таблица (5).xlsx'


df_excel = pd.read_excel(file_path)


def main(page: ft.Page):
    page.title = "Кликер"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    # Загружаем данные при каждом запуске программы
    current_df = pd.read_excel(file_path)
    initial_count = current_df.iat[0, 0]

    txt = ft.Text(value=str(initial_count), size=30)
    count = initial_count

    def kliker(e):
        nonlocal count
        count += 1
        txt.value = str(count)
        page.update()

    def clean(e):
        nonlocal count
        count = 0
        txt.value = str(count)
        page.update()

    def save(e):
        nonlocal count
        new_df = pd.DataFrame([[count]], columns=['Значение'])
        new_df.to_excel(file_path, index=False)

        # Показываем подтверждение
        page.add(ft.Text(f"Сохранено", ))
        print(new_df)
        page.update()

    page.add(
        ft.Column(
            [
                txt,
                ft.Row(
                    [
                        ft.ElevatedButton("+", on_click=kliker),
                        ft.ElevatedButton("Сброс", on_click=clean),
                        ft.ElevatedButton("Сохранить", on_click=save)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )


ft.app(target=main)