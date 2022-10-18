
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
    Markdown
)
import random
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
                        icon_path=f"{self.path[0].name}",
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
        self.quest_layout = Column()
        self.next = TextButton(text="Дальше", visible=False, on_click=self.next_quest)
        self.result_positive = Text("Правильно!", color=colors.GREEN, weight="bold", visible=False)
        self.result_negative = Text("Неправильно!", color=colors.RED,weight='bold', visible=False)
        self.quest_label = Text(
            "", size=20, weight="bold"
        )
        self.quest_image = Image(src='Excel.jpg', width=100, height=100, visible=False)
        self.update()

    def next_quest(self, e):
        self.generate_quests()

    def generate_quests(self,):
        self.quest_layout.controls.clear()
        self.result_negative.visible = False
        self.result_positive.visible = False
        self.next.visible = False
        self.quest_image.visible = True
        session = Session()
        data = session.query(Card).all()
        num_quest = random.randint(0, len(data)-1)
        current_quest = data.pop(num_quest)
        rand_quest = random.randint(0, len(data)-1)
        current_variant = data.pop(rand_quest)
        rand_quest2 = random.randint(0, len(data)-1)
        current_variant2 = data.pop(rand_quest2)
        self.quest_label.value = current_quest.term
        if current_quest.icon_path:
            print(current_quest.icon_path)
            self.quest_image.src = f'{current_quest.icon_path}'
            self.quest_image.visible = True
            self.update()
        self.update()
        
        print(current_quest.term)

        def change_button(e):
            #print(e.control.data)
            print(current_quest.definition, e.control.data)
            if current_quest.definition == e.control.data:
                e.control.icon = icons.CHECK_CIRCLE
                e.control.bgcolor = colors.GREEN
                self.result_positive.visible = True
                for i in self.quest_layout.controls:
                    i.disabled = True
            else:
                e.control.icon = icons.WARNING
                e.control.bgcolor = colors.RED
                self.result_negative.visible = True
                for i in self.quest_layout.controls:
                    i.disabled = True

            self.next.visible = True
            self.update()

        data = [current_quest, current_variant, current_variant2]
        
        numbers = [i for i in range(len(data))]
        random.shuffle(numbers)
        for i in range(len(data)):
            self.quest_layout.controls.append(
                FilledButton(text=data[numbers[i]].definition,data=data[numbers[i]]
                .definition, on_click=change_button)
            )
        self.quest_layout.update()

    def build(self):
        quest = RadioGroup()
        quest.content = self.quest_layout

        view = Column(
            horizontal_alignment="center",
            controls=[
                Row(alignment='center', controls=[self.quest_image]),
                Row(alignment="center", controls=[self.quest_label]),
                Row(alignment="center", controls=[quest]),
                Row(alignment="center", controls=[self.result_positive,self.result_negative, self.next]),
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
                user_ui = UserUI(page)
                page.controls.pop()
                page.add(user_ui)
                user_ui.generate_quests()
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


flet.app(target=main, upload_dir="assets", assets_dir='assets')
