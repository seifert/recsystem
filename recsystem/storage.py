
import collections
import datetime
import logging
import threading

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

Entity = collections.namedtuple(
    'Entity', ['id', 'published', 'guid', 'url', 'title', 'alpha', 'beta'])

logger = logging.getLogger(__name__)


class Storage(object):

    class DuplicateEntry(Exception):
        pass

    def __init__(self, **database_kwargs):
        self.connection = self.get_connection(**database_kwargs)
        self.database_kwargs = database_kwargs

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

    @staticmethod
    def create_entity(entity_id, published_ts, guid, url, title, alpha, beta):
        published_dt = datetime.datetime.fromtimestamp(published_ts)
        return Entity(entity_id, published_dt, guid, url, title, alpha, beta)

    def entities_list(self, limit=10):
        with self.connection:
            entities = self.connection.execute(
                "SELECT id, published, guid, url, title, alpha, beta "
                "FROM entities ORDER BY published DESC LIMIT ?", (limit,))
            return [self.create_entity(*ent) for ent in entities]

    @classmethod
    def _save_alphas_betas_worker(cls, database_kwargs, alphas, betas):
        connection = cls.get_connection(**database_kwargs)
        try:
            with connection:
                for k, v in alphas.items():
                    connection.execute(
                        "UPDATE entities SET alpha=alpha+? WHERE id=?", (v, k))
                for k, v in betas.items():
                    connection.execute(
                        "UPDATE entities SET beta=beta+? WHERE id=?", (v, k))
        finally:
            connection.close()

    def save_alphas_betas(self, alphas, betas):
        logger.info("Save alphas and betas into database")
        t = threading.Thread(
            target=self._save_alphas_betas_worker,
            args=(self.database_kwargs, alphas, betas))
        t.start()
