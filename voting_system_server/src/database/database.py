import mariadb
from contextlib import contextmanager
from pydantic import BaseModel

class Database:
    _instance : Database = None
    def __new__(cls , *args, **kwargs) -> 'Database':
        if cls._instance is None:
            cls._instance : Database =  super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'): return
        self._pool = mariadb.ConnectionPool(
            host="localhost",
            port=3306,
            pool_size= 5,
            pool_name='voting_pool',
            user='voting_app',
            password='bongbongbangag2026',
            database='voting_app'
        )
        self._initialized = True

    @contextmanager
    def transaction(self):
        conn = self._pool.get_connection()
        try:
            conn.begin()
            yield conn
            conn.commit()
        except BaseException:
            conn.rollback()
            raise
        finally:
            conn.close()
    def fetchAll(self, cursor):
        cols = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(cols,row)) for row in rows]

    def hydrate(self, model: type[BaseModel], rows):
        return [model.model_validate(row) for row in rows]