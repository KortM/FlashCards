from email.mime import image
import flet
from flet import (
    IconButton, Page, Row, TextField, icons, theme, Column,
    RadioGroup, Radio, Text, ElevatedButton, FilledButton, ButtonStyle,
    colors, Image, View, AppBar, FilePicker, ElevatedButton, FilePickerUploadFile
)
from db import User, Card, User_session, Session

def gerenerate_questions():
    #TODO

    pass

def user_UI(page:Page):
    print('user_UI')
    page.views.clear()
    page.views.append(
        View(
            '/Card',
            [
                AppBar(title= Text('FlashCards'))
            ],
        )
    )
    page.update()

def admin_UI(page:Page):
    print('admin_ui')
    term = TextField(label='Термин')
    definition = TextField(label='Определение')
    
    
    def upload(e):
        path = []
        print(image_path.result)
        if image_path.result != None and image_path.result.files != None:
            for f in image_path.result.files:
                path.append(
                    FilePickerUploadFile(
                        f.name,
                        upload_url=page.get_upload_url(f.name, 600),
                    )
                )
            image_path.upload(path)
        print(path)
    
    image_path = FilePicker(on_result=upload)
    btn_add = FilledButton( on_click=upload, icon=icons.ADD)
    
    return Column(
        alignment= 'center',
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
                        on_click= lambda _: image_path.pick_files()
                        ),
                        btn_add
                    ]
            ),
            
        ]
    )
    '''page.window_width = 500
    page.window_height = 400
    page.overlay.append(image_path)
    page.add(view)
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.window_maximized = False
    page.update()
    print('after update')'''
    
def main(page: Page):
    page.title = "FlashCard"
    login_view = TextField(label='Имя пользователя', width=300, height=40)
    passwd_view = TextField(label = 'Пароль', width=300, height=40, password=True)
    login_btn = FilledButton(text = 'Войти', width = 300)
    
    view = Column(
        controls=[
            Row(
                alignment='center', 
                controls = [login_view]
            ),
            Row(
                alignment='center',
                controls=[passwd_view]
            ),
            Row(
                alignment='center', 
                controls= [login_btn] 
            )
        ]
    )
    def route_change(route):
        print('route change')
        if page.route == '/Card':
            page.views.append(user_UI(page))
        if page.route == '/Admin':
            page.views.append(admin_UI(page))

    def auth(e):
        session = User_session()
        login = login_view.value
        passwd = passwd_view.value
        local_user = session.query(User).filter_by(name = login.lower()).first()
        if local_user and local_user.check_password(passwd):
            if local_user.role:
                print(local_user)
                page.views.pop()
                page.add(admin_UI(page))
                page.update()
                
            else:
                page.go('/Card')
                page.views.append(user_UI(page))
                
    
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
    
'''cg = RadioGroup(content=Column(
        [
            FilledButton(text='Red', width=300, icon='circle', style=ButtonStyle(
                color=colors.INDIGO
            )),
            FilledButton(text='Green', width=300), 
            FilledButton(text='Yellow', width=300)
        ]
    ))'''