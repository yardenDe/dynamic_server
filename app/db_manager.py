from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

def dict_result(result):
    res = []
    for row in result:
        d = row._asdict()
        res.append(d)
    return res

class DB_Manager:
    """Handles any database interactions using SQLAlchemy."""
    def __init__(self):
        load_dotenv()
        self.db_url = os.getenv("DATABASE_URL", "sqlite:///local.db")
        self.engine = create_engine(self.db_url)
        self.log_table_initialized = False  
        

    def execute_query(self, query, params=None):
        """Handles read-only queries"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), params)
                return dict_result(result)
        except Exception as e:
            raise e

    def execute_transaction(self, query, params=None):
        """Handles all queries"""
        try:
            with self.engine.begin() as conn:
                return conn.execute(text(query), params)
        except Exception as e:
            raise e
        
    def create_log_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS execution_times (
                file_name TEXT PRIMARY KEY,
                date_created TEXT,
                record_count INTEGER,
                select_time_ms REAL,
                write_time_ms REAL
            )
        """
        self.execute_transaction(query)

    def add_log(self, params):
        if not self.log_table_initialized:
            self.create_log_table()
            self.log_table_initialized = True

        query = """
            INSERT INTO execution_times
            (file_name, date_created, record_count, select_time_ms, write_time_ms)
            VALUES (:file_name, :date_created, :record_count, :select_time_ms, :write_time_ms)
        """
        self.execute_transaction(query, params)
