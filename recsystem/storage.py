
import sqlite3

DB_SCHEMA = """
    CREATE TABLE IF NOT EXISTS entities (
        id INTEGER NOT NULL PRIMARY KEY,
        published INTEGER NOT NULL,
        guid TEXT NOT NULL UNIQUE,
        url TEXT NOT NULL,
        title TEXT NOT NULL,
        alpha REAL NOT NULL DEFAULT 1.0,
        beta REAL NOT NULL DEFAULT 1.0
    );
"""


class Storage(object):

    class DuplicateEntry(Exception):
        pass

    def __init__(self, **database_kwargs):
        self.connection = self.get_connection(**database_kwargs)

    @staticmethod
    def get_connection(**database_kwargs):
        return sqlite3.connect(**database_kwargs)

    @classmethod
    def create_schema(cls, **database_kwargs):
        connection = cls.get_connection(**database_kwargs)
        try:
            with connection:
                for obj in DB_SCHEMA.split(';'):
                    obj = obj.strip()
                    if not obj:
                        continue
                    connection.execute(obj)
        finally:
            connection.close()

    def insert_entity(self, published, guid, url, title):
        with self.connection:
            try:
                self.connection.execute(
                    "INSERT INTO entities (published, guid, url, title) "
                    "VALUES (?, ?, ?, ?)", (published, guid, url, title))
            except sqlite3.IntegrityError:
                raise self.DuplicateEntry(guid)
