
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
    Image,
    Icon,
    border_radius,
    GridView
)
import random
from db import Card, Session, User, User_session


class AdminUI(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        term = TextField(label="Термин", multiline=True, max_lines=2)
        definition = TextField(label="Определение", multiline=True, max_lines=4)
        self.path = []
        self.page.window_width = 700
        self.page.window_height = 300

        def upload(e):
            if image_path.result != None and image_path.result.files != None:
                for f in image_path.result.files:
                    self.path.append(
                        FilePickerUploadFile(
                            f.name, self.page.get_upload_url(f.name, 600)
                        )
                    )

        def new_term(e):
            if term.value and definition.value:
                session = Session()
                n_term = None
                if self.path:
                    image_path.upload(self.path)
                    n_term = Card(
                        term=term.value,
                        definition=definition.value,
                        icon_path=f"{self.path[0].name}",
                    )
                else:
                    n_term = Card(
                        term=term.value, definition=definition.value, icon_path=None
                    )

                session.add(n_term)
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
                            IconButton(icon=icons.DELETE, on_click=delete_card),
                        ],
                    )
                )
                update_cards()
                self.update()

        def change_user(e):
            self.page.controls.pop()
            user_ui = UserUI(self.page)
            self.page.add(user_ui)
            user_ui.generate_quests()
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

        def delete_card(e):
            session = Session()
            tmp = session.query(Card).filter_by(id=e.control.data).first()
            session.delete(tmp)
            session.commit()
            questions.controls.clear()
            self.update()
            update_cards()
            self.update()
            self.page.update()

        questions = ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        def update_cards():
            questions.controls.clear()
            cards_session = Session()
            cards = cards_session.query(Card).all()
            for card in cards:
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
                                        Checkbox(label=card.term),
                                        Text(card.definition),
                                    ]
                                ),
                            ),
                            IconButton(
                                icon=icons.DELETE, data=card.id, on_click=delete_card
                            ),
                        ],
                    )
                )

        update_cards()
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
        self.page.window_height = 600
        self.page.window_width = 600
        self.quest_layout = Column()
        self.next = TextButton(text=" ", visible=True, on_click=self.next_quest, disabled=True)
        self.result_positive = Text("", color=colors.GREEN, weight="bold", visible=True)
        self.quest_label = Text("", size=20, weight="bold")
        self.quest_image = Image(
            src="Excel.jpg",
            width=100,
            height=100,
            visible=False,
            border_radius=border_radius.all(50),
            fit="fill",
        )
        self.info = Text(
            "Пройденых вопросов: {}, Правильных ответов: {}, Неправильных ответов: {}".format(
                0, 0, 0
            ),
            color=colors.BLUE_600,
            weight="bold",
        )
        self.count_valid = 0
        self.count_invalid = 0
        self.count_quest = 0
        self.update()

    def next_quest(self, e):
        self.generate_quests()

    def generate_quests(
        self,
    ):
        self.quest_layout.controls.clear()
        self.count_quest += 1
        self.result_positive.value = ""
        self.next.text = ' '
        self.next.disabled = True
        self.quest_image.visible = True
        session = Session()
        data = session.query(Card).all()
        rand_values = [data.pop(random.randint(0, len(data) - 1)) for i in range(5)]
        self.quest_label.value = rand_values[0].term
        current_quest = rand_values[0]
        if rand_values[0].icon_path:
            self.quest_image.src = f"{rand_values[0].icon_path}"
            self.quest_image.visible = True
            self.update()
        self.update()

        def change_button(e):
            if current_quest.definition == e.control.data:
                e.control.icon = icons.CHECK_CIRCLE
                e.control.bgcolor = colors.GREEN
                self.result_positive.value = "Правильно!"
                for i in self.quest_layout.controls:
                    i.disabled = True
                self.count_valid += 1
                self.next.text = 'Дальше'
                self.update()
            else:
                e.control.icon = icons.WARNING
                e.control.bgcolor = colors.RED
                self.result_positive.value = "Неправильно!"
                self.count_invalid += 1
                for i in self.quest_layout.controls:
                    i.disabled = True
                self.next.text = 'Дальше'
                self.update()

            self.info.value = f"Пройденых вопросов: {self.count_quest}, Правильных ответов: {self.count_valid}, Неправильных ответов: {self.count_invalid}"
            self.next.visible = True
            self.next.disabled = False
            self.update()

        random.shuffle(rand_values)
        for i in range(len(rand_values)):
            self.quest_layout.controls.append(
                FilledButton(
                    text=rand_values[i].definition,
                    data=rand_values[i].definition,
                    on_click=change_button,
                )
            )
        self.quest_layout.update()

    def build(self):

        def follow_admin(e):
            admin_ui = Auth(self.page)
            self.page.controls.clear()
            self.page.add(admin_ui)
            self.page.update()

        btn_admin = TextButton(
            "В админ панель",
            icon=icons.SWITCH_ACCESS_SHORTCUT_SHARP,
            on_click=follow_admin,
        )

        view = Column(
            alignment="center",
            controls=[
                Row(alignment="center", controls=[self.info]),
                Row(alignment="center", controls=[self.quest_image]),
                Row(alignment="center", controls=[self.quest_label]),
                Row(alignment="center", controls=[self.quest_layout]),
                Row(alignment="center", controls=[self.result_positive, self.next]),
                Row(vertical_alignment="end", controls=[btn_admin]),
            ],
        )
        return view


class Auth(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page

    def build(self):
        login_view = TextField(label="Имя пользователя", width=300, border="outline")
        passwd_view = TextField(
            label="Пароль", width=300, password=True, border="outline"
        )
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
                Row(alignment="center", controls=[Text('Авторизация', weight='bold',size=25, color='blue900')]),
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
                    self.page.controls.pop()
                    self.page.add(AdminUI(self.page))
                    self.page.vertical_alignment = "start"
                    self.page.horizontal_alignment = "start"
                    self.page.update()
                else:
                    user_ui = UserUI(self.page)
                    self.page.controls.pop()
                    self.page.add(user_ui)
                    user_ui.generate_quests()
                    self.page.update()

            else:
                message.value = "Неверные имя пользователя/пароль!"
                self.page.update()

        login_btn.on_click = auth
        return view


def main(page: Page):
    page.title = "FlashCard"
    page.window_width = 350
    page.window_height = 350
    page.window_maximized = False
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    auth = Auth(page)
    page.add(auth)


flet.app(target=main, upload_dir="assets", assets_dir="assets")
