from peewee import CharField, TextField, ForeignKeyField, BooleanField, DateTimeField
from .auth import User
from .base import BaseModel

import datetime

class Category(BaseModel):
    name = CharField(unique=True)

class Post(BaseModel):
    title = CharField(unique=True)
    content = TextField()
    description = TextField()
    date = DateTimeField(default=datetime.datetime.now, null=True)
    slug = CharField(unique=True, null=True)
    is_published = BooleanField(default=False)
    author = ForeignKeyField(User, null=True)
    category = ForeignKeyField(Category)
