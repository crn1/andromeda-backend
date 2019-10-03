from peewee import SqliteDatabase

database = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})
