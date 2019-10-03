from peewee import CharField, TextField, ForeignKeyField
from flask_login import UserMixin
from .base import BaseModel

import datetime

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
