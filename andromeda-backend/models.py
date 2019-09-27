from peewee import *
from flask_login import UserMixin
import datetime

db = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})

def initialize_db():
    db.connect()
    db.create_tables([User, Role, UserRole, File, Category, Post], safe=True)

class BaseModel(Model):
    class Meta:
        database = db

class User(UserMixin, BaseModel):
    fullname = CharField()
    email = CharField(unique=True)
    password = CharField()
    description = TextField(null=True)
    avatar_url = CharField(null=True)

    def has_role(self, role):
        user_role = (UserRole
                    .select()
                    .join(Role)
                    .switch(UserRole)
                    .join(User)
                    .where(
                        (User.id == self.id) &
                        (Role.name == role)
                    ))
        if user_role:
            return True
        return False

    def get_roles(self):
        users = (UserRole
                .select()
                .join(Role)
                .switch(UserRole)
                .join(User)
                .where(User.id == self.id))
        roles = []
        for user in users:
            roles.append({
                'user_role_id': user.id,
                'role_id': user.role.id,
                'name': user.role.name,
            })
        return roles

class Role(BaseModel):
    name = CharField(unique=True)

class UserRole(BaseModel):
    user = ForeignKeyField(User)
    role = ForeignKeyField(Role)

class File(BaseModel):
    filename = CharField(unique=True)
    date_uploaded = DateTimeField(default = datetime.datetime.now, null=True)
    description = CharField()

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
