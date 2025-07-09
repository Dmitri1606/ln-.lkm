import flet as ft
import datetime
import json
import os
import sqlite3


class PatientChat:
    def __init__(self, patient_name):
        self.patient_name = patient_name
        self.messages = []
        self.chat_ui = ft.ListView(expand=True, spacing=10, auto_scroll=True)

    def add_message(self, sender, text):
        current_time = datetime.datetime.now().strftime("%H:%M")
        self.messages.append({
            "sender": sender,
            "text": text,
            "time": current_time
        })
        self.update_chat_ui()

    def update_chat_ui(self):
        self.chat_ui.controls.clear()
        for msg in self.messages:
            self.chat_ui.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"{msg['sender']} ({msg['time']})",
                                weight="bold", size=12),
                        ft.Text(msg['text'])
                    ]),
                    bgcolor=ft.Colors.BLUE_100 if msg['sender'] == "Вы" else ft.Colors.GREEN_100,
                    border_radius=10,
                    padding=10,
                    margin=5,
                    width=300,
                    alignment=ft.alignment.top_left if msg['sender'] == "Вы" else ft.alignment.top_right
                )
            )
class Medication:
    def __init__(self, tablet_name,quantity,time_drink,end_course,dosage_unit,comments):
        self.tablet_name = tablet_name
        self.quantity = quantity
        self.time_drink=time_drink
        self.end_course=end_course
        self.dosage_unit=dosage_unit
        self.comments=comments
class TreatmentCourse:
    def __init__(self,start_date,end_date,course_name ,list_medications):
        self.patients = {
            "Иванов И.И.": PatientChat("Иванов И.И."),
            "Петрова С.К.": PatientChat("Петрова С.К."),
            "Сидоров А.В.": PatientChat("Сидоров А.В.")
        }
        self.course_name  = course_name
        self.list_medications=list_medications
        self.start_date=start_date
        self.end_date=end_date








class AuthManager:
    USERS_FILE = "users.json"

    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.USERS_FILE):
            with open(self.USERS_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_users(self):
        with open(self.USERS_FILE, "w") as f:
            json.dump(self.users, f)

    def register(self, username, password):
        if username in self.users:
            return False
        self.users[username] = {"password": password}
        self.save_users()
        return True

    def login(self, username, password):
        user = self.users.get(username)
        if user and user["password"] == password:
            return True
        return False


class MedicalApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.auth_manager = AuthManager()
        self.show_login_screen()
        self.treatment_courses = []
        self.current_course = None
        self.pills = []


    def curses_screen(self) -> None:
        self.page.clean()
        self.course_name = ft.TextField(label="Название", width=300)
        self.start_date = ft.TextField(label="Формата ДД ММ ГГГГ",  width=300)
        self.end_date = ft.TextField(label="Формата ДД ММ ГГГГ", width=300)
        name = ft.Column([
            ft.Text("Ведите название", size=15, weight="bold")
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        start = ft.Column([ft.Text("Ведите дату начало", size=15, weight="bold"),
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        end = ft.Column([ft.Text("Ведите дату конца", size=15, weight="bold"),
                                  ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        create_btn = ft.ElevatedButton("Создать новый курс", icon=ft.Icons.ADD, on_click=lambda _: self.ffff(

            self.course_name,
            self.start_date,
            self.end_date,
        ))
        nazad=ft.ElevatedButton("Назад",  on_click=lambda _: self.show_courses_screen())
        self.page.add(name,
                      self.course_name,
                      start,
                      self.start_date,
                      end,
                      self.end_date,
                      create_btn,
                      nazad
                      )

    def pills_creat(self):
        self.time_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(t) for t in ["Таблетка", "Капсула", "Драже", "Миллиграм","Грамм", "Капля", "Микрограмм", "Литр"]],
            label="Еденица измерение",
            width=400,
            editable=True
        )

        self.pills_coment = ft.TextField(label="Коментарий", width=300)
        self.time_pickerr=ft.TextField(label="Время формата ЧЧ:ММ", width=300)
        self.page.clean()
        self.pills_name = ft.TextField(label="Название", width=300)
        self.pills_quantity = ft.TextField(label="Количество", width=300)
        nazad = ft.ElevatedButton("Назад", on_click=lambda _: self.pills_def(self.course_id))
        create_btn = ft.ElevatedButton("Добавить", icon=ft.Icons.ADD, on_click=lambda _: self.pills_add(
        ))
        self.page.add(
            ft.Text(f"Добавление препората в курс: {self.course_nam}", size=20),
            self.pills_name,
            self.time_dropdown,
            self.pills_quantity,
            self.time_pickerr,
            self.pills_coment,
            nazad,
            create_btn
                      )
    def pills_add(self):
        connect = sqlite3.connect(';.sqlite')
        cursor = connect.cursor()



        self.name_pills = self.pills_name.value
        self.col_pills = self.time_dropdown.value
        self.quantity_pills = self.pills_quantity.value
        self.coment_pills = self.pills_coment.value
        self.time_pills = self.time_pickerr.value
        self.pills_def(self.course_id)
        print(1)

        cursor.execute("""
                INSERT INTO PILLSs (NAMECURS, NAME, COL, QUANTITY, COMENT, TIME) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.course_nam, self.name_pills, self.col_pills, self.quantity_pills, self.coment_pills, self.time_pills))
        connect.commit()
        cursor.execute("SELECT * FROM PILLSs")
        pills_data = cursor.fetchall()

        print("Данные в таблице PILLS:")
        for row in pills_data:
            print(row)

        print(3)
        self.pills_def(self.course_id)
    def pills_def(self, course_id):

        self.course_id = course_id
        connect = sqlite3.connect(';.sqlite')
        cursor = connect.cursor()

        cursor.execute("""
                SELECT NAME
                FROM CURS 
                WHERE id = ?
            """, (self.course_id,))
        course_data = cursor.fetchone()
        self.course_nam = course_data[0]
        connect.close()
        nazad = ft.ElevatedButton("Назад", on_click=lambda _: self.show_courses_screen())
        self.page.clean()
        pills_tekst = ft.Column([
            ft.Text(f"Куpс: {self.course_nam}", size=15),
            ft.Text("Препараты:", size=20, weight="bold"),
            ft.ElevatedButton("Добавить новый препарат",
                              on_click=lambda _: self.pills_creat()),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        print(self.course_nam)
        connect = sqlite3.connect(';.sqlite')
        cursor = connect.cursor()
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS PILLSs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        NAMECURS TEXT,
                        NAME TEXT,           
                        COL TEXT,   
                        QUANTITY TEXT,
                        COMENT TEXT,
                        TIME TEXT    
                    )
                """)

        cursor.execute("SELECT NAMECURS, NAME, COL, QUANTITY, COMENT, TIME FROM PILLSs WHERE NAMECURS=?",
                       (self.course_nam,))
        all_pillse = cursor.fetchall()
        connect.close()
        self.pills = []
        for pillse in all_pillse:
            namecurse, name_pilss, COL_pills, end_date, qs, qss = pillse
            self.pills.append(ft.Column(
                [ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f" {name_pilss} {end_date} {COL_pills}",
                                    weight=ft.FontWeight.BOLD),
                            ft.Text(f"{qss} | {qs}",
                                    color=ft.Colors.GREY_600)
                        ], spacing=5),
                        padding=15,
                        width=400
                    )
                )]))
        add_tablets = ft.Column([
            pills_tekst,
            *self.pills,
            nazad
        ], expand=True)
        self.page.add(add_tablets)



    def ffff(self, name_field, start_field, end_field):
        self.name_curs = name_field.value
        self.start_curs = start_field.value
        self.end_curs = end_field.value
        connect = sqlite3.connect(';.sqlite')
        cursor = connect.cursor()
        cursor.execute("""
                    INSERT INTO CURS (NAME, START_TIME, END_TIME) 
                    VALUES (?, ?, ?)
                """, (self.name_curs, self.start_curs, self.end_curs,))
        connect.commit()



        self.show_courses_screen()

    def show_courses_screen(self) -> None:
        self.page.clean()
        self.patient_buttonsS = [
            ft.ElevatedButton(
                text=name,
                on_click=self.select_patient,
                width=200,
                style=ft.ButtonStyle(
                    padding=10,
                    shape=ft.RoundedRectangleBorder(radius=10)
                )) for name in self.patients.keys()
        ]
        connect = sqlite3.connect(';.sqlite')
        cursor = connect.cursor()
        cursor.execute("SELECT id, NAME, START_TIME, END_TIME FROM CURS")
        all_courses = cursor.fetchall()
        connect.close()
        self.course_buttons = []
        for course in all_courses:
            course_id, name, start_date, end_date = course

            # Создаем обработчик с привязкой к конкретному course_id
            def create_handler(cid):
                return lambda _: self.pills_def(cid)

            course_content = ft.Column(
                controls=[
                    ft.Text(name, size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Даты: {start_date} - {end_date}",
                            size=14, color=ft.Colors.GREY_600)
                ]
            )

            self.course_buttons.append(
                ft.ElevatedButton(
                    content=course_content,
                    style=ft.ButtonStyle(padding=20),
                    on_click=create_handler(course_id)  # Используем обработчик с привязкой
                ))

        pat=ft.Column(
                [
                    ft.Text("Пациенты", size=20, weight="bold"),
                    *self.patient_buttonsS
                ],
                width=250,
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.START
            )
        top_bar = ft.Row([
            ft.IconButton(icon=ft.Icons.MENU, on_click=self.show_drawer),
            ft.Text("Курсы лечения", size=20, weight="bold"),
            ft.IconButton(icon=ft.Icons.LOGOUT, on_click=lambda _: self.show_login_screen())
        ], spacing=20)
        create_btn = ft.ElevatedButton("Создать новый курс", icon=ft.Icons.ADD,on_click=lambda _: self.curses_screen())
        courses_list = ft.Column()
        content = ft.Column([
            top_bar,
            pat,
            ft.Text("Список курсов:", size=16, weight="bold"),
            *self.course_buttons,
            create_btn,
            courses_list
        ], expand=True)
        self.page.add(content)
    def show_login_screen(self):
        self.page.clean()

        self.login_username = ft.TextField(label="Логин", width=300)
        self.login_password = ft.TextField(label="Пароль", password=True, width=300)
        self.login_error = ft.Text("", color="red")

        self.register_username = ft.TextField(label="Логин", width=300)
        self.register_password = ft.TextField(label="Пароль", password=True, width=300)
        self.register_error = ft.Text("", color="red")
        self.register_success = ft.Text("", color="green")

        login_form = ft.Column([
            ft.Text("Вход", size=20, weight="bold"),
            self.login_username,
            self.login_password,
            ft.ElevatedButton("Войти", on_click=self.on_login),
            self.login_error,
            ft.Divider(),
            ft.Text("Еще нет аккаунта?", size=16),
            ft.ElevatedButton("Регистрация", on_click=lambda _: self.toggle_auth_forms())
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        register_form = ft.Column([
            ft.Text("Регистрация", size=20, weight="bold"),
            self.register_username,
            self.register_password,
            ft.ElevatedButton("Зарегистрироваться", on_click=self.on_register),
            self.register_error,
            self.register_success,
            ft.Divider(),
            ft.Text("Уже есть аккаунт?", size=16),
            ft.ElevatedButton("Войти", on_click=lambda _: self.toggle_auth_forms())
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, visible=False)

        self.auth_container = ft.Container(
            content=ft.Column([
                login_form,
                register_form
            ], spacing=30),
            alignment=ft.alignment.center,
            expand=True
        )

        self.page.add(self.auth_container)

    def toggle_auth_forms(self):
        login_form = self.auth_container.content.controls[0]
        register_form = self.auth_container.content.controls[1]

        login_form.visible = not login_form.visible
        register_form.visible = not register_form.visible

        self.login_error.value = ""
        self.register_error.value = ""
        self.register_success.value = ""

        self.page.update()

    def on_login(self, e):
        username = self.login_username.value
        password = self.login_password.value

        if not username or not password:
            self.login_error.value = "Заполните все поля"
            self.page.update()
            return

        if self.auth_manager.login(username, password):
            self.login_error.value = ""
            self.setup_main_app(username)
        else:
            self.login_error.value = "Неверный логин или пароль"
            self.page.update()

    def on_register(self, e):
        username = self.register_username.value
        password = self.register_password.value

        if not username or not password:
            self.register_error.value = "Заполните все поля"
            self.page.update()
            return

        if len(password) < 6:
            self.register_error.value = "Пароль должен быть не менее 6 символов"
            self.page.update()
            return

        if self.auth_manager.register(username, password):
            self.register_error.value = ""
            self.register_success.value = "Регистрация успешна! Теперь вы можете войти."
            self.register_username.value = ""
            self.register_password.value = ""
            self.page.update()
        else:
            self.register_error.value = "Пользователь с таким логином уже существует"
            self.page.update()

    def setup_main_app(self, username):
        self.page.clean()
        self.setup_page(username)
        self.setup_patients()
        self.setup_ui()
        self.setup_drawer()
        self.chat_created = False
        self.chat_controls = None


    def setup_page(self, username):
        self.page.title = f"Пользoватель - {username}"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.add(
            ft.Row([
                ft.IconButton(icon=ft.Icons.MENU, on_click=self.show_drawer),
                ft.Text(f"Пользoватель - {username}", size=20, weight="bold"),
                ft.IconButton(icon=ft.Icons.LOGOUT, on_click=lambda _: self.show_login_screen())
            ], spacing=20)
        )

    def setup_patients(self):

        self.patients = {
            "Иванов И.И.": PatientChat("Иванов И.И."),
            "Петрова С.К.": PatientChat("Петрова С.К."),
            "Сидоров А.В.": PatientChat("Сидоров А.В.")
        }
        self.current_patient = None
        self.new_message = ft.TextField(hint_text="Сообщение...", expand=True)
        self.chat_column = ft.Column(controls=[ft.Text("Выберите пациента")], expand=True)

    def setup_ui(self):
        self.patient_buttons = [
            ft.ElevatedButton(
                text=name,
                on_click=self.select_patient,
                width=200,
                style=ft.ButtonStyle(
                    padding=10,
                    shape=ft.RoundedRectangleBorder(radius=10)
                )) for name in self.patients.keys()
        ]

    def setup_drawer(self):
        self.page.drawer = ft.NavigationDrawer(
            selected_index=-1,
            on_change=self.drawer_changed,
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    label="Чат с пациентами",
                    icon=ft.Icons.CHAT_BUBBLE_OUTLINE,
                    selected_icon=ft.Icons.CHAT_BUBBLE,
                ),
                ft.NavigationDrawerDestination(
                    label="Очередь пациента",
                    icon=ft.Icons.STAR_BORDER,
                    selected_icon=ft.Icons.STAR,
                ),
                ft.NavigationDrawerDestination(
                    label="Курсы лечение",
                    icon=ft.Icons.HEALING,
                    selected_icon=ft.Icons.HEALING,
                ),
                ft.Divider(),
                ft.NavigationDrawerDestination(
                    label="Настройки",
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.SETTINGS,
                ),
            ],
        )

    def drawer_changed(self, e):
        selected_index = e.control.selected_index

        if selected_index == 0:
            if not self.chat_created:
                self.select_chat()
                self.chat_created = True
            else:
                self.page.controls.clear()
                self.page.add(
                    ft.Row([
                        ft.IconButton(icon=ft.Icons.MENU, on_click=self.show_drawer),
                        ft.Text(f"Мед. Чат - {self.page.title.split('-')[-1].strip()}", size=20, weight="bold"),
                        ft.IconButton(icon=ft.Icons.LOGOUT, on_click=lambda _: self.show_login_screen())
                    ], spacing=20)
                )
                self.page.add(self.chat_controls)
        elif selected_index == 1:
            pass
        elif selected_index == 2:
          self.show_courses_screen()
        self.page.update()

    def show_drawer(self, e):
        self.page.drawer.open = True
        self.page.update()

    def send_message(self, e):
        if self.current_patient and self.new_message.value:
            self.patients[self.current_patient].add_message("Вы", self.new_message.value)
            self.new_message.value = ""
            self.page.update()

    def select_patient(self, e):
        self.current_patient = e.control.text
        self.chat_column.controls.clear()
        self.chat_column.controls.append(self.patients[self.current_patient].chat_ui)
        self.page.update()

    def select_chat(self):
        self.chat_controls = ft.Row([
            ft.Column(
                [
                    ft.Text("Пациенты", size=20, weight="bold"),
                    *self.patient_buttons
                ],
                width=250,
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.START
            ),
            ft.Column(
                [
                    ft.Text("Чат с пациентом", size=20, weight="bold"),
                    ft.Container(
                        content=self.chat_column,
                        border=ft.border.all(1),
                        border_radius=5,
                        padding=10,
                        expand=True
                    ),
                    ft.Row(
                        [
                            self.new_message,
                            ft.IconButton(
                                icon=ft.Icons.SEND,
                                on_click=self.send_message,
                                tooltip="Отправить"
                            )
                        ]
                    )
                ],
                expand=True
            )
        ], expand=True)

        self.page.add(self.chat_controls)



def main(page: ft.Page):
    MedicalApp(page)


ft.app(target=main)
