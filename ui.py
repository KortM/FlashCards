
import flet
from flet import Container, ListView, colors, border
from flet import Checkbox, Column, FloatingActionButton, Page, Row, TextField, UserControl, icons
from flet import FilledButton, FilePicker, FilePickerUploadFile, ElevatedButton, Page, Text, Checkbox
from db import User_session, Session, User, Card
import threading

class AdminUI(UserControl):

    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        print('admin_ui')
        term = TextField(label='Термин', multiline=True)
        definition = TextField(label='Определение', multiline=True, height=150)
        self.path = []
        def upload(e):
            if image_path.result != None and image_path.result.files != None:
                for f in image_path.result.files:
                    self.path.append(FilePickerUploadFile(
                            f.name,
                            self.page.get_upload_url(f.name, 600)
                    ))
                #image_path.upload(self.path)
        def new_term(e):
            if term.value and definition.value and self.path:    
                image_path.upload(self.path)
                questions.controls.append(
                    Row(
                        alignment='spaceBetween',
                        width=300,
                        scroll=True,
                        controls=[
                            Container(
                                border = border.only(bottom=border.BorderSide(1, 'black')),
                                content=Row(
                                controls = [
                                    Checkbox(label = term.value), 
                                    Text(definition.value),
                                ]  
                            ),
                            ),
                            FloatingActionButton(icon=icons.DELETE)
                        ]
                    )
                )
                questions.update()
                self.update()


        image_path = FilePicker(on_result=upload)
        btn_add = FilledButton(on_click=new_term, icon=icons.ADD)

        questions = ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        view =  Row(
            height=300,
            controls=[
                Column(
                    controls=[
                        Row(
                        alignment='center',
                        controls=[term]
                    ),
                        Row(
                        alignment='center',
                        controls=[definition]
                    ),  
                        Row(
                        alignment='center',
                        controls=[
                            ElevatedButton(
                                text='Загрузить изображение', icon=icons.FILE_OPEN,
                                on_click=lambda _: image_path.pick_files()
                            ),
                        btn_add
                        ]
                    ),
                    ]
                ),
                questions

            ]
        )
        view.controls.append(image_path)
        return view

class UserUI(UserControl):

    def build(self):
        pass

def main(page: Page):
    page.title = "FlashCard"
    login_view = TextField(label='Имя пользователя', width=300, height=40)
    passwd_view = TextField(label='Пароль', width=300,
                            height=40, password=True)
    login_btn = FloatingActionButton(text='Войти', width=300)

    view = Column(
        controls=[
            Row(
                alignment='center',
                controls=[login_view]
            ),
            Row(
                alignment='center',
                controls=[passwd_view]
            ),
            Row(
                alignment='center',
                controls=[login_btn]
            )
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
                page.vertical_alignment = 'start'
                page.horizontal_alignment = 'start'
                page.update()
            else:
                page.controls.pop()
                page.add(UserUI())
                page.update()


    #page.on_route_change = route_change

    login_btn.on_click = auth

    #page.window_resizable =False
    page.window_width = 350
    page.window_height = 350
    page.window_maximized = False
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.add(view)

flet.app(target=main, upload_dir='assets')