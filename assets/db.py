from email.policy import default
from enum import unique
import os
from xmlrpc.client import Boolean
from sqlalchemy import create_engine, Column, Integer, String, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib, uuid

card_db = 'Card.db'
user_db = 'Users.db'
engine = create_engine('sqlite:///{}'.format(card_db), connect_args={'check_same_thread': False})
user_engine = create_engine('sqlite:///{}'.format(user_db), connect_args={'check_same_thread': False})
Base = declarative_base()
Session = sessionmaker(bind=engine)
User_session = sessionmaker(bind=user_engine)

class Card(Base):
    __tablename__ = 'Card'

    id = Column(Integer, primary_key = True)
    term = Column(String(500))
    definition = Column(String(1000))
    icon_path = Column(String(1000))

    def __init__(self):
        return 'Term: {}, Definition: {}, Icon: {}'.format(self.term, self.definition, self.icon_path)

class User(Base):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    pwd_hash = Column(String(550))
    role = Column(BOOLEAN, unique= False, default=False)

    def __init_(self, name: str):
        self.name = name
    
    def __repr__(self) -> str:
        return 'User: {}, PWD: {}, Role: {}'.format(self.name, self.pwd_hash, self.role)
    
    def set_password(self, password):
        self.pwd_hash = hashlib.sha256(''.join([password]).encode('utf-8')).hexdigest()
    
    def check_password(self, password):
        key = hashlib.sha256(''.join([password]).encode('utf-8')).hexdigest()
        if key == self.pwd_hash:
            return True
        else:
            return False

Base.metadata.create_all(engine)
Base.metadata.create_all(user_engine)

admin = User(name = 'admin', role = True)
admin.set_password('J4cG9CgjCjpH')
admin.check_password('J4cG9CgjCjpH')
user = User(name = 'user')
user.set_password('1234')
user.check_password('1234')
user_session = User_session()
user_session.add(admin)
user_session.add(user)
user_session.commit()