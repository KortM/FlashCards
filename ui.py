import flet
from flet import (
    ButtonStyle,
    Checkbox,
    Column,
    Container,
    ElevatedButton,
    FilePicker,
    FilePickerUploadFile,
    FilledButton,
    FloatingActionButton,
    IconButton,
    ListView,
    Page,
    RadioGroup,
    Row,
    Text,
    TextButton,
    TextField,
    UserControl,
    border,
    colors,
    icons,
)

from db import Card, Session, User, User_session


class AdminUI(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        print("admin_ui")
        term = TextField(label="Термин", multiline=True, max_lines=2)
        definition = TextField(label="Определение", multiline=True, max_lines=4)
        self.path = []
        self.page.window_width = 700

        def upload(e):
            if image_path.result != None and image_path.result.files != None:
                for f in image_path.result.files:
                    self.path.append(
                        FilePickerUploadFile(
                            f.name, self.page.get_upload_url(f.name, 600)
                        )
                    )
                # image_path.upload(self.path)

        def new_term(e):
            if term.value and definition.value:
                session = Session()
                n_term = None
                if self.path:
                    image_path.upload(self.path)
                    n_term = Card(
                        term=term.value,
                        definition=definition.value,
                        icon_path=f"static\\{self.path[0].name}",
                    )
                else:
                    n_term = Card(
                        term=term.value, definition=definition.value, icon_path=None
                    )

                session.add(n_term)
                print(self.path, n_term)
                session.commit()
                self.path = []
                questions.controls.append(
                    Row(
                        alignment="spaceEvenly",
                        width=300,
                        scroll=True,
                        spacing=10,
                        controls=[
                            Container(
                                content=Row(
                                    controls=[
                                        Checkbox(label=term.value),
                                        Text(definition.value),
                                    ]
                                ),
                            ),
                            IconButton(
                                icon=icons.DELETE
                            ),
                        ],
                    )
                )

                self.update()

        def change_user(e):
            self.page.controls.pop()
            self.page.add(UserUI(self.page))
            self.page.vertical_alignment = "center"
            self.page.horizontal_alignment = "center"
            self.page.update()

        change_user_view = FilledButton(
            text="Сменить пользователя", icon=icons.SWITCH_ACCOUNT, on_click=change_user
        )
        image_path = FilePicker(on_result=upload)
        btn_add = FloatingActionButton(
            on_click=new_term, icon=icons.ADD, height=42, width=64, bgcolor=colors.WHITE
        )

        questions = ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        view = Row(
            height=250,
            controls=[
                Column(
                    controls=[
                        Row(alignment="center", controls=[term]),
                        Row(alignment="center", controls=[definition]),
                        Row(
                            alignment="center",
                            controls=[
                                ElevatedButton(
                                    text="Загрузить изображение",
                                    icon=icons.FILE_OPEN,
                                    on_click=lambda _: image_path.pick_files(),
                                ),
                                btn_add,
                            ],
                        ),
                        Row(alignment="center", controls=[change_user_view]),
                    ]
                ),
                questions,
            ],
        )
        view.controls.append(image_path)
        return view


class UserUI(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page

    def build(self):
        quest_label = Text(
            "Начальник департамента управления проектами", size=20, weight="bold"
        )

        def change_button(e):
            e.control.icon = icons.CHECK_CIRCLE
            e.control.bgcolor = colors.GREEN
            next.visible = True
            self.update()

        quest = RadioGroup(
            content=Column(
                [
                    FilledButton(
                        text="Иванов Иван Иванович", data="test", on_click=change_button
                    ),
                    FilledButton(text="Иванов Иван Иванович", on_click=change_button),
                    FilledButton(text="Иванов Иван Иванович", on_click=change_button),
                ]
            )
        )
        next = TextButton(text="Дальше")
        next.visible = False
        result_positive = Text("Правильно!", color=colors.GREEN, weight="bold")
        result_negative = Text("Ошибка!", color=colors.RED)

        view = Column(
            horizontal_alignment="center",
            controls=[
                Row(alignment="center", controls=[quest_label]),
                Row(alignment="center", controls=[quest]),
                Row(alignment="center", controls=[result_positive, next]),
            ],
        )
        return view


def main(page: Page):
    page.title = "FlashCard"
    login_view = TextField(label="Имя пользователя", width=300, border="outline")
    passwd_view = TextField(label="Пароль", width=300, password=True, border="outline")
    login_btn = FilledButton(
        text="Войти",
        width=300,
        icon=icons.LOGIN,
        style=ButtonStyle(color="blue"),
        height=60,
    )
    message = Text(color=colors.RED)

    view = Column(
        controls=[
            Row(alignment="center", controls=[login_view]),
            Row(alignment="center", controls=[passwd_view]),
            Row(alignment="center", controls=[login_btn]),
            Row(alignment="center", controls=[message]),
        ]
    )

    def auth(e):
        session = User_session()
        login = login_view.value
        passwd = passwd_view.value
        local_user = session.query(User).filter_by(name=login.lower()).first()
        if local_user and local_user.check_password(passwd):
            if local_user.role:
                page.controls.pop()
                page.add(AdminUI(page))
                page.vertical_alignment = "start"
                page.horizontal_alignment = "start"
                page.update()
            else:
                page.controls.pop()
                page.add(UserUI(page))
                page.update()
        else:
            message.value = "Неверные имя пользователя/пароль!"
            page.update()

    # page.on_route_change = route_change

    login_btn.on_click = auth

    # page.window_resizable =False
    page.window_width = 350
    page.window_height = 350
    page.window_maximized = False
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.add(view)


flet.app(target=main, upload_dir="assets")
